import os
from enum import Enum
from pydantic import BaseModel



class CaesarAIGameConstants:
    IGDB_CLIENT_ID=os.environ.get("IGDB_CLIENT_ID")
    IGDB_CLIENT_SECRET=os.environ.get("IGDB_CLIENT_SECRET")