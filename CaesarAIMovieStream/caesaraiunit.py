import os
import json
import requests
import unittest
import sys
"""
from CaesarAIConstants import CaesarAIConstants
from CaesarAITorrentParsers.CaesarAIJackett.responses.EpisodesResponse import EpisodesResponse
from CaesarAIRealDebrid.responses.StatusAndProgressResponse import StatusAndProgressResponse
from CaesarAIRealDebrid.responses.StreamingLinkResponse import StreamingLinkResponse
"""
import asyncio
import websockets
base_url = "http://localhost:8082"

title = "Solo Leveling"
season = 1
episode = 12


class CaesarAIUnittest(unittest.TestCase):
    def test_get_episodesws(self):
        import asyncio
        from websockets.asyncio.client import connect


        async def hello():
            async with connect("ws://localhost:8082/api/v1/stream_get_episodews") as websocket:
                await websocket.send(json.dumps({"title":"Solo Leveling","season":1,"episode":1}))
                while True:
                    data = json.loads(await websocket.recv())
                    print(data)


        asyncio.run(hello())
        
    def test_get_indexer_names(self):
        pass

"""       
    def test_get_streaming_link_magnet(self):

        magnet_link="magnet:?xt=urn:btih:77bc04c4b0f18ec007aac33f3ea89ba0dd22dfd5&dn=%5BToonsHub%5D%20Dragon%20Ball%20DAIMA%20S01E06%201080p%20AMZN%20WEB-DL%20DDP2.0%20H.264%20%28Dual-Audio%2C%20English-Sub%29&tr=http%3A%2F%2Fnyaa.tracker.wf%3A7777%2Fannounce&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Fexodus.desync.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce"
        response = requests.post(f"{base_url}/api/v1/torrent_magnet",json={"magnet_link":magnet_link})
        status_and_progress = StatusAndProgressResponse.model_validate(response.json())
        print(response.content)
        self.assertNotEqual(status_and_progress.id,None)
        while status_and_progress.status != "downloaded":
            response = requests.get(f"{base_url}/api/v1/check_torrent",params={"_id":status_and_progress.id})
            status_and_progress = StatusAndProgressResponse.model_validate(response.json())
            print(status_and_progress)
            self.assertNotEqual(status_and_progress.id,None)
        response = requests.get(f"{base_url}/api/v1/get_streaming_link",params={"_id":status_and_progress.id})
        streams = StreamingLinkResponse.model_validate(response.json())
        print(streams)
        


        
"""

if __name__ == "__main__":
    unittest.main()