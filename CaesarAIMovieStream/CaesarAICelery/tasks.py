import logging
import asyncio
from celery import Celery
from CaesarAIRedis import CaesarAIRedis
from CaesarAITorrentParsers.CaesarAIJackett import CaesarAIJackett
logger = logging.getLogger(__name__)
celery_app = Celery(
    "worker",
    backend="redis://redis:6379/0",
    broker="redis://redis:6379/0",
)
# Your actual async function
async def async_get_unfinished_episodes(interuptted_episode_tasks,indexers,redis_instance):
    for episode_task in interuptted_episode_tasks:
        title, season, episode = episode_task.split('_')
        
        logger.info(f"Extracting: {title},{season},{episode}") 
        redis_instance.delete_episode_task(episode_task)# Have this before. It stops the task from repeatedly saving.
        async for event in CaesarAIJackett.stream_get_episodews(title,season,episode,indexers):
            logger.info(str(event))
    return interuptted_episode_tasks
        
        


@celery_app.task(bind=True)
def get_unfinished_episodes(self):
    cr = CaesarAIRedis()
    indexers = CaesarAIJackett.get_current_torrent_indexers()
    interuptted_episode_tasks = cr.get_all_episode_task_ids()
    results =  asyncio.run(async_get_unfinished_episodes(interuptted_episode_tasks,indexers,cr))
    self.update_state(state='COMPLETED', meta={'results': results})
    return {'results': results}

