FROM python:3.9-buster


COPY ./requirements.txt /
RUN pip install -r /requirements.txt

COPY ./arq_dashboard /arq_dashboard/

CMD uvicorn arq_dashboard:app --host 0.0.0.0 --port 9182