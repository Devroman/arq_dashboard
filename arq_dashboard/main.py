import os
from pydantic import BaseModel
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from arq_dashboard.arq_client import ARQClient


REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)
REDIS_DB = int(os.environ.get('REDIS_DB', 0))


app = FastAPI()
templates = Jinja2Templates(
    directory="arq_dashboard/templates"
)
arq_client = ARQClient(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB
)


class RetryRequest(BaseModel):
    job_key: str


@app.on_event("startup")
async def startup_event():
    await arq_client.init_pool()


@app.get("/")
async def read_root(request: Request):
    summary = await arq_client.get_summary()
    return templates.TemplateResponse(
        "index.html",
        dict(request=request, **summary)
    )


@app.get("/api/jobs")
async def get_jobs():
    return await arq_client.get_summary()


@app.post("/api/jobs")
async def retry_job(request: RetryRequest):
    job_key = request.job_key
    return await arq_client.retry_job(job_key)


@app.delete("/api/jobs/{job_id}")
async def delete_job(job_id):
    await arq_client.delete_job(job_id)
    return {}
