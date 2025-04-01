from typing import Dict, Optional, List
from pydantic import BaseModel, HttpUrl
class AudioStreamInfo(BaseModel):
    stream:str
    lang:str
    lang_iso:str
    codex:str
    sampling:int
    channels:int
      
class VideoStreamInfo(BaseModel):
    stream:str
    lang:str
    lang_iso:str
    codec:str
    colorspace:str
    width:int
    height:int
      
class SubtitleStreamInfo(BaseModel):
    stream:str
    lang:str
    lang_iso:str
    type:str

class Details(BaseModel):
    video: Dict[str, VideoStreamInfo]
    audio: Dict[str, AudioStreamInfo]
    subtitles: Dict[str, SubtitleStreamInfo]

class StreamRealDebridResponse(BaseModel):
    filename: str
    hoster: str
    link: HttpUrl
    type: str
    season: str
    episode: str
    year: Optional[int]
    duration: float
    bitrate: int
    size: int
    details: Details
    poster_path: HttpUrl
    backdrop_path: HttpUrl
    baseUrl: HttpUrl
    availableFormats: Dict[str, str]
    availableQualities: Dict[str, str]
    modelUrl: str
    host: str

   
