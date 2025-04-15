from typing import Optional, Dict, List,Union
from pydantic import BaseModel,computed_field
import PTN

class VideoStream(BaseModel):
    stream: str
    lang: str
    lang_iso: str
    codec: str
    colorspace: str
    width: int
    height: int


class AudioStream(BaseModel):
    stream: str
    lang: str
    lang_iso: str
    codec: str
    sampling: int
    channels: int


class SubtitleStream(BaseModel):
    stream: str
    lang: str
    lang_iso: str
    type: str


class StreamDetails(BaseModel):
    video: Dict[str, VideoStream]
    audio: Dict[str, AudioStream]
    subtitles: Union[Dict[str, SubtitleStream],List] = []


class StreamItem(BaseModel):
    filename: str
    hoster: str
    link: str
    type: str
    @computed_field
    @property
    def season(self) -> Optional[Union[int]]:
        info = PTN.parse(self.filename)
        return info.get("season") if info.get("season") else None
    @computed_field
    @property
    def episode(self) -> Optional[Union[int]]:
        info = PTN.parse(self.filename)
        return info.get("episode") if info.get("episode") else None
    year: Optional[int]
    duration: float
    bitrate: int
    size: int
    details: StreamDetails
    baseUrl: str
    availableFormats: Dict[str, str]
    availableQualities: Dict[str, str]
    modelUrl: str
    host: str



#class StreamResponse(BaseModel):
#    streams: List[Stream]
