from pydantic import  BaseModel,computed_field
from typing import List,Optional,Union
import PTN
from pathlib import Path
import re
class StreamItem(BaseModel):
    id:str
    filename:str
    download:str
    streamable:int
    mimeType:str
    filesize:int
    link:str
    host:str
    host_icon:str
    chunks:int
    crc:int
    
    @staticmethod
    def format_season_episode(season:str, episode:str):
        if season and episode:
            season =f"S{int(season[0]):02}~S{int(season[-1]):02}" if type(season) == list else f"S{int(season):02}"
            episode = f"E{int(episode[0]):02}~E{int(episode[-1]):02}" if type(episode) == list else f"E{int(episode):02}"
            return f"{season}{episode}"
        else:
            return None
    @computed_field
    @property
    def title(self) -> Optional[str]:
        return Path(self.filename).stem
    @computed_field
    @property
    def dual_audio(self) -> Optional[str]:
        """Extracts 'Dual Audio' if present, otherwise None."""
        pattern = re.search(r'\b(Dual Audio|Dual-Audio|Multi-Audio|Eng\+Jap|Eng\+Fre|DUAL-A|DA)\b', self.title, re.IGNORECASE)
        return pattern.group(1) if pattern else None  # Return matched value or None
    @computed_field
    @property
    def displayname(self) -> Optional[str]:
        format_se = self.format_season_episode(self.season,self.episode) if self.episode and self.season else ""
        resolution = self.resolution if self.resolution else ""
        dual_audio = self.dual_audio if self.dual_audio else ""
        return f"{self.title} {format_se} {resolution} {dual_audio}".strip()
    @computed_field
    @property
    def name(self) -> Optional[str]:
        info = PTN.parse(Path(self.title).stem)
        return info.get("title")  if info.get("title") else None
    @computed_field
    @property
    def season(self) -> Optional[Union[int,List]]:
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
    def subtitles(self) -> Optional[str]:
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
{'id': 'SM6ZDMBUWN44M', 'filename': '[LostYears] Solo Leveling - S01E07 (WEB 1080p x264 AAC) [20D3399B].mkv', 'mimeType': 'video/x-matroska', 'filesize': 1484963443, 'link': 'https://real-debrid.com/d/6PN22A3T6UPTA9D2', 'host': 'real-debrid.com', 'host_icon': 'https://fcdn.real-debrid.com/0830/images/hosters/realdebrid.png', 'chunks': 32, 'crc': 1, 'download': 'https://77-4.download.real-debrid.com/d/SM6ZDMBUWN44M/%5BLostYears%5D%20Solo%20Leveling%20-%20S01E07%20%28WEB%201080p%20x264%20AAC%29%20%5B20D3399B%5D.mkv', 'streamable': 1}
 