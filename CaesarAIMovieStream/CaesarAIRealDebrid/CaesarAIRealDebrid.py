import io
import requests
import httpx
import asyncio
from typing import Union
from CaesarAIConstants import CaesarAIConstants
from CaesarAIRealDebrid.models.ContainerStreamItem import ContainerStreamItem
from CaesarAIRealDebrid.models.StreamItem import StreamItem
from CaesarAIRealDebrid.responses.StatusAndProgressResponse import StatusAndProgressResponse
from CaesarAIRealDebrid.responses.StreamRealDebridResponse import StreamRealDebridResponse
class CaesarAIRealDebrid:
    def __init__(self) -> None:
        self.url="https://api.real-debrid.com/rest/1.0/"
        self.api_key = CaesarAIConstants.REALDEBRID_API_KEY
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def add_magnet(self,magnet:str) -> Union[str,None]:
        d = {'magnet':magnet}

        response = requests.post(f"{self.url}/torrents/addMagnet", data=d,headers=self.headers)

        if response.status_code == 201:
            return response.json()["id"]
        else:
            return None
    def add_torrent(self,torrent_link:str) -> Union[str,None]:
        response = requests.get(torrent_link)

        # Convert response.content (bytes) to a BufferedReader
        buffered_reader = io.BufferedReader(io.BytesIO(response.content))
        
        response = requests.put("https://api.real-debrid.com/rest/1.0/torrents/addTorrent", headers=self.headers, data=buffered_reader)
        if response.status_code == 201:
            return response.json()["id"]
        else:
            return None
    def get_torrent_info(self,_id):
        response = requests.get(f"{self.url}/torrents/info/{_id}",headers=self.headers)
        return response.json()
    

    async def get_streaming_info(self,containeritem:ContainerStreamItem) -> StreamRealDebridResponse:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.url}/streaming/mediaInfos/{containeritem.id}", headers=self.headers)
            if response.status_code == 200:
                #print(response.json())
                return response.json() # StreamRealDebridResponse.model_validate()
                
            else:
                return response.status_code

    
    def get_progress_and_status(self,_id) -> StatusAndProgressResponse:
        torrentinfo = self.get_torrent_info(_id) # May have to store id in a supabase redis instance to track progress.
        return {"id":_id,"status":torrentinfo.get("status"),"progress":torrentinfo.get("progress")}
    
    def get_restricted_links(self,_id):
        return self.get_torrent_info(_id)["links"]
    async def unrestrict_link(self,link:str):
        headers = dict()
        headers["Authorization"] = self.headers["Authorization"]
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.url}/unrestrict/link", headers=headers, data={"link":link})
            if response.status_code == 200:
                return ContainerStreamItem.model_validate(response.json())
            else:
                return response.status_code


    async def get_streaming_links(self,_id):
        tasks = [self.get_streaming_info(await self.unrestrict_link(url) )for url in self.get_restricted_links(_id)]
        return await asyncio.gather(*tasks)
    async def get_container_links(self,_id):
        tasks = [self.unrestrict_link(url) for url in self.get_restricted_links(_id)]
        return await asyncio.gather(*tasks)
    def select_files(self,_id) -> Union[str,None]:
        response = requests.post(f"{self.url}/torrents/selectFiles/{_id}", data={"files":"all"},headers=self.headers)
        if response.status_code == 200:
            return True
        else:
            return False





