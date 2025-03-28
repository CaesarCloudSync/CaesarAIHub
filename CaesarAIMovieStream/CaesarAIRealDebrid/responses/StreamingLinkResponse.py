from typing import List
from pydantic import BaseModel
from CaesarAIRealDebrid.models.ContainerStreamItem import ContainerStreamItem
class StreamingLinkResponse(BaseModel):
    streams : List[ContainerStreamItem]