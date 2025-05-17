from typing import List
class CaesarAIMediaIndexers:
    # https://github.com/Jackett/Jackett/wiki/Jackett-Categories
    GAME_INDEXERS = ["1337x","Torlock","The Pirate Bay"]
    GAME_CATEGORIES_PC_RANGE = "4000,4010,4020,4030,4040,4050,4060,4070"
    GAME_CATEGORIES_CONSOLE_RANGE = "1000,1010,1020,1030,1040,1050,1060,1070,1080,1090,1110,1120,1130,1140,1180"
    MOVIE_INDEXERS = ["Torlock","1337x","The Pirate Bay","Torrent9","Badass Torrents"]
    MOVIE_CATEGORIES_RANGE = "2000,2010,2020,2030,2040,2045,2050,2060,2070,2080"
    ANIME_INDEXERS = ["Nyaa.si","1337x","YTS"] # ETC.
    TV_INDEXERS = ["1337x","YTS"]
    
    MUSIC_INDEXERS = ["1337x","YTS"]
    BOOK_INDEXERS = ["1337x","YTS"]
    MANGA_INDEXERS = ["1337x","YTS"]
    COMIC_INDEXERS = ["1337x","YTS"]
    EBOOK_INDEXERS = ["1337x","YTS"]

    DOCUMENT_INDEXERS = ["1337x","YTS"]
    SOFTWARE_INDEXERS = ["1337x","YTS"]

    AUDIOBOOK_INDEXERS = ["1337x","YTS"]
    MAGAZINE_INDEXERS = ["1337x","YTS"]
    NEWSPAPER_INDEXERS = ["1337x","YTS"]

    MISC_INDEXERS = ["1337x","YTS"]
    OTHER_INDEXERS = ["1337x","YTS"]
    # Define a sorting key using the priority list
    @staticmethod
    def make_sort_key(priority_list):
        def sort_key(item):
            try:
                return priority_list.index(item)
            except ValueError:
                return len(priority_list)
        return sort_key

    def sort_indexer_for_game(indexers:List[str]):
        sorted_list = sorted(indexers, key=CaesarAIMediaIndexers.make_sort_key(CaesarAIMediaIndexers.GAME_INDEXERS))
        return sorted_list
    def sort_indexer_for_movie(indexers:List[str]):
        sorted_list = sorted(indexers, key=CaesarAIMediaIndexers.make_sort_key(CaesarAIMediaIndexers.MOVIE_INDEXERS))
        return sorted_list
    def sort_indexer_for_anime(indexers:List[str]):
        sorted_list = sorted(indexers, key=CaesarAIMediaIndexers.make_sort_key(CaesarAIMediaIndexers.ANIME_INDEXERS))
        return sorted_list
    def sort_indexer_for_tv(indexers:List[str]):
        sorted_list = sorted(indexers, key=CaesarAIMediaIndexers.make_sort_key(CaesarAIMediaIndexers.TV_INDEXERS))
        return sorted_list
    def sort_indexer_for_music(indexers:List[str]):
        sorted_list = sorted(indexers, key=CaesarAIMediaIndexers.make_sort_key(CaesarAIMediaIndexers.MUSIC_INDEXERS))
        return sorted_list
    def sort_indexer_for_book(indexers:List[str]):
        sorted_list = sorted(indexers, key=CaesarAIMediaIndexers.make_sort_key(CaesarAIMediaIndexers.BOOK_INDEXERS))
        return sorted_list
    def sort_indexer_for_manga(indexers:List[str]):
        sorted_list = sorted(indexers, key=CaesarAIMediaIndexers.make_sort_key(CaesarAIMediaIndexers.MANGA_INDEXERS))
        return sorted_list
    def sort_indexer_for_comic(indexers:List[str]):
        sorted_list = sorted(indexers, key=CaesarAIMediaIndexers.make_sort_key(CaesarAIMediaIndexers.COMIC_INDEXERS))
        return sorted_list
    def sort_indexer_for_ebook(indexers:List[str]):
        sorted_list = sorted(indexers, key=CaesarAIMediaIndexers.make_sort_key(CaesarAIMediaIndexers.EBOOK_INDEXERS))
        return sorted_list
    def sort_indexer_for_document(indexers:List[str]):
        sorted_list = sorted(indexers, key=CaesarAIMediaIndexers.make_sort_key(CaesarAIMediaIndexers.DOCUMENT_INDEXERS))
        return sorted_list
    def sort_indexer_for_software(indexers:List[str]):
        sorted_list = sorted(indexers, key=CaesarAIMediaIndexers.make_sort_key(CaesarAIMediaIndexers.SOFTWARE_INDEXERS))
        return sorted_list
    def sort_indexer_for_audiobook(indexers:List[str]):
        sorted_list = sorted(indexers, key=CaesarAIMediaIndexers.make_sort_key(CaesarAIMediaIndexers.AUDIOBOOK_INDEXERS))
        return sorted_list
    def sort_indexer_for_magazine(indexers:List[str]):
        sorted_list = sorted(indexers, key=CaesarAIMediaIndexers.make_sort_key(CaesarAIMediaIndexers.MAGAZINE_INDEXERS))
        return sorted_list
    def sort_indexer_for_newspaper(indexers:List[str]):
        sorted_list = sorted(indexers, key=CaesarAIMediaIndexers.make_sort_key(CaesarAIMediaIndexers.NEWSPAPER_INDEXERS))
        return sorted_list
    def sort_indexer_for_misc(indexers:List[str]):
        sorted_list = sorted(indexers, key=CaesarAIMediaIndexers.make_sort_key(CaesarAIMediaIndexers.MISC_INDEXERS))
        return sorted_list
    def sort_indexer_for_other(indexers:List[str]):
        sorted_list = sorted(indexers, key=CaesarAIMediaIndexers.make_sort_key(CaesarAIMediaIndexers.OTHER_INDEXERS))
        return sorted_list
   