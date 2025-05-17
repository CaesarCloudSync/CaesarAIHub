from pydantic import BaseModel
from typing import Optional

class MoviesRequest(BaseModel):
    title:str

    