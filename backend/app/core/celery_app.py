from celery import Celery
from app.core import celery_config
import urllib.parse

_backend_user = urllib.parse.quote(celery_config.celery_backend_user)
_backend_password = urllib.parse.quote(celery_config.celery_backend_password)
_backend_host = urllib.parse.quote(celery_config.celery_backend_host)
_backend_port = urllib.parse.quote(celery_config.celery_backend_port)
_backend_database = urllib.parse.quote(celery_config.celery_backend_database)
_backend_url = f'db+postgresql://{_backend_user}:{_backend_password}@{_backend_host}:{_backend_port}/{_backend_database}'


celery_app = Celery(
    celery_config.celery_id,
    broker=celery_config.celery_broker_uri,
    backend=_backend_url,
    # include=[
    #     'vv8web_task_queue.tasks.vv8_worker_tasks',
    #     'vv8web_task_queue.tasks.log_parser_tasks'
    # ]
)

# TODO Not sure what to do about the worker includes at the moment