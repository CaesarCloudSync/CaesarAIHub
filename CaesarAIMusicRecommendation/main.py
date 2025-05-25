import re

import uvicorn
import subprocess
from fastapi import FastAPI,Query, File, UploadFile
from typing import Dict,List,Any,Union
from fastapi.responses import StreamingResponse,JSONResponse
from fastapi import WebSocket,WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from models import MusicRecommendations,SetupBrowser
from CaesarAIMusicStreamRecommendation import CaesarAIMusicStreamRecommendation
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




@app.get('/')# GET # allow all origins all methods.
async def index():
    return "Welcome to CaesarAIMusicStreamYT."
@app.get('/healthcheck')# GET # allow all origins all methods.
async def healthcheck():
    return {"status":"OK"}
@app.get('/api/v1/get_recommendation',response_model=MusicRecommendations)# GET # allow all origins all methods.
async def get_recommendation(song_query:str,playlist_name:str="",max_songs:int=150,description:str="",backup:bool=False):
    try:
        cmsr = CaesarAIMusicStreamRecommendation()
        recommendations = cmsr.get_similiar_songs_from_song_with_seeds(song_query,playlist_name,max_songs,description,backup)
        return recommendations
    except Exception as ex:
        return {"error":f"{type(ex)},{ex}"}
@app.post("/api/v1/setup_browser_oauth",description="This browser header normally lasts for 2 years but if it expires follow. https://ytmusicapi.readthedocs.io/en/stable/setup/browser.html#copy-authentication-headers. Get the raw header from the music.youtube.com page then put it into headers raw and it will all sort itself out. No more configuration.")
async def setup_browser(file: UploadFile = File(...)):
    try:
        # Check if the file is a text file (optional)
        if not file.filename.endswith(('.txt', '.log')):
            return JSONResponse(status_code=400, content={"error": "Please upload a text file"})
        
        # Read the file contents
        content = await file.read()
        text_content = content.decode('utf-8')  # Decode bytes to string
        CaesarAIMusicStreamRecommendation.setup_browser(text_content)
        return {"status":"success"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Failed to read file: {str(e)}"})
    finally:
        await file.close()  # Ensure the file is closed




if __name__ == "__main__":
    uvicorn.run("main:app",port=8080,log_level="info")
    #uvicorn.run()
    #asyncio.run(main())