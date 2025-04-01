from typing import List
from pydantic import BaseModel
from CaesarAIRealDebrid.models.ContainerStreamItem import ContainerStreamItem
from CaesarAIRealDebrid.responses.StreamRealDebridResponse import StreamRealDebridResponse
class StreamingLinkResponse(BaseModel):
    streams : List[StreamRealDebridResponse]