#! /usr/bin/env sh
set -e
exec gunicorn -k uvicorn.workers.UvicornWorker \
    -b 0.0.0.0:8000 \
    --workers 4 \
    main:app
