from pydantic import BaseModel
from CaesarAIGames.models.CaesarAIGameResponse import CaesarAISearchResponse
from pydantic import BaseModel
from typing import ClassVar, Optional
from dataclasses import dataclass  # Assuming CaesarAISearchResponse is a dataclass or similar

# Placeholder for CaesarAISearchResponse (replace with actual definition)
@dataclass
class CaesarAISearchResponse:
    data: list  # Simplified for example; replace with actual fields

class CaesarAIGameRequests(BaseModel):
    field: ClassVar[str] = """name,summary,first_release_date,rating,genres.name,artworks,bundles,category,checksum,collection,collections,cover.image_id,created_at,dlcs,expanded_games,expansions,external_games,first_release_date,follows,forks,franchise,franchises,game_engines,game_localizations,game_modes,game_status,game_type,genres,hypes,involved_companies,keywords,language_supports,multiplayer_modes,name,parent_game,platforms,player_perspectives,ports,rating,rating_count,release_dates,remakes,remasters,screenshots,similar_games,slug,standalone_expansions,status,storyline,summary,tags,themes,total_rating,total_rating_count,updated_at,url,version_parent,version_title,videos,websites"""
    genres : ClassVar[str] = [
    "Pinball",
    "Adventure",
    "Indie",
    "Arcade",
    "Visual Novel",
    "Card & Board Game",
    "MOBA",
    "Point-and-click",
    "Fighting",
    "Shooter",
    "Music",
    "Platform",
    "Puzzle",
    "Racing",
    "Real Time Strategy (RTS)",
    "Role-playing (RPG)",
    "Simulator",
    "Sport",
    "Strategy",
    "Turn-based strategy (TBS)",
    "Tactical",
    "Hack and slash/Beat 'em up",
    "Quiz/Trivia"
    ]

    search_response: Optional[CaesarAISearchResponse] = None  # Use None as default

    @classmethod
    def get_search_query(cls,game_name: str,offset:int = 0,limit:int = 0) -> str:
        """Generate the search query string using the game name."""
        return f'''
            search "{game_name}";
            fields {cls.field};
            limit {limit};
            offset {offset};
        '''.strip()
    
    popular_response: Optional[CaesarAISearchResponse] = None  # Use None as default
    @classmethod
    def get_popular_query(cls,offset:int = 0,limit:int = 0,genre=None) -> str:
        """Generate the popular query string using the field ClassVar."""
        if genre:
            return f'''
                fields {cls.field};
                limit {limit};
                offset {offset};
                sort rating desc;
                sort total_rating_count desc;
                where genres.id = "{genre}";
            '''.strip() # where total_rating_count > 500;
        else:
            return f'''
                fields {cls.field};
                limit {limit};
                offset {offset};
                sort rating desc;
                sort total_rating_count desc;
            '''.strip() # where total_rating_count > 500;
        return 