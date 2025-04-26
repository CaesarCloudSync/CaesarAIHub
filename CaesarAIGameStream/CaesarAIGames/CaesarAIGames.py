import requests
from CaesarAIGameConstants import CaesarAIGameConstants
from CaesarAIGames.models import CaesarAIGameRequests
class CaesarAIGames:
    def __init__(self):
        self.client_id = CaesarAIGameConstants.IGDB_CLIENT_ID
        self.client_secret = CaesarAIGameConstants.IGDB_CLIENT_SECRET
        self.access_token = None
    # Step 1: Get OAuth Token
    def get_igdb_token(self):
        url = 'https://id.twitch.tv/oauth2/token'
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials'
        }
        response = requests.post(url, data=params)
        response.raise_for_status()
        self.access_token = response.json()['access_token']
        return self.access_token

    # Step 2: Search for a game
    def search_game(self,game_name:str): 
        url = 'https://api.igdb.com/v4/games'
        headers = {
            'Client-ID': self.client_id,
            'Authorization': f'Bearer {self.access_token}',
        }
        query = CaesarAIGameRequests.search_query.format(game_name=game_name)
        response = requests.post(url, headers=headers, data=query)
        response.raise_for_status()
        return CaesarAIGameRequests.search_response.model_validate({"games":response.json()})
if __name__ == "__main__":
    pass