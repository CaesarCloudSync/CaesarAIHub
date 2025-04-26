import os
class CaesarAIConstants:
    BASE_PROWLER_CONTAINER="http://prowlarr"
    BASE_LOCALHOST="http://localhost"
    BASE_JACKETT_URL = "http://jackett:9117/api/v2.0"
    TORZNAB_ALL_SUFFIX="/indexers/all/results/torznab"
    ALL_INDEXERS_SUFFIX="/indexers/all/results"

    BASE_PROWLER_URL = "http://prowlarr:9696/api/v1/search"
    JACKETT_API_KEY= os.environ.get("JACKETT_API_KEY")
    PROWLARR_API_KEY=os.environ.get("PROWLARR_API_KEY")
    ENDPOINT="tvsearch"
    REALDEBRID_API_KEY= os.environ.get("REALDEBRID_API_KEY")
    ANIME_JACKETT_CATEGORY=5070
    MOVIESRIES_TABLE="moviesseries"
    TEXT_SANITIZE_REGEX=r'[^a-zA-Z0-9\s]'
    REDIS_HASH_NAME="episode-task"
    EPISODE_REDIS_ID="{query}_{season}_{episode}"
    Nyaasi="nyaasi"
    EZTV="eztv"