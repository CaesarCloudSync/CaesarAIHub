from pydantic import BaseModel

class StreamingLinkRequest(BaseModel):
    magnet_link:str