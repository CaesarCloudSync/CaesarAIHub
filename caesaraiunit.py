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
    def test_real_debrid_torrent_file(self):

        with open(torrent_filname, 'rb') as file:
            request = requests.put("https://api.real-debrid.com/rest/1.0/torrents/addTorrent", headers=headers, data=file)


        #response = requests.get(url, headers=headers, files=files)
        print(request.status_code)

     


    def test_get_streaming_link(self):
        """response = requests.get(f"{base_url}/api/v1/get_single_episodes",params={"title":title,"season":season,"episode":episode})
        print(response.json())
        episodes = EpisodesResponse.model_validate(response.json())
        self.assertNotEqual(len(episodes.episodes),0)
        magnet_link = episodes.episodes[0].magnet_link
        print(magnet_link)
        """
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
        


        


if __name__ == "__main__":
    unittest.main()