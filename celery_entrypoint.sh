#!/bin/sh
cd api
celery -A worker.celery_init worker -l INFO
