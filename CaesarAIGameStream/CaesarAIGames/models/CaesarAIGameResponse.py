from pydantic import BaseModel,computed_field
from typing import Optional,List
from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Union
from datetime import datetime
from enum import IntEnum

class Genre(BaseModel):
    name: Optional[str] = None

class Cover(BaseModel):
    image_id: Optional[str] = None
    @computed_field
    @property
    def url(self) -> Optional[str]:
        if self.image_id:
            return f"https://images.igdb.com/igdb/image/upload/t_cover_big/{self.image_id}.jpg"
        return None

class GameCategory(IntEnum):
    MAIN_GAME = 0
    DLC_ADDON = 1
    EXPANSION = 2
    BUNDLE = 3
    STANDALONE_EXPANSION = 4
    MOD = 5
    EPISODE = 6
    SEASON = 7
    REMAKE = 8
    REMASTER = 9
    EXPANDED_GAME = 10
    PORT = 11
    FORK = 12
    PACK = 13
    UPDATE = 14

class GameStatus(IntEnum):
    RELEASED = 0
    ALPHA = 2
    BETA = 3
    EARLY_ACCESS = 4
    OFFLINE = 5
    CANCELLED = 6
    RUMORED = 7
    DELISTED = 8

class Game(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    summary: Optional[str] = None
    first_release_date: Optional[datetime] = None
    rating: Optional[float] = None
    genres: Optional[List[Genre]] = None
    artworks: Optional[List[int]] = None
    bundles: Optional[List[int]] = None
    category: Optional[GameCategory] = None
    checksum: Optional[str] = None
    collection: Optional[int] = None
    collections: Optional[List[int]] = None
    cover: Optional[Cover] = None
    created_at: Optional[datetime] = None
    dlcs: Optional[List[int]] = None
    expanded_games: Optional[List[int]] = None
    expansions: Optional[List[int]] = None
    external_games: Optional[List[int]] = None
    follows: Optional[int] = None
    forks: Optional[List[int]] = None
    franchise: Optional[int] = None
    franchises: Optional[List[int]] = None
    game_engines: Optional[List[int]] = None
    game_localizations: Optional[List[int]] = None
    game_modes: Optional[List[int]] = None
    game_status: Optional[GameStatus] = None
    game_type: Optional[int] = None
    hypes: Optional[int] = None
    involved_companies: Optional[List[int]] = None
    keywords: Optional[List[int]] = None
    language_supports: Optional[List[int]] = None
    multiplayer_modes: Optional[List[int]] = None
    parent_game: Optional[int] = None
    platforms: Optional[List[int]] = None
    player_perspectives: Optional[List[int]] = None
    ports: Optional[List[int]] = None
    rating_count: Optional[int] = None
    release_dates: Optional[List[int]] = None
    remakes: Optional[List[int]] = None
    remasters: Optional[List[int]] = None
    screenshots: Optional[List[int]] = None
    similar_games: Optional[List[int]] = None
    slug: Optional[str] = None
    standalone_expansions: Optional[List[int]] = None
    status: Optional[int] = None
    storyline: Optional[str] = None
    tags: Optional[List[int]] = None
    themes: Optional[List[int]] = None
    total_rating: Optional[float] = None
    total_rating_count: Optional[int] = None
    updated_at: Optional[datetime] = None
    url: Optional[HttpUrl] = None
    version_parent: Optional[int] = None
    version_title: Optional[str] = None
    videos: Optional[List[int]] = None
    websites: Optional[List[int]] = None
class CaesarAISearchResponse(BaseModel):
    games:List[Game]
