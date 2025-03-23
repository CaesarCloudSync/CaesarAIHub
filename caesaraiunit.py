import json
import requests
import unittest
import sys
from CaesarAIJackett.responses.EpisodesResponse import EpisodesResponse
from CaesarAIRealDebird.responses.StatusAndProgressResponse import StatusAndProgressResponse
from CaesarAIRealDebird.responses.StreamingLinkResponse import StreamingLinkResponse
uri = "http://127.0.0.1:8081" #"https://blacktechdivisionreward-hrjw5cc7pa-uc.a.run.app"
title = "Solo Leveling"
season = 1
episode = 12

class CaesarAIUnittest(unittest.TestCase):
    def test_get_streaming_link(self):
        response = requests.get(f"{uri}/api/v1/get_single_episodes",params={"title":title,"season":season,"episode":episode})
        print(response.json())
        episodes = EpisodesResponse.model_validate(response.json())
        self.assertNotEqual(len(episodes.episodes),0)
        magnet_link = episodes.episodes[0].magnet_link
        response = requests.post(f"{uri}/api/v1/torrent_magnet",json={"magnet_link":magnet_link})
        status_and_progress = StatusAndProgressResponse.model_validate(response.json())
        self.assertNotEqual(status_and_progress.id,None)
        while status_and_progress.status != "downloaded":
            response = requests.get(f"{uri}/api/v1/check_torrent",params={"_id":status_and_progress.id})
            status_and_progress = StatusAndProgressResponse.model_validate(response.json())
            self.assertNotEqual(status_and_progress.id,None)
        response = requests.get(f"{uri}/api/v1/get_streaming_link",params={"_id":status_and_progress.id})
        streams = StreamingLinkResponse.model_validate(response.json())
        print(streams)
        
        


if __name__ == "__main__":
    unittest.main()