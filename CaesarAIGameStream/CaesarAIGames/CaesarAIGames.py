import requests
from CaesarAIGameConstants import CaesarAIGameConstants
from CaesarAIGames.models import CaesarAIGameRequests
from CaesarAIGames.models.CaesarAIGameResponse import CaesarAISearchResponse
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
    # Step 1: Get genre ID by name
    def get_genre_id(self,genre_name):
        url = 'https://api.igdb.com/v4/genres'
        headers = {
            'Client-ID': self.client_id,
            'Authorization': f'Bearer {self.access_token}',
        }
        if genre_name not in CaesarAIGameRequests.genres:
            raise ValueError(f"Genre '{genre_name}' not found in predefined genres")
        else:
            query = f'fields id,name; where name = "{genre_name}";'
            response = requests.post(url, headers=headers, data=query)
            response.raise_for_status()
            genres = response.json()
            if genres:
                return genres[0]['id']
            else:
                raise ValueError(f"Genre '{genre_name}' not found")

    # Step 2: Search for a game
    def search_game(self,game_name:str,offset:int=0,limit:int=10):
        if self.access_token is None:
            raise ValueError("Access token is not set. Call get_igdb_token() first.") 
        url = 'https://api.igdb.com/v4/games'
        headers = {
            'Client-ID': self.client_id,
            'Authorization': f'Bearer {self.access_token}',
        }
        query = CaesarAIGameRequests.get_search_query(game_name,offset=offset,limit=limit)
        response = requests.post(url, headers=headers, data=query)
        response.raise_for_status()
        return CaesarAISearchResponse.model_validate({"games":response.json()})
    def get_popular_games(self,offset:int=0,limit:int=10,genre=None):
        url = 'https://api.igdb.com/v4/games'
        headers = {
            'Client-ID': self.client_id,
            'Authorization': f'Bearer {self.access_token}',
        }
        
        genre_id = self.get_genre_id(genre) if genre else None
        query = CaesarAIGameRequests.get_popular_query(offset=offset,limit=limit,genre=genre_id)
        response = requests.post(url, headers=headers, data=query)
        response.raise_for_status()
        return CaesarAISearchResponse.model_validate({"games":response.json()})
