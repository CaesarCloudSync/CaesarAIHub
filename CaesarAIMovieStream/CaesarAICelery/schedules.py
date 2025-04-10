
import logging
from CaesarAICelery.tasks import get_unfinished_episodes,update_indexers
class CaesarAISchedules:
    @staticmethod
    def schedule_interrupted_episodes():
        logging.info(f"Creating interrupted episodes task...")
        result = get_unfinished_episodes.delay()
        logging.info(f"Interrupted episodes task created.")
        return {"task_id":result.id}
    @staticmethod
    def schedule_update_indexers():
        logging.info(f"Creating update indexers task...")
        result = update_indexers.delay()
        logging.info(f"Update indexers task created.")
        return {"task_id":result.id}
