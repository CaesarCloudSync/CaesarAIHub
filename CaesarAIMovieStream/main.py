import uvicorn
from fastapi import FastAPI, WebSocket, Depends
import requests
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from CaesarAITorrentParsers.CaesarAIJackett import CaesarAIJackett
from CaesarAIConstants import CaesarAIConstants
from CaesarAITorrentParsers.CaesarAIJackett.responsemodels.EpisodesResponse import EpisodesResponse
from CaesarAITorrentParsers.CaesarAIJackett.requestmodels.EpisodesRequest import EpisodesRequest
from CaesarAITorrentParsers.CaesarAIJackett.requestmodels.MoviesRequest import MoviesRequest
from CaesarAITorrentParsers.CaesarAIProwlarr import CaesarAIProwlarr
from CaesarAIRealDebrid.requestmodels.StreamingLinkRequest import StreamingLinkRequest
from CaesarAIRealDebrid import CaesarAIRealDebrid
from CaesarAIRealDebrid.responses.StreamingLinkResponse import StreamingLinkResponse
from CaesarAIRealDebrid.responses.StatusAndProgressResponse import StatusAndProgressResponse
from fastapi.responses import StreamingResponse
from CaesarSQLDB.caesar_create_tables import CaesarCreateTables
from CaesarSQLDB.caesarcrud import CaesarCRUD
from CaesarAIUtils import CaesarAIUtils
from starlette.websockets import WebSocketDisconnect,WebSocketState
from websockets.exceptions import ConnectionClosedError,ConnectionClosedOK
from CaesarAICelery.tasks import get_unfinished_episodes
from CaesarAIRedis import CaesarAIRedis
from fastapi import FastAPI
from datetime import datetime
import json
from celery.result import AsyncResult
from CaesarAICelery.celery_worker import celery_app
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler  # runs tasks in the background
from apscheduler.triggers.cron import CronTrigger  # allows us to specify a recurring time for execution
from CaesarAICelery.schedules import CaesarAISchedules
from CaesarAITorrentParsers.CaesarAIMediaIndexers import CaesarAIMediaIndexers
import json

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logging.getLogger('apscheduler').setLevel(logging.WARNING) # This hides the apscedhuler events


# Set up the scheduler
scheduler = BackgroundScheduler()
trigger = CronTrigger(hour=0, minute=0) # 00:00 dayZZ # every minute
scheduler.add_job(CaesarAISchedules.update_all_torrent_indexers, trigger)
scheduler.start()


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

caesarcrud = CaesarCRUD()
caesaraird = CaesarAIRealDebrid()
cartable = CaesarCreateTables()

cartable.create(caesarcrud)

# Ensure the scheduler shuts down properly on application exit.
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    scheduler.shutdown()


@app.get('/')# GET # allow all origins all methods.
async def index():
    return "Welcome to CaesarAIMovieStream."
@app.get('/healthcheck')# GET # allow all origins all methods.
async def healthcheck():
    return {"status":"OK"}

@app.get("/api/v1/get_indexers")
async def get_indexers():
    indexers = CaesarAIJackett.get_current_torrent_indexers()
    return {"indexers":indexers}

@app.get("/api/v1/start_get_unfinished_episodes")
async def start_get_unfinished_episodes():
    logging.info(f"Creating interrupted episodes task...")
    result = get_unfinished_episodes.delay()
    logging.info(f"Interrupted episodes task created.")
    print(result.id,flush=True)
    return {"task_id":result.id}
@app.get("/status/{task_id}")
def get_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)

    if result.state == "PENDING":
        return {"status": "pending", "results": []}
    elif result.state == "PROGRESS":
        return {"status": "in-progress", "results": result.info.get("results", [])}
    elif result.state == "COMPLETED":
        return {"status": "completed", "results": result.result.get("results", [])}
    else:
        return {"status": result.state, "results": []}


@app.get("/api/v1/store_recent_episodes")
async def store_recent_episodes(episode_data: EpisodesRequest = Depends()):
    """
    Stream episodes based on title, season, and episode number.
    """
    cj = CaesarAIJackett(db=True,asynchronous=True)
    cr = CaesarAIRedis(async_mode=True)
    print(f"Storing episode: {episode_data.title} S{episode_data.season}E{episode_data.episode}",flush=True)
    episode_id = CaesarAIConstants.EPISODE_REDIS_ID.format(query=episode_data.title,season=episode_data.season,episode=episode_data.episode)
    episodes_exists_in_db = await cj.check_batch_episodes_db_async(episode_data.title,episode_data.season,episode_data.episode)
    await cr.async_delete__episode_task(episode_id)
    task_to_save_in_db_exists = await cr.async_hget_episode_task(episode_id)
    if not episodes_exists_in_db and not task_to_save_in_db_exists:
        print(episode_id,flush=True)
        logging.info(episode_id)
        await cr.async_set_episode_task(episode_id,"pending")
        await start_get_unfinished_episodes()
        return { "status": "pending", "message": "Episode task created, please check the status later." }
    else:
        return {"status": "completed", "message": "Episode already exists in the database."}

@app.websocket("/api/v1/stream_get_episodews")
async def stream_get_episodews(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = EpisodesRequest.model_validate(await websocket.receive_json())
            indexers = await CaesarAIJackett.get_current_torrent_indexers_async()
            print(indexers,flush=True)
            async for event in CaesarAIJackett.stream_get_episodews(data.title,data.season,data.episode,indexers):
                #print(event)
                await websocket.send_json(event)
    except (WebSocketDisconnect,ConnectionClosedOK,ConnectionClosedError) as cex:
        cj = CaesarAIJackett(db=True,asynchronous=True)
        cr = CaesarAIRedis(async_mode=True)
        episode_id = CaesarAIConstants.EPISODE_REDIS_ID.format(query=data.title,season=data.season,episode=data.episode)
        episodes_exists_in_db = await cj.check_batch_episodes_db_async(data.title,data.season,data.episode)
        await cr.async_delete__episode_task(episode_id)
        task_to_save_in_db_exists = await cr.async_hget_episode_task(episode_id)
        if not episodes_exists_in_db and not task_to_save_in_db_exists:
            print(episode_id,flush=True)
            logging.info(episode_id)
            await cr.async_set_episode_task(episode_id,"pending")
            await start_get_unfinished_episodes()
@app.websocket("/api/v1/stream_get_moviesws")
async def stream_get_moviesws(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = MoviesRequest.model_validate(await websocket.receive_json())
            indexers = await CaesarAIJackett.get_current_torrent_indexers_async()
            indexers = CaesarAIMediaIndexers.sort_indexer_for_movie(indexers)
            async for event in CaesarAIJackett.stream_get_moviesws(data.title,indexers):
                #print(event)
                await websocket.send_json(event)
    except (WebSocketDisconnect,ConnectionClosedOK,ConnectionClosedError) as cex:
        pass
@app.websocket("/api/v1/stream_get_gamews")
async def stream_get_gamews(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = MoviesRequest.model_validate(await websocket.receive_json())
            indexers = await CaesarAIJackett.get_current_torrent_indexers_async()
            indexers = CaesarAIMediaIndexers.sort_indexer_for_game(indexers)
            async for event in CaesarAIJackett.stream_get_gamews(data.title,indexers):
                #print(event)
                await websocket.send_json(event)
    except (WebSocketDisconnect,ConnectionClosedOK,ConnectionClosedError) as cex:
        pass

@app.post('/api/v1/torrent_magnet')# GET # allow all origins all methods.
async def torrent_magnet(magnetdata:StreamingLinkRequest):
    try:
        torrent_link = magnetdata.torrent_link
        magnet_link = magnetdata.magnet_link
        print(torrent_link,magnet_link)
        if magnet_link:
            magnet_link = magnetdata.magnet_link
            _id = caesaraird.add_magnet(magnet_link)
            caesaraird.select_files(_id)
            return caesaraird.get_progress_and_status(_id)

        elif torrent_link:
            torrent_link = torrent_link.replace(CaesarAIConstants.BASE_LOCALHOST,CaesarAIConstants.BASE_PROWLER_CONTAINER) if "localhost" in torrent_link else torrent_link
            _id = caesaraird.add_torrent(torrent_link)
            caesaraird.select_files(_id)
            return caesaraird.get_progress_and_status(_id)

    

    except Exception as ex:
        return {"error":f"{type(ex)},{ex}"}

@app.get('/api/v1/check_torrent',response_model=StatusAndProgressResponse)# GET # allow all origins all methods.
async def check_torrent(_id:str):
    try:
        return caesaraird.get_progress_and_status(_id)
    except Exception as ex:
        return {"error":f"{type(ex)},{ex}"}


@app.get('/api/v1/get_streaming_links')# GET # allow all origins all methods.,response_model=StreamingLinkResponse)
async def get_streaming_links(_id:str):
    try:
        return {"streams":await caesaraird.get_streaming_links(_id)}
    except Exception as ex:
        return {"error":f"{type(ex)},{ex}"}
@app.get('/api/v1/get_streaming_linksws')# GET # allow all origins all methods.,response_model=StreamingLinkResponse)
async def get_streaming_linkswss(_id:str):
    try:
        return {"streams":await caesaraird.get_streaming_links(_id)}
    except Exception as ex:
        return {"error":f"{type(ex)},{ex}"}
@app.get('/api/v1/get_container_links')# GET # allow all origins all methods.,response_model=StreamingLinkResponse)
async def get_container_links(_id:str):
    try:
        return {"streams":await caesaraird.get_container_links(_id)}
    except Exception as ex:
        return {"error":f"{type(ex)},{ex}"}
@app.get ("/api/v1/update_all_torrent_indexers")# GET # allow all origins all methods.
async def update_all_torrent_indexers():
    try:
        
        return CaesarAISchedules.update_all_torrent_indexers()
    except Exception as ex:
        return {"status":"error","message":f"{type(ex)},{ex}"}
if __name__ == "__main__":
    uvicorn.run("main:app",port=8080,log_level="info")
