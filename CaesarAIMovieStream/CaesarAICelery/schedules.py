from CaesarAITorrentParsers.CaesarAIJackett import CaesarAIJackett
class CaesarAISchedules:
    @staticmethod
    def update_all_torrent_indexers():
        return {"results":"Done","indexers":CaesarAIJackett.extract_all_torrent_indexers()}
   