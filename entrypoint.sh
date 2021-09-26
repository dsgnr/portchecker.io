#!/bin/sh
cd /api
export GUNICORN_RELOAD="--reload"
export GUNICORN_BIND="-b 0.0.0.0:3000"
export GUNICORN_WORKER_COUNT="10"
exec gunicorn \
         -t 120 \
         -w ${GUNICORN_WORKER_COUNT} \
         --max-requests 2000 \
         --keep-alive 0 \
         --access-logfile - \
         --error-logfile - \
         ${GUNICORN_BIND} \
         ${GUNICORN_RELOAD} \
         app:app
echo "Exiting..."
