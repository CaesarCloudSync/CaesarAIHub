import requests
import httpx
import asyncio
from typing import Union
from CaesarAIRealDebird.models.StreamItem import StreamItem
from CaesarAIRealDebird.responses.StatusAndProgressResponse import StatusAndProgressResponse
class CaesarAIRealDebrid:
    def __init__(self) -> None:
        self.url="https://api.real-debrid.com/rest/1.0/"
        self.api_key = "ZJ5LBOGWLSG4QLF7A5HSMGBJUOSIEXGH3BKLZAM2HV4TM7ACG4DA"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def add_magnet(self,magnet:str) -> Union[str,None]:
        d = {'magnet':magnet}
        response = requests.post(f"{self.url}/torrents/addMagnet", data=d,headers=self.headers)
        if response.status_code == 201:
            return response.json()["id"]
        else:
            return None
    def get_torrent_info(self,_id):
        response = requests.get(f"{self.url}/torrents/info/{_id}",headers=self.headers)
        return response.json()
    
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
                return StreamItem.model_validate(response.json())
            else:
                return response.status_code
    async def get_streaming_links(self,_id):
        tasks = [self.unrestrict_link(url) for url in self.get_restricted_links(_id)]
        return await asyncio.gather(*tasks)
    def select_files(self,_id) -> Union[str,None]:
        response = requests.post(f"{self.url}/torrents/selectFiles/{_id}", data={"files":"all"},headers=self.headers)
        if response.status_code == 200:
            return True
        else:
            return False





