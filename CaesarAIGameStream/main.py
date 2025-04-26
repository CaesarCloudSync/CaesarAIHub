import re
import uvicorn
import subprocess
from fastapi import FastAPI,Query
from typing import Dict,List,Any,Union
from fastapi.responses import StreamingResponse
from fastapi import WebSocket,WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware


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
    return "Welcome to CaesarAIGameStream"
@app.get('/healthcheck')# GET # allow all origins all methods.
async def healthcheck():
    return {"status":"OK"}

if __name__ == "__main__":
    uvicorn.run("main:app",port=8080,log_level="info")
    #uvicorn.run()
    #asyncio.run(main())