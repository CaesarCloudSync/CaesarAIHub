import os
class CaesarAIConstants:
    BASE_PROWLER_CONTAINER="http://prowlarr"
    BASE_LOCALHOST="http://localhost"
    BASE_JACKETT_URL = "http://jackett:9117/api/v2.0/indexers/all/results/torznab"
    BASE_PROWLER_URL = "http://prowlarr:9696/api/v1/search"
    JACKETT_API_KEY= os.environ.get("JACKETT_API_KEY")
    PROWLARR_API_KEY=os.environ.get("PROWLARR_API_KEY")
    ENDPOINT="tvsearch"
    REALDEBRID_API_KEY= os.environ.get("REALDEBRID_API_KEY")