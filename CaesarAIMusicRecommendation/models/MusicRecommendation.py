from pydantic import BaseModel, model_validator
from typing import List, Optional

class Thumbnail(BaseModel):
    url: str
    width: int
    height: int

class FeedbackTokens(BaseModel):
    add: str
    remove: str

class Artist(BaseModel):
    name: str
    id: Optional[str]

class Album(BaseModel):
    name: str
    id: str

class MusicRecommendation(BaseModel):
    videoId: str
    title: str
    length: str
    thumbnail: List[Thumbnail]
    feedbackTokens: FeedbackTokens
    likeStatus: str
    inLibrary: bool
    videoType: str
    artists: List[Artist]
    album: Album
    year: Optional[str] = None
    views: Optional[str] = None

class MusicRecommendations(BaseModel):
    music: List[MusicRecommendation]
    @model_validator(mode="before")
    def filter_tracks_with_missing_album_or_artists(cls, values):
        # Get the 'music' list from the input values
        music_list = values.get('music', [])
        # Filter out items where 'album' or 'artists' is missing or None
        filtered_music = [
            track for track in music_list
            if isinstance(track, dict) 
            and 'album' in track and track['album'] is not None
            and 'artists' in track and track['artists'] is not None
        ]
        # Update the 'music' list with filtered items
        values['music'] = filtered_music
        return values