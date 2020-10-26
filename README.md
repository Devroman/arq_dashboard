# ARQ Dashboard
Simple dashboard for [async RQ](https://github.com/samuelcolvin/arq)  

You can:
- View all queued jobs
- View active jobs
- Remove job from queue
- Retry failed jobs or repeat successed jobs

## How to use
At now ARQ Dashboard easy work only with docker  

## How to dev
After change you must build and push image througt Gitlab CI

### Backend
We use FastAPI and basic redis access to queue  
All sources in: `./arq_dashboard`

### Frontend
UI based on simple [Milligram CSS framework](https://milligram.io/) and Google Fonts  
All sources in one file: `./arq_dashboard/templates/index.html`

## TODO's
- Use data access and models from ARQ package
- Remove 'keys' execution
- Migrate app SSR to SPA
- Add websocket to UI for UX
- Create pip package
- Add tests
- Separate dev packages and production build