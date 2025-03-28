import re
import requests
import uvicorn
from typing import Union,Any,Dict,List
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


JSONObject = Dict[Any, Any]
JSONArray = List[Any]
JSONStructure = Union[JSONArray, JSONObject]

@app.get('/{service}/{port}/{sub_path:path}')# GET # allow all origins all methods.
async def index(service:str,port:int,sub_path: str, request: Request):
    new_url = f"http://{service}:{port}/{sub_path}"
    if request.query_params:
        query_string = dict(request.query_params)  # Get all query parameters
    else:
        query_string = None
    print(new_url)
    return requests.get(new_url,params=query_string).json()

@app.post('/{service}/{port}/{sub_path:path}')# GET # allow all origins all methods.
async def index(service:str,port:int,sub_path: str, data: JSONStructure):
    new_url = f"http://{service}:{port}/{sub_path}"
    new_json = data if data else None
    return requests.post(new_url,json=new_json).json()


@app.get('/healthcheck')# GET # allow all origins all methods.
async def healthcheck():
    try:
        return {"status":"OK"}
    except Exception as ex:
        return {"error":f"{type(ex)},{ex}"}



if __name__ == "__main__":
    uvicorn.run("main:app",port=8000,log_level="info")
    #uvicorn.run()
    #asyncio.run(main())