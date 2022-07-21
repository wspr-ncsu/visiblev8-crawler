import log_parser_worker.config.celery_config as cfg
import urllib.parse

from celery import Celery
from kombu import Queue


_backend_user = urllib.parse.quote(cfg.celery_backend_user)
_backend_password = urllib.parse.quote(cfg.celery_backend_password)
_backend_host = urllib.parse.quote(cfg.celery_backend_host)
_backend_port = urllib.parse.quote(cfg.celery_backend_port)
_backend_database = urllib.parse.quote(cfg.celery_backend_database)
_backend_url = f'db+postgresql://{_backend_user}:{_backend_password}@{_backend_host}:{_backend_port}/{_backend_database}'


celery_app = Celery(
    cfg.celery_id,
    broker=cfg.celery_broker_uri,
    backend=_backend_url,
    include=[
        'log_parser_worker.tasks'
    ]
)


celery_app.conf.task_default_queue = 'default'
celery_app.conf.task_routes = (
    Queue('default', routing_key='default'),
    Queue('log_parser', routing_key='log_parser')
)
celery_app.conf.task_default_exchange = 'default'
celery_app.conf.task_default_exchange_type = 'direct'
celery_app.conf.task_default_routing_key = 'default'
celery_app.conf.task_routes = {
    'log_parser_worker.tasks.parse_log_task': {
        'queue': 'log_parser'
    }
}


if __name__ == '__main__':
    celery_app.start()
