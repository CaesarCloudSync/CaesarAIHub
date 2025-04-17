from pydantic import BaseModel
from typing import Optional,List
class Cover(BaseModel):
    id: int
    url: str


class Genre(BaseModel):
    id: int
    name: str


class Game(BaseModel):
    id: int
    cover: Optional[Cover] = []
    first_release_date: Optional[int] = None
    genres: Optional[List[Genre]] = []
    name: str
    rating: Optional[float] = None
    summary: Optional[str] = None


class CaesarAISearchResponse(BaseModel):
    games:List[Game]

class CaesarAIGameRequests:
    search_query:Optional[str] =  '''
            search "{game_name}";
            fields name, summary, first_release_date, rating, genres.name, cover.url;
            limit 100;
        '''
    search_response: Optional[CaesarAISearchResponse] = CaesarAISearchResponse