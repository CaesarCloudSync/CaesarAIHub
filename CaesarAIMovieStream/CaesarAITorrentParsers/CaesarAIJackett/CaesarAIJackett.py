import xml.etree.ElementTree as ET
from io import BytesIO
from CaesarAITorrentParsers.models.TorrentItem import TorrentItem
from CaesarAIConstants import CaesarAIConstants
from typing import List, AsyncGenerator,Union
import requests
import json
from CaesarAIRedis import CaesarAIRedis
from CaesarSQLDB.caesarcrud import CaesarCRUD
from CaesarSQLDB.caesar_create_tables import CaesarCreateTables
from imdb import Cinemagoer
import logging
from collections import OrderedDict
from CaesarAITorrentParsers.CaesarAIJackett.CaesarAIDBConditions import CaesarAIDBConditins
from CaesarAIUtils import CaesarAIUtils
class CaesarAIJackett:
    def __init__(self,url=None,db=False) -> None:
        # Extract relevant data
        self.torrent_items:List[TorrentItem]= []
        self.crud = CaesarCRUD()
        self.cardb = CaesarCreateTables()
        if not db:
            self.response = requests.get(url)
            xml = self.response.content
            self.namespace = {'atom': 'http://www.w3.org/2005/Atom', 'torznab': 'http://torznab.com/schemas/2015/feed'}
            tree = ET.parse(BytesIO(xml))
            self.root = tree.getroot()


    def get_torrent_info(self,query,verbose=0) -> List[TorrentItem]:
    
        
        for item in self.root.findall(".//item"):
            title = item.find("title").text if item.find("title") is not None else "N/A"
            guid = item.find("guid").text if item.find("guid") is not None else "N/A"
            pub_date = item.find("pubDate").text if item.find("pubDate") is not None else "N/A"
            size = item.find("size").text if item.find("size") is not None else "N/A"
            magnet_link = item.find("link").text if item.find("link") is not None else "N/A"
            indexer = item.find("jackettindexer").text if item.find("jackettindexer") is not None else "N/A"
            # Extract torznab attributes
            categories = [attr.get("value") for attr in item.findall("torznab:attr[@name='category']", self.namespace)]
            seeders = item.find("torznab:attr[@name='seeders']", self.namespace)
            peers = item.find("torznab:attr[@name='peers']", self.namespace)

            seeders = seeders.get("value") if seeders is not None else "N/A"
            peers = peers.get("value") if peers is not None else "N/A"
            if verbose == 1:
                # Print extracted data
                print(f"Title: {title}")
                print(f"Indexer: {indexer}")
                print(f"GUID: {guid}")
                print(f"Published Date: {pub_date}")
                print(f"Size: {size}")
                print(f"Magnet Link: {magnet_link}")
                print(f"Categories: {categories}")
                print(f"Seeders: {seeders}")
                print(f"Peers: {peers}")
                print("-" * 50)

            # Create Pydantic model instance
            torrent = TorrentItem(
                query=query,
                title=title,
                guid=guid,
                pub_date=pub_date,
                size=size,
                magnet_link=magnet_link,
                categories=categories,
                seeders=seeders,
                peers=peers,
                indexer=indexer
            )
            self.torrent_items.append(torrent)
        return self.torrent_items
    def get_largest_file(self) -> List[TorrentItem]:
        return sorted(self.torrent_items, key=lambda x: x.size or 0, reverse=True)
    def get_largest_file_with_highest_seeders(self) -> List[TorrentItem]:
        return sorted(self.torrent_items, key=lambda x: ( x.size and x.seeders)or 0 , reverse=True)
    def get_single_episodes(self) -> List[TorrentItem]:
        return list(filter(lambda x:self.is_single(x) and self.not_torrent_only_magnet(x),self.torrent_items))
    def sort_torrents(self,torrent:TorrentItem):
        # Prioritize 'BATCH' episodes by putting them first
        if torrent.episode == "BATCH":
            return (-1, 0)  # 'BATCH' comes first, ignore the actual episode number
        if isinstance(torrent.episode,list):
            return (-1,0)
        return (1, torrent.episode)  # Otherwise, sort by the episode number

    def get_batch_episodes(self)-> List[TorrentItem]:
        return list(sorted(filter(lambda x:self.is_batch and self.not_torrent_only_magnet(x),self.torrent_items),key=self.sort_torrents))
    def filter_unique_episodes(self,torrents: List[TorrentItem]) -> List[TorrentItem]:

        seen = set()
        unique_torrents = []
        
        for torrent in torrents:
            episode_key = frozenset(torrent.episode) if isinstance(torrent.episode, list) else torrent.episode  # Handle lists or strings
            if episode_key not in seen:
                seen.add(episode_key)
                unique_torrents.append(torrent)
    
        return unique_torrents

    def check_batch_episodes_db(self,query:str,season:int):
        print(CaesarAIDBConditins.batch_name_and_season.format(query=CaesarAIUtils.sanitize_text(query),season=season))
        exists = self.crud.check_exists(("*"),CaesarAIConstants.MOVIESRIES_TABLE,CaesarAIDBConditins.batch_name_and_season.format(query=CaesarAIUtils.sanitize_text(query),season=season))
        return exists
    def check_episodes_db(self,query:str,season:int,episode:int):
        print(CaesarAIDBConditins.episodes_name_and_season.format(query=CaesarAIUtils.sanitize_text(query),season=season,episode=episode))
        exists = self.crud.check_exists(("*"),CaesarAIConstants.MOVIESRIES_TABLE,CaesarAIDBConditins.episodes_name_and_season.format(query=CaesarAIUtils.sanitize_text(query),season=season,episode=episode))
        return exists
    def get_episodes_db(self,query:str,season:int,episode:int) -> List[TorrentItem]:
     
        results = self.crud.get_data(self.cardb.MOVISERIESFIELDS,CaesarAIConstants.MOVIESRIES_TABLE,CaesarAIDBConditins.episodes_name_and_season.format(query=CaesarAIUtils.sanitize_text(query),season=season,episode=episode))
        results:List[TorrentItem] = list(map(lambda x:TorrentItem.parse_obj(x),results))
        return sorted(results,key=self.sort_torrents)
    
    def get_batch_episodes_db(self,query:str,season:int) -> List[TorrentItem]:
     
        results = self.crud.get_data(self.cardb.MOVISERIESFIELDS,CaesarAIConstants.MOVIESRIES_TABLE,CaesarAIDBConditins.batch_name_and_season.format(query=CaesarAIUtils.sanitize_text(query),season=season))
        results:List[TorrentItem] = list(map(lambda x:TorrentItem.parse_obj(x),results))
        return sorted(results,key=self.sort_torrents)

    def save_batch_episode(self,torrentitem:TorrentItem) -> bool:
        try:
            
            result = self.crud.post_data(self.cardb.MOVISERIESFIELDS,
                                (torrentitem.query,torrentitem.title,torrentitem.name,torrentitem.displayname,None,None,str(torrentitem.season),str(torrentitem.episode),torrentitem.size,torrentitem.resolution,str(torrentitem.languages),"tv/series/anime/movie",torrentitem.pub_date,
                                torrentitem.guid,torrentitem.magnet_link,torrentitem.torrent_link,torrentitem.categories,torrentitem.seeders,torrentitem.peers,torrentitem.indexer,str(torrentitem.dual_audio),str(torrentitem.subtitles),
                                torrentitem.is_multi_audio
                                ),
                                CaesarAIConstants.MOVIESRIES_TABLE)
            if result:
                return True
            else:
                return False
        except Exception as ex:
            print(type(ex),ex)
            return False

    def save_batch_episodes(self,torrentitems:List[TorrentItem]) -> List[bool]:
        unique_episodes = self.filter_unique_episodes(torrentitems)
      
        print(unique_episodes)
        return list(map(self.save_batch_episode,unique_episodes))
    
    def get_single_and_multi_audio(self)-> List[TorrentItem]:
        return list(filter(lambda x:x.is_multi_audio and self.not_torrent_only_magnet(x),self.get_single_episodes()))
    def not_torrent_only_magnet(self,x:TorrentItem):
        return "magnet:?xt=" in x.magnet_link
    def is_batch(self,x:TorrentItem):
        return type(x.episode) == list
    def is_single(self,x:TorrentItem):
        return type(x.episode) != list
    @staticmethod
    def get_all_torrent_indexers():
        cr = CaesarAIRedis()
        if not cr.getkey("indexers"):
            url = f"{CaesarAIConstants.BASE_JACKETT_URL}{CaesarAIConstants.ALL_INDEXERS_SUFFIX}?apikey={CaesarAIConstants.JACKETT_API_KEY}"
            response = requests.get(url)
            indexers_data = response.json()["Indexers"]
            indexers = list(set([indexer["ID"] for indexer in indexers_data]))
            cr.setkey("indexers",json.dumps(indexers))
            return indexers
        else:
            indexers = cr.getkey("indexers")
            return json.loads(indexers)


    #@staticmethod
    #def get_series_movies_id(torrent:TorrentItem):
    #    imdb_id = None
    #    anilist_id = None
    #    if not CaesarAIConstants.ANIME_JACKETT_CATEGORY in torrent.categories: # Anime Category
   #         imdb_id,mediatype = None,None #,CaesarAIJackett.get_imdb_id(torrent.name)
    #    else:
    #        anilist_id = CaesarAIJackett.get_anilist_id(torrent.name)
    #        mediatype="tv/anime"
    #    return imdb_id,anilist_id,mediatype
            


    @staticmethod
    async def episodes_streamer(title:str,season:int,episode:int,indexers:List[str],save:Union[bool,None]):
        caejackett = CaesarAIJackett(db=True)
        yield "event: open\ndata:open\n\n"
        for indexer in indexers:            
            print("Starting...")
            if caejackett.check_episodes_db(title,season,episode):
                torrentinfo = caejackett.get_episodes_db(title,season,episode)
                save = False
            else:
                print("Extracting")
                url = f"{CaesarAIConstants.BASE_JACKETT_URL}{CaesarAIConstants.TORZNAB_ALL_SUFFIX.replace('all',indexer)}?apikey={CaesarAIConstants.JACKETT_API_KEY}&t={CaesarAIConstants.ENDPOINT}&q={title}&season={season}"
                caejackett = CaesarAIJackett(url)
                torrentinfo = caejackett.get_torrent_info(title)
                torrentinfo_single = caejackett.get_single_episodes()
                torrentinfo_batch =  caejackett.get_batch_episodes()
                torrentinfo = torrentinfo_batch + torrentinfo_single
                print(torrentinfo)
            if save:
                print("Saving...")
                caejackett.save_batch_episodes(torrentinfo)




            for index,torrent in enumerate(torrentinfo):
                data = json.dumps({"index":index,"total":len(torrentinfo),"episodes":torrent.dict()})
                yield f"event: episodes\n\ndata: {data}\n\n"
        yield "event: close\ndata:close\n\n"


    @staticmethod
    async def single_episode_streamer(title:str,season:int,episode:int,indexers:List[str]):
        yield "event: open\ndata:open\n\n"
        for indexer in indexers:

            url = f"{CaesarAIConstants.BASE_JACKETT_URL}{CaesarAIConstants.TORZNAB_ALL_SUFFIX.replace('all',indexer)}?apikey={CaesarAIConstants.JACKETT_API_KEY}&t={CaesarAIConstants.ENDPOINT}&q={title}&season={season}&ep={episode}"
            caejackett = CaesarAIJackett(url)
            torrentinfo = caejackett.get_torrent_info(title)
            torrentinfo = caejackett.get_single_episodes()
            
            first = True
            
            for index,torrent in enumerate(torrentinfo):
                data = json.dumps({"index":index,"total":len(torrentinfo),"episodes":torrent.dict()})
                yield f"event: episodes\n\ndata: {data}\n\n"
        yield "event: close\ndata:close\n\n"
