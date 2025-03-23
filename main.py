import uvicorn
from fastapi import FastAPI
import requests
from fastapi.middleware.cors import CORSMiddleware
from CaesarAIJackett import CaesarAIJackett
from CaesarAIConstants import CaesarAIConstants
from CaesarAIJackett.responses.EpisodesResponse import EpisodesResponse
from CaesarAIRealDebird.requestmodels.StreamingLinkRequest import StreamingLinkRequest
from CaesarAIRealDebird import CaesarAIRealDebrid
from CaesarAIRealDebird.responses.StreamingLinkResponse import StreamingLinkResponse
from CaesarAIRealDebird.responses.StatusAndProgressResponse import StatusAndProgressResponse
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
    return "Welcome to CaesarAI Template. Hello"
@app.get('/api/v1/get_single_episodes',response_model=EpisodesResponse)# GET # allow all origins all methods.
async def get_single_episodes(title:str,season:int,episode:int):
    try:
        url = f"{CaesarAIConstants.BASE_JACKETT_URL}?apikey={CaesarAIConstants.JACKETT_API_KEY}&t={CaesarAIConstants.ENDPOINT}&q={title}&season={season}&ep={episode}"
        response = requests.get(url)
        caejackett = CaesarAIJackett(response.content)
        torrentinfo = caejackett.get_torrent_info()
        torrentinfo = caejackett.get_single_episodes()
        return {"episodes":torrentinfo}
    except Exception as ex:
        return {"error":f"{type(ex)},{ex}"}
@app.get('/api/v1/get_batch_episodes',response_model=EpisodesResponse)# GET # allow all origins all methods.
async def get_batch_episodes(title:str,season:int):
    try:
        url = f"{CaesarAIConstants.BASE_JACKETT_URL}?apikey={CaesarAIConstants.JACKETT_API_KEY}&t={CaesarAIConstants.ENDPOINT}&q={title}&season={season}"
        response = requests.get(url)
        caejackett = CaesarAIJackett(response.content)
        torrentinfo = caejackett.get_torrent_info()
        torrentinfo = caejackett.get_batch_episodes()
        return {"episodes":torrentinfo}
    except Exception as ex:
        return {"error":f"{type(ex)},{ex}"}
@app.get('/api/v1/get_single_and_batched_episodes',response_model=EpisodesResponse)# GET # allow all origins all methods.
async def get_single_and_batched_episodes(title:str,season:int,episode:int):
    try:
        url = f"{CaesarAIConstants.BASE_JACKETT_URL}?apikey={CaesarAIConstants.JACKETT_API_KEY}&t={CaesarAIConstants.ENDPOINT}&q={title}&season={season}&ep={episode}"
        response = requests.get(url)
        caejackett = CaesarAIJackett(response.content)
        torrentinfo = caejackett.get_torrent_info()
        torrentinfo_single = caejackett.get_single_episodes()
        torrentinfo_batched = caejackett.get_batch_episodes()
        
        torrentinfo = torrentinfo_single + torrentinfo_batched
        return {"episodes":torrentinfo}
    except Exception as ex:
        return {"error":f"{type(ex)},{ex}"}
@app.post('/api/v1/torrent_magnet',response_model=StatusAndProgressResponse)# GET # allow all origins all methods.
async def torrent_magnet(magnetdata:StreamingLinkRequest):
    try:
        magnet_link = magnetdata.magnet_link
        _id = caesaraird.add_magnet(magnet_link)
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
