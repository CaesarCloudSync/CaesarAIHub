import json
import requests
import unittest
import sys

from CaesarAIConstants import CaesarAIConstants
from CaesarAITorrentParsers.CaesarAIJackett.responses.EpisodesResponse import EpisodesResponse
from CaesarAIRealDebird.responses.StatusAndProgressResponse import StatusAndProgressResponse
from CaesarAIRealDebird.responses.StreamingLinkResponse import StreamingLinkResponse
base_url = "http://localhost:8081/"

title = "Solo Leveling"
season = 1
episode = 12
api_key = "ZJ5LBOGWLSG4QLF7A5HSMGBJUOSIEXGH3BKLZAM2HV4TM7ACG4DA"
headers = {"Authorization": f"Bearer {api_key}"}

torrent_filname ="/home/amari/Desktop/CaesarAIHub/CaesarAIMovieStream/sampledata/Frieren Beyond the Journeys End S01E01-E04 1080p NF WEB-DL AAC2.0 H 264-VARYG (Sousou no Frieren, Multi-Subs).torrent"
class CaesarAIUnittest(unittest.TestCase):
    def test_get_streaming_link_torrent(self):

        magnet_link="https://nyaa.si/download/1936235.torrent"
        response = requests.post(f"{base_url}/api/v1/torrent_magnet",json={"torrent_link":magnet_link})
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
        


        


if __name__ == "__main__":
    unittest.main()