
import logging
from CaesarAICelery.tasks import get_unfinished_episodes
class CaesarAISchedules:
    @staticmethod
    def schedule_interrupted_episodes():
        logging.info(f"Creating interrupted episodes task...")
        result = get_unfinished_episodes.delay()
        logging.info(f"Interrupted episodes task created.")
        return {"task_id":result.id}