from pydantic import BaseModel
from typing import List
from CaesarAITorrentParsers.models.TorrentItem import TorrentItem
class EpisodesResponse(BaseModel):
    episodes:List[TorrentItem]