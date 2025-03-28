import json
import requests
import unittest
import sys

base_url_movies = "http://localhost:8081" #"https://blacktechdivisionreward-hrjw5cc7pa-uc.a.run.app"
base_url_music = "https://music.caesaraihub.org"
class CaesarAIUnittest(unittest.TestCase):
    def test_music_stream(self):

        url = f"{base_url_music}/getaudio"
        response = requests.get(url,params={"url":"https://www.youtube.com/watch?v=sSudJNPsxAc"})
        print(response.json())
    def test_movie_stream(self):
        url = f"{base_url_movies}/api/v1/get_single_episodes"
        response = requests.get(url,params={"title":"Solo Leveling","season":1,"episode":1})
        print(response.json())



if __name__ == "__main__":
    unittest.main()