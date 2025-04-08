from pydantic import BaseModel
from typing import Optional

class EpisodesRequest(BaseModel):
    title:str
    season:int
    episode:int
    