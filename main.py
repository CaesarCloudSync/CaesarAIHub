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
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


caesaraird = CaesarAIRealDebrid()

@app.get('/')# GET # allow all origins all methods.
async def index():
    return "Welcome to CaesarAIMovieStream."
@app.get('/healthcheck')# GET # allow all origins all methods.
async def healthcheck():
    return {"status":"OK"}
@app.get('/api/v1/get_single_episodes',response_model=EpisodesResponse)# GET # allow all origins all methods.
async def get_single_episodes(title:str,season:int,episode:int,service:Optional[str]=None):
    try:
        if not service or "jackett":
            url = f"{CaesarAIConstants.BASE_JACKETT_URL}?apikey={CaesarAIConstants.JACKETT_API_KEY}&t={CaesarAIConstants.ENDPOINT}&q={title}&season={season}&ep={episode}"
            caejackett = CaesarAIJackett(url)
            torrentinfo = caejackett.get_torrent_info()
            torrentinfo = caejackett.get_single_episodes()
        else:
            url = f"{CaesarAIConstants.BASE_PROWLER_URL}?apikey={CaesarAIConstants.PROWLARR_API_KEY}&query={title} {CaesarAIProwlarr.format_season_episode(season,episode)}"
            caeprowlarr = CaesarAIProwlarr(url)
            torrentinfo = caeprowlarr.get_torrent_info()
            torrentinfo = caeprowlarr.get_single_episodes()

        return {"episodes":torrentinfo}
    except Exception as ex:
        return {"error":f"{type(ex)},{ex}"}
@app.get('/api/v1/get_batch_episodes',response_model=EpisodesResponse)# GET # allow all origins all methods.
async def get_batch_episodes(title:str,season:int,service:Optional[str]=None):
    try:
        if not service or "jackett":
            url = f"{CaesarAIConstants.BASE_JACKETT_URL}?apikey={CaesarAIConstants.JACKETT_API_KEY}&t={CaesarAIConstants.ENDPOINT}&q={title}&season={season}"
            caejackett = CaesarAIJackett(url)
            torrentinfo = caejackett.get_torrent_info()
            torrentinfo = caejackett.get_batch_episodes()
        else:
            url = f"{CaesarAIConstants.BASE_PROWLER_URL}?apikey={CaesarAIConstants.PROWLARR_API_KEY}&query={title} {CaesarAIProwlarr.format_season(season)}"
            caeprowlarr = CaesarAIProwlarr(url)
            torrentinfo = caeprowlarr.get_torrent_info()
            torrentinfo = caeprowlarr.get_batch_episodes()

        return {"episodes":torrentinfo}
    except Exception as ex:
        return {"error":f"{type(ex)},{ex}"}
@app.get('/api/v1/get_single_and_batched_episodes',response_model=EpisodesResponse)# GET # allow all origins all methods.
async def get_single_and_batched_episodes(title:str,season:int,episode:int,service:Optional[str]=None):
    try:
        if not service or "jackett":
            url = f"{CaesarAIConstants.BASE_JACKETT_URL}?apikey={CaesarAIConstants.JACKETT_API_KEY}&t={CaesarAIConstants.ENDPOINT}&q={title}&season={season}"
            caejackett = CaesarAIJackett(url)
            torrentinfo_single = caejackett.get_single_episodes()
            torrentinfo_batched = caejackett.get_batch_episodes()
            
            torrentinfo = torrentinfo_single + torrentinfo_batched
            return {"episodes":torrentinfo}
        else:
            url = f"{CaesarAIConstants.BASE_PROWLER_URL}?apikey={CaesarAIConstants.PROWLARR_API_KEY}&query={title} {CaesarAIProwlarr.format_season(season)}"
            caeprowlarr = CaesarAIProwlarr(url)
            torrentinfo_single = caeprowlarr.get_single_episodes()
            torrentinfo_batched = caeprowlarr.get_batch_episodes()
            
            torrentinfo = torrentinfo_single + torrentinfo_batched
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


@app.get('/api/v1/get_streaming_link',response_model=StreamingLinkResponse)# GET # allow all origins all methods.
async def get_streaming_links(_id:str):
    try:
        return {"streams":await caesaraird.get_streaming_links(_id)}
    except Exception as ex:
        return {"error":f"{type(ex)},{ex}"}
if __name__ == "__main__":
    uvicorn.run("main:app",port=8080,log_level="info")
