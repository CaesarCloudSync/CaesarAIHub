
class CaesarAIDBConditins:
    name_and_season="(query = '{query}' AND season = '{season}') OR (query = '{query}' AND season  LIKE '%{season}%') OR (query = '{query}' AND season = 'BATCH')"