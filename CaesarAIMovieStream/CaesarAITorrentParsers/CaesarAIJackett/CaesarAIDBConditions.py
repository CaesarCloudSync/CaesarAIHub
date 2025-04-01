
class CaesarAIDBConditins:
    batch_name_and_season="(query = '{query}' AND season = '{season}') OR (query = '{query}' AND season  LIKE '%{season}%') OR (query = '{query}' AND season = 'BATCH')"
    episodes_batch_name_and_season="(query = '{query}' AND season = 'BATCH') OR (query = '{query}' AND episode = 'BATCH')"
    episode_name_and_season="(query = '{query}' AND season = '{season}' AND episode = '{episode}') OR (query = '{query}' AND season  LIKE '%{season}%' AND episode LIKE '%{episode}%')"