import os
from CaesarAIGames import CaesarAIGames

from dotenv import load_dotenv
load_dotenv(".env")
if __name__ == "__main__":
    cgm = CaesarAIGames()
    cgm.client_id = os.environ.get("IGDB_CLIENT_ID")
    cgm.client_secret = os.environ.get("IGDB_CLIENT_SECRET")
    cgm.get_igdb_token()
  
    print(cgm.search_game("Call Of Duty").games)