from pydantic import  BaseModel,computed_field,root_validator,field_validator
from typing import List,Optional,Union
import PTN
import re
from CaesarAIConstants import CaesarAIConstants
from CaesarAIUtils import CaesarAIUtils
class TorrentItem(BaseModel):
    query:str
    title: str
    guid: str
    pub_date: Optional[str] = None
    size: int
    magnet_link: Optional[str] = None
    torrent_link: Optional[str] = None
    categories: Union[Optional[List[int]],str]
    seeders: int
    peers: Optional[int] = None
    indexer:Optional[str] = None
    service:str
    @field_validator("query")
    @classmethod
    def sanitize_query(cls, value):
        value = CaesarAIUtils.sanitize_text(value)
        return value
 
    
    @root_validator(pre=True)
    def validate_links(cls, values):
        magnet_link = values.get("magnet_link")
        torrent_link = values.get("torrent_link")

        if not magnet_link and not torrent_link:
            raise ValueError("Either 'magnet_link' or 'torrent_link' must be provided.")
        return values

    @staticmethod
    def format_season_episode(season:Union[str,List[str]], episode:Union[str,List[str]]):
        if season and episode:
            season =f"S{int(season[0]):02}~S{int(season[-1]):02}" if type(season) == list else f"S{int(season):02}"
            episode = f"E{int(episode[0]):02}~E{int(episode[-1]):02}" if type(episode) == list else f"E{int(episode):02}"
            return f"{season}{episode}"
        else:
            return None
    @computed_field
    @property
    def dual_audio(self) -> Optional[Union[str,List[str]]]:
        """Extracts 'Dual Audio' if present, otherwise None."""
        pattern = re.search(r'\b(Dual Audio|Dual-Audio|Multi-Audio|Eng\+Jap|Eng\+Fre|DUAL-A|DA)\b', self.title, re.IGNORECASE)
        return pattern.group(1) if pattern else None  # Return matched value or None
    @computed_field
    @property
    def displayname(self) -> Optional[str]:
        if self.episode != "BATCH" and self.season != "BATCH":
            format_se = self.format_season_episode(self.season,self.episode) if (self.episode and self.season) else ""
        else:
            format_se = "BATCH"
        resolution = self.resolution if self.resolution else ""
        dual_audio = self.dual_audio if self.dual_audio else ""
        return f"{self.name} {format_se} {resolution} {dual_audio}".strip()
    @computed_field
    @property
    def name(self) -> Optional[str]:
        info = PTN.parse(self.title)
        
        return info.get("title") if info.get("title") else None
    @computed_field
    @property
    def season(self) -> Optional[Union[int,str,List[str]]]:
        info = PTN.parse(self.title)
        return info.get("season") if info.get("season") else "BATCH"
    @computed_field
    @property
    def episode(self) -> Optional[Union[int,str,List[int]]]:
        info = PTN.parse(self.title)
        return info.get("episode") if info.get("episode") else "BATCH"
    @computed_field
    @property
    def resolution(self) -> Optional[str]:
        info = PTN.parse(self.title)
        return info.get("resolution")
    @computed_field
    @property
    def languages(self) -> Optional[Union[List[str],str]]:
        info = PTN.parse(self.title)
        return info.get("language")
    @computed_field
    @property
    def subtitles(self) -> Optional[Union[List[str],str]]:
        info = PTN.parse(self.title)
        return info.get("subtitles")
    @computed_field
    @property
    def is_multi_audio(self) -> bool:
        """Detects if the torrent contains dual audio."""
        dual_audio_patterns = [
            r'\bDual Audio\b',
            r'\bDual\b',
            r'\bMulti-Audio\b',
            r'\bEng\+Jap\b',
            r'\bEng\+Fre\b',  # Add more languages if needed
            r'\bDUAL-A\b',
            r'\bDA\b'
        ]
        return any(re.search(pattern, self.title, re.IGNORECASE) for pattern in dual_audio_patterns)
 