# ARQ Dashboard
Simple dashboard for [async RQ](https://github.com/samuelcolvin/arq)  

You can:
- View all queued jobs
- View active jobs
- Remove job from queue
- Retry failed jobs or repeat successed jobs

**Warning!**  
arq_dashboard use [KEYS](https://redis.io/commands/KEYS) 

## How to use
At now ARQ Dashboard easy work only with docker  

For example `docker-compose.yml` part:
```yml
arq_dashboard:
  image: devroman/arq_dashboard:latest
  environment:
    - REDIS_HOST=redis
    - REDIS_DB=1
  ports:
    - 9182:9182
```

### Backend
We use FastAPI and basic redis access to queue  
All sources in: [arq_dashboard/arq_client.py](arq_dashboard/arq_client.py)

### Frontend
UI based on simple [Milligram CSS framework](https://milligram.io/) and Google Fonts  
All sources in one file: [arq_dashboard/templates/index.html](arq_dashboard/templates/index.html)

## TODO's
- Use data access and models from ARQ package
- Remove 'keys' execution
- Migrate app SSR to SPA
- Add websocket to UI for UX
- Create pip package
- Add tests
- Separate dev packages and production build
