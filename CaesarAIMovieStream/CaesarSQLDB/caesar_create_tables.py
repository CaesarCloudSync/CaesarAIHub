from CaesarSQLDB.caesarcrud import CaesarCRUD
from CaesarAIConstants import CaesarAIConstants
class CaesarCreateTables:
    def __init__(self) -> None:
        self.MOVISERIESFIELDS = ("query","title","name","displayname","imdbid","anilistid","season","episode","size","resolution","languages","mediatype","pub_date","guid","magnet_link","torrent_link","categories","seeders","peers","indexer","dual_audio","subtitles","is_multi_audio")

        

    def create(self,caesarcrud :CaesarCRUD):
        caesarcrud.create_table(f"{CaesarAIConstants.MOVIESRIES_TABLE}id",self.MOVISERIESFIELDS,
        ("varchar(255) NOT NULL","varchar(255) NOT NULL","varchar(255) NOT NULL","varchar(255) NOT NULL","varchar(255)","varchar(255)","varchar(255)","varchar(255)","BIGINT","varchar(255)","varchar(255)","varchar(255) NOT NULL","varchar(255)","TEXT","TEXT","TEXT","TEXT","INT","INT","varchar(255)","varchar(255)","varchar(255)","varchar(255)"),
        CaesarAIConstants.MOVIESRIES_TABLE)
