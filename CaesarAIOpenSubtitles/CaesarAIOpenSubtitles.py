import requests
class CaesarAIOpenSubtitles:
    def __init__(self) -> None:
        self.api_key = "2GVVw07GFNwoqqYXEGzHRo5FQsa7pTQv"
        self.base_url = "https://api.opensubtitles.com/"
        self.headers = {
            "User-Agent": "",
            "Api-Key": self.api_key
        }

    def get_subtitle_ids(self):
        querystring = {"imdb_id":"tt22248376","episode_number":"1"}
        response = requests.get(f"{self.base_url}/api/v1/subtitles" , headers=self.headers, params=querystring)
        return response.json()

print()