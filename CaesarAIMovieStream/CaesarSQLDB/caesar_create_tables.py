from CaesarSQLDB.caesarcrud import CaesarCRUD
class CaesarCreateTables:
    def __init__(self) -> None:
        self.usersfields = ("title","name","displayname","imdbid","anilistid","season","episode","resolution","languages","mediatype","pub_date","magnet_link","torrent_link","categories","seeders","peers","indexer","dual_audio","subtitles","is_multi_audio")

        

    def create(self,caesarcrud :CaesarCRUD):
        caesarcrud.create_table("userid",self.usersfields,
        ("varchar(255) NOT NULL","varchar(255) NOT NULL","varchar(255) NOT NULL","varchar(255)","varchar(255)","INT","INT","varchar(255)","varchar(255)","varchar(255) NOT NULL","varchar(255)","TEXT","TEXT","TEXT","INT","INT","varchar(255)","varchar(255)","BOOLEAN","BOOLEAN"),
        "users")
