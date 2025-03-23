from pydantic import  BaseModel,computed_field
from typing import List,Optional,Union
import PTN
import re
class TorrentItem(BaseModel):
    title: str
    guid: str
    pub_date: Optional[str] = None
    size: int
    magnet_link: str
    categories: Optional[List[int]]
    seeders: int
    peers: Optional[int] = None
    indexer:Optional[str] = None

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
        format_se = self.format_season_episode(self.season,self.episode) if self.episode and self.season else ""
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
    def season(self) -> Optional[Union[int,List[str]]]:
        info = PTN.parse(self.title)
        return info.get("season") if info.get("season") else None
    @computed_field
    @property
    def episode(self) -> Optional[Union[int,List[int]]]:
        info = PTN.parse(self.title)
        return info.get("episode") if info.get("episode") else None
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
 