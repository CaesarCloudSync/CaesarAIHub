from CaesarAITorrentParsers.CaesarAIJackett import CaesarAIJackett
class CaesarAISchedules:
    @staticmethod
    def update_all_torrent_indexers():
        CaesarAIJackett.extract_all_torrent_indexers()
        return {"results":"Done"}
   