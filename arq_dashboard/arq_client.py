import pickle
import aioredis


class ARQClient:
    QUEUE_KEY = 'arq:queue'
    JOBS_KEY = 'arq:job:{}'
    RESULTS_KEY = 'arq:result:{}'
    ACTIVE_JOBS_KEY = 'arq:in-progress:{}'

    def __init__(self, host='localhost', port=6379, db=0):
        self.host = host
        self.port = port
        self.db = db
        self._redis = None

    async def init_pool(self):
        self._redis = await aioredis.create_redis_pool(
            f'redis://{self.host}:{self.port}',
            db=self.db,
        )

    async def _extract_jobs(self, keys, mask='{}'):
        jobs = {}
        for key in keys:
            key = key.decode()
            job = pickle.loads(await self._redis.get(mask.format(key)))
            jobs[key] = job
        return jobs

    async def get_jobs(self):
        jobs_keys = await self._redis.zrevrange(self.QUEUE_KEY, 0, -1)
        return await self._extract_jobs(jobs_keys, self.JOBS_KEY)

    async def get_results(self):
        result_keys = await self._redis.keys(self.RESULTS_KEY.format('*'))
        return await self._extract_jobs(result_keys)

    async def get_active_jobs(self):
        return [
            key.decode().split(':')[-1]
            for key in await self._redis.keys(self.ACTIVE_JOBS_KEY.format('*'))
        ]

    async def get_summary(self):
        jobs = await self.get_jobs()
        job_results = await self.get_results()
        active_jobs = await self.get_active_jobs()
        return {
            'jobs': jobs,
            'job_results': job_results,
            'active_jobs': active_jobs
        }

    async def retry_job(self, job_key):
        raw_job = await self._redis.get(job_key)
        job = pickle.loads(raw_job)

        # delete previous result of job
        await self._redis.delete(job_key)

        # create job as new
        await self._redis.set(
            job_key.replace('result', 'job'),
            raw_job
        )
        job_id = job_key.split(':')[-1]

        # push job to queue
        self._redis.zadd(self.QUEUE_KEY, job['et'], job_id)
        return job

    async def delete_job(self, job_id):
        # remove from queue
        await self._redis.zrem(self.QUEUE_KEY, job_id)

        # remove all artifacts
        job_keys = await self._redis.keys(f'*{job_id}*')
        for key in job_keys:
            await self._redis.delete(key)
