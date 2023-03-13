from celery import Celery
from app.core import celery_config
import urllib.parse

_backend_user = urllib.parse.quote(celery_config.celery_backend_user)
_backend_password = urllib.parse.quote(celery_config.celery_backend_password)
_backend_host = urllib.parse.quote(celery_config.celery_backend_host)
_backend_port = urllib.parse.quote(celery_config.celery_backend_port)
_backend_database = urllib.parse.quote(celery_config.celery_backend_database)
_backend_url = f'db+postgresql://{_backend_user}:{_backend_password}@{_backend_host}:{_backend_port}/{_backend_database}'

celery_client = Celery(
    celery_config.celery_id,
    broker=celery_config.celery_broker_uri,
    backend=celery_config.celery_backend_uri,
)