
class CaesarAIDBConditins:
    season_condition="(query = '{query}' AND season = '{season}') OR (query = '{query}' AND season  LIKE ' %{season}%')"
    batch_conditon="(query = '{query}' AND season = 'BATCH') OR (query = '{query}' AND episode = 'BATCH')"
    episode_condition="(query = '{query}' AND season = '{season}' AND episode = '{episode}') OR (query = '{query}' AND season  LIKE '%{season}%' AND episode LIKE ' %{episode}%')"