import uvicorn
from fastapi import FastAPI
import requests
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from CaesarAITorrentParsers.CaesarAIJackett import CaesarAIJackett
from CaesarAIConstants import CaesarAIConstants
from CaesarAITorrentParsers.CaesarAIJackett.responses.EpisodesResponse import EpisodesResponse
from CaesarAITorrentParsers.CaesarAIProwlarr import CaesarAIProwlarr
from CaesarAIRealDebrid.requestmodels.StreamingLinkRequest import StreamingLinkRequest
from CaesarAIRealDebrid import CaesarAIRealDebrid
from CaesarAIRealDebrid.responses.StreamingLinkResponse import StreamingLinkResponse
from CaesarAIRealDebrid.responses.StatusAndProgressResponse import StatusAndProgressResponse
from fastapi.responses import StreamingResponse
from CaesarSQLDB.caesar_create_tables import CaesarCreateTables
from CaesarSQLDB.caesarcrud import CaesarCRUD
from CaesarAIUtils import CaesarAIUtils
import json
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
@app.get('/')# GET # allow all origins all methods.
async def index():
    return "Welcome to CaesarAIMovieStream."
@app.get('/healthcheck')# GET # allow all origins all methods.
async def healthcheck():
    return {"status":"OK"}

@app.get("/api/v1/get_indexers")
async def get_indexers():
    indexers = CaesarAIJackett.get_all_torrent_indexers()
    return {"indexers":indexers}
@app.get('/api/v1/get_episodes',response_model=EpisodesResponse)# GET # allow all origins all methods.
async def get_episodes(title:str,season:int,episode:int,service:Optional[str]=None):
    try:
        caejackett = CaesarAIJackett(db=True)
        if not service or "jackett":
            if caejackett.check_batch_episodes_db(title,season,episode):
                torrentinfo = caejackett.get_episodes_db(title,season,episode)
                return {"episodes":torrentinfo}
               
            else:
                url = f"{CaesarAIConstants.BASE_JACKETT_URL}{CaesarAIConstants.TORZNAB_ALL_SUFFIX}?apikey={CaesarAIConstants.JACKETT_API_KEY}&t={CaesarAIConstants.ENDPOINT}&q={title}&season={season}&episode=${episode}"
                caejackett = CaesarAIJackett(url)
                torrentinfo = caejackett.get_torrent_info(query=title)
                torrentinfo_single = caejackett.get_single_episodes()
                torrentinfo_batched = caejackett.get_batch_episodes()
                caejackett.save_batch_episodes(torrentinfo)
                torrentinfo = torrentinfo_batched + torrentinfo_single 
                return {"episodes":torrentinfo}

            
            
        else:
            url = f"{CaesarAIConstants.BASE_PROWLER_URL}{CaesarAIConstants.TORZNAB_ALL_SUFFIX}?apikey={CaesarAIConstants.PROWLARR_API_KEY}&query={title} {CaesarAIProwlarr.format_season(season)}"
            caeprowlarr = CaesarAIProwlarr(url)
            torrentinfo = caeprowlarr.get_torrent_info(query=title)
            torrentinfo_single = caeprowlarr.get_single_episodes()
            torrentinfo_batched = caeprowlarr.get_batch_episodes()
            
            torrentinfo = torrentinfo_single + torrentinfo_batched
            return {"episodes":torrentinfo}

    except Exception as ex:
        return {"error":f"{type(ex)},{ex}"}
@app.get('/api/v1/stream_get_episodes')# GET # allow all origins all methods. ,response_model=EpisodesResponse
async def stream_get_episodes(title:str,season:int,episode:int,save:Optional[bool]=True,service:Optional[str]=None):
    try:

        if not service or "jackett":
            indexers = CaesarAIJackett.get_all_torrent_indexers()
            return StreamingResponse(CaesarAIJackett.episodes_streamer(title,season,episode,indexers,save), media_type="text/event-stream")
        else:
            pass



    except Exception as ex:
        return {"error":f"{type(ex)},{ex}"}    
@app.get('/api/v1/stream_get_single_episodes')# GET # allow all origins all methods. ,response_model=EpisodesResponse
async def stream_get_single_episodes(title:str,season:int,episode:int,service:Optional[str]=None):
    try:

        if not service or "jackett":
            indexers = CaesarAIJackett.get_all_torrent_indexers()
            return StreamingResponse(CaesarAIJackett.single_episode_streamer(title,season,episode,indexers), media_type="text/event-stream")
        else:
            pass



    except Exception as ex:
        return {"error":f"{type(ex)},{ex}"}
@app.get('/api/v1/get_single_episodes',response_model=EpisodesResponse)# GET # allow all origins all methods.
async def get_single_episodes(title:str,season:int,episode:int,service:Optional[str]=None):
    try:
        if not service or "jackett":
            url = f"{CaesarAIConstants.BASE_JACKETT_URL}{CaesarAIConstants.TORZNAB_ALL_SUFFIX}?apikey={CaesarAIConstants.JACKETT_API_KEY}&t={CaesarAIConstants.ENDPOINT}&q={title}&season={season}&ep={episode}"
            caejackett = CaesarAIJackett(url)
            torrentinfo = caejackett.get_torrent_info(query=title)           
            torrentinfo = caejackett.get_single_episodes()
        else:
            url = f"{CaesarAIConstants.BASE_PROWLER_URL}{CaesarAIConstants.TORZNAB_ALL_SUFFIX}?apikey={CaesarAIConstants.PROWLARR_API_KEY}&query={title} {CaesarAIProwlarr.format_season_episode(season,episode)}"
            caeprowlarr = CaesarAIProwlarr(url)
            torrentinfo = caeprowlarr.get_torrent_info(query=title)
            torrentinfo = caeprowlarr.get_single_episodes()

        return {"episodes":torrentinfo}
    except Exception as ex:
        return {"error":f"{type(ex)},{ex}"}
@app.get('/api/v1/get_batch_episodes',response_model=EpisodesResponse)# GET # allow all origins all methods.
async def get_batch_episodes(title:str,season:int,save:Optional[bool]=True,service:Optional[str]=None):
    try:
        if not service or "jackett":
            caejackett = CaesarAIJackett(db=True)
            print("Starting...")
            if caejackett.check_batch_seasons_db(title,season):
                torrentinfo = caejackett.get_batch_season_db(title,season)
                save = False
            else:
                print("Extracting")
                url = f"{CaesarAIConstants.BASE_JACKETT_URL}{CaesarAIConstants.TORZNAB_ALL_SUFFIX}?apikey={CaesarAIConstants.JACKETT_API_KEY}&t={CaesarAIConstants.ENDPOINT}&q={title}"
                caejackett = CaesarAIJackett(url)
                torrentinfo = caejackett.get_torrent_info(query=title)
                torrentinfo = caejackett.get_batch_episodes()
            if save:
                print("Saving...")
                caejackett.save_batch_episodes(torrentinfo)
        else:
            url = f"{CaesarAIConstants.BASE_PROWLER_URL}{CaesarAIConstants.TORZNAB_ALL_SUFFIX}?apikey={CaesarAIConstants.PROWLARR_API_KEY}&query={title} {CaesarAIProwlarr.format_season(season)}"
            caeprowlarr = CaesarAIProwlarr(url)
            torrentinfo = caeprowlarr.get_torrent_info(query=title)
            torrentinfo = caeprowlarr.get_batch_episodes()

        return {"episodes":torrentinfo}
    except Exception as ex:
        return {"error":f"{type(ex)},{ex}"}

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
@app.get('/api/v1/get_container_links')# GET # allow all origins all methods.,response_model=StreamingLinkResponse)
async def get_container_links(_id:str):
    try:
        return {"streams":await caesaraird.get_container_links(_id)}
    except Exception as ex:
        return {"error":f"{type(ex)},{ex}"}
if __name__ == "__main__":
    uvicorn.run("main:app",port=8080,log_level="info")
