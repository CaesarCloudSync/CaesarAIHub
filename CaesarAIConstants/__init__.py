import os
class CaesarAIConstants:
    BASE_JACKETT_URL = "http://jackett:9117/api/v2.0/indexers/all/results/torznab"
    JACKETT_API_KEY= os.environ.get("JACKETT_API_KEY")
    ENDPOINT="tvsearch"
    REALDEBRID_API_KEY= os.environ.get("REALDEBRID_API_KEY")