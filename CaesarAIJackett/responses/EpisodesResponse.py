from pydantic import BaseModel
from typing import List
from CaesarAIJackett.models.TorrentItem import TorrentItem
class EpisodesResponse(BaseModel):
    episodes:List[TorrentItem]