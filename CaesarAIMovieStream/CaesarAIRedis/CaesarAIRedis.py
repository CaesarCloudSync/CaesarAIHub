import redis
from itertools import zip_longest
import redis.asyncio as redisasync
from CaesarAIConstants import CaesarAIConstants

class CaesarAIRedis:
    def __init__(self,async_mode=False) -> None:
        if not async_mode:
            self.r= redis.Redis(host='redis', port=6379, decode_responses=True)
        else:
            self.r= redisasync.Redis(host='redis', port=6379, decode_responses=True)


    def setkey(self,key:str,data:str):
        self.r.set(key,data)
    def getkey(self,key:str):
        return self.r.get(key)
    def deletekey(self,key:str):
        self.r.delete(key)
    def set_episode_task(self,episodeid:str,value:str):
        self.r.hset(f"{CaesarAIConstants.REDIS_HASH_NAME}",episodeid,value)
    def get_episode_task(self,episodeid:str):
        return self.r.hget(f"{CaesarAIConstants.REDIS_HASH_NAME}",episodeid)
    def delete_episode_task(self,episodeid:str):
        self.r.delete(f"{CaesarAIConstants.REDIS_HASH_NAME}",episodeid)
    def batcher(self,iterable, n):
        args = [iter(iterable)] * n
        return zip_longest(*args)

    def delete_all_episode_tasks(self):
        fields = self.r.hkeys(CaesarAIConstants.REDIS_HASH_NAME)
        self.r.hdel(CaesarAIConstants.REDIS_HASH_NAME, *fields)
            
    def get_all_episode_task_ids(self):
        all_fields = self.r.hgetall(CaesarAIConstants.REDIS_HASH_NAME)
        decoded_fields = list(k for k in all_fields.keys())
        return decoded_fields

    def get_all_episode_tasks(self):
        all_fields = self.r.hgetall(CaesarAIConstants.REDIS_HASH_NAME)
        decoded_fields = {k: v for k, v in all_fields.items()}
        return decoded_fields
    def delete_task(self,episodeid:str):
        self.r.hdel(CaesarAIConstants.REDIS_HASH_NAME, episodeid)


    async def async_set_key(self,key:str,data:str):
        await self.r.set(key,data)
    async def async_get_key(self,key:str):
        return await self.r.get(key)
    async def async_delete_key(self,key:str):
        await self.r.delete(key)
    async def async_set_episode_task(self,episodeid:str,value:str):
        await self.r.hset(f"{CaesarAIConstants.REDIS_HASH_NAME}",episodeid,value)
    async def async_hget_episode_task(self,episodeid:str):
        return await self.r.hget(f"{CaesarAIConstants.REDIS_HASH_NAME}",episodeid)
    async def async_delete__episode_task(self,episodeid:str):
        await self.r.delete(f"{CaesarAIConstants.REDIS_HASH_NAME}",episodeid)
    async def async_get_all_episode_task_ids(self):
        all_fields = await self.r.hgetall(CaesarAIConstants.REDIS_HASH_NAME)
        decoded_fields = list(k for k in all_fields.keys())
        return decoded_fields

