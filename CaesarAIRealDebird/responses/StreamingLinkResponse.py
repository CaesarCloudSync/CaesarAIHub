from typing import List
from pydantic import BaseModel
from CaesarAIRealDebird.models.StreamItem import StreamItem
class StreamingLinkResponse(BaseModel):
    streams : List[StreamItem]