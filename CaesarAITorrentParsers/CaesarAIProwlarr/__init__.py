import requests
from io import BytesIO
from typing import List,Union
import xml.etree.ElementTree as ET
from CaesarAITorrentParsers.models.TorrentItem import TorrentItem


class CaesarAIProwlarr:
    def __init__(self,url) -> None:
        # Extract relevant data
        response = requests.get(url)
        self.items:List[dict] = response.json()
        self.torrent_items:List[TorrentItem]= []
    @staticmethod
    def format_season_episode(season:Union[str,int], episode:Union[str,int]) -> str:
        return f"S{int(season):02d}E{int(episode):02d}"
    def format_season(season:Union[str,int]) -> str:
        return f"S{int(season):02d}"
    def get_torrent_info(self,verbose=0) -> List[TorrentItem]:
        for item in self.items:
            magnet_link = item.get("guid") if "magnet:?xt=urn:btih:" in item.get("guid") else None
            torrent_link = item.get("downloadUrl") if item.get("downloadUrl") else None
            torrent = TorrentItem(
                title=item.get("title"),
                guid=item.get("guid"),
                pub_date=item.get("publishDate"),
                size=item.get("size"),
                magnet_link=magnet_link,
                torrent_link=torrent_link,
                categories=[category["id"] for category in item.get("categories")],
                seeders=item.get("seeders"),
                peers=item.get("peers"),
                indexer=item.get("indexer")
            )
            self.torrent_items.append(torrent)
        return self.torrent_items
    def get_largest_file(self) -> List[TorrentItem]:
        return sorted(self.torrent_items, key=lambda x: x.size or 0, reverse=True)
    def get_largest_file_with_highest_seeders(self) -> List[TorrentItem]:
        return sorted(self.torrent_items, key=lambda x: ( x.size and x.seeders)or 0 , reverse=True)
    def get_single_episodes(self) -> List[TorrentItem]:
        return list(filter(lambda x:self.is_single(x) and self.not_torrent_only_magnet(x),self.torrent_items))
    def get_batch_episodes(self)-> List[TorrentItem]:
        return list(filter(lambda x:self.is_batch and self.not_torrent_only_magnet(x),self.torrent_items))
    def get_single_and_multi_audio(self)-> List[TorrentItem]:
        return list(filter(lambda x:x.is_multi_audio and self.not_torrent_only_magnet(x),self.get_single_episodes()))
    def not_torrent_only_magnet(self,x:TorrentItem):
        return "magnet:?xt=" in x.magnet_link
    def is_batch(self,x:TorrentItem):
        return type(x.episode) == list
    def is_single(self,x:TorrentItem):
        return type(x.episode) != list
