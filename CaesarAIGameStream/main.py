import re
import uvicorn
import subprocess
from fastapi import FastAPI,Query
from typing import Dict,List,Any,Union
from fastapi.responses import StreamingResponse
from fastapi import WebSocket,WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from CaesarAIGames import CaesarAIGames
from CaesarAIGames.models.CaesarAIGameResponse import CaesarAISearchResponse

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



caesaraigames = CaesarAIGames()
caesaraigames.get_igdb_token()# get the token from igdb

@app.get('/')# GET # allow all origins all methods.
async def index():
    return "Welcome to CaesarAIGameStream"
@app.get('/api/v1/search_game',response_model=CaesarAISearchResponse)# GET # allow all origins all methods.
async def search_game(game:str,offset:int=0,limit:int=10):
    return caesaraigames.search_game(game,offset=offset,limit=limit)
@app.get('/api/v1/popular_games',response_model=CaesarAISearchResponse)# GET # allow all origins all methods.
async def popular_games(offset:int=0,limit:int=10,genre:str=None):
    print(genre)
    return caesaraigames.get_popular_games(offset,limit,genre)
@app.get('/healthcheck')# GET # allow all origins all methods.
async def healthcheck():
    return {"status":"OK"}

if __name__ == "__main__":
    uvicorn.run("main:app",port=8080,log_level="info")
    #uvicorn.run()
    #asyncio.run(main())