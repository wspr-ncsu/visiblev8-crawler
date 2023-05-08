from celery import Celery
from app.core import celery_config

celery_client = Celery(
    celery_config.celery_id,
    broker=celery_config.celery_broker_uri,
    backend=celery_config.celery_backend_uri,
)
