"""
The Celery definition
"""
# Standard Library
import os

# Third Party
from celery import Celery


def get_celery():
    """
    Defines the celery config
    """
    rabbit_user = os.environ.get("RABBITMQ_DEFAULT_USER")
    rabbit_pass = os.environ.get("RABBITMQ_DEFAULT_PASS")
    rabbit_vhost = os.environ.get("RABBITMQ_DEFAULT_VHOST")
    broker_url = f'amqp://{rabbit_user}:{rabbit_pass}@rabbitmq:5672/{rabbit_vhost}'
    celery = Celery("tasks")
    celery_conf = {
        "include": "tasks",
        "result_backend": "redis://redis",
        "broker_url": broker_url,
        "timezone": "UTC",
        "task_serializer": "json",
        "result_serializer": "json",
        "task_soft_time_limit": 1800,
        "worker_prefetch_multiplier": 1,
        "result_expires": 900,  # 15 minutes
    }

    celery.conf.update(celery_conf)
    return celery


celery_init = get_celery()
