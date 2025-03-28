from pydantic import BaseModel

class StatusAndProgressResponse(BaseModel):
    id:str
    status:str
    progress:int