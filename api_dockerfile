from python:3.9.7-alpine
COPY requirements.txt /.
RUN pip3 install -r requirements.txt
COPY entrypoint.sh celery_entrypoint.sh /.
COPY api /api
