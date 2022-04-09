import vv8web_task_queue.config.celery_config as cfg
import urllib.parse

from celery import Celery
from kombu import Queue


_backend_user = urllib.parse.quote(cfg.celery_backend_user)
_backend_password = urllib.parse.quote(cfg.celery_backend_password)
_backend_host = urllib.parse.quote(cfg.celery_backend_host)
_backend_port = urllib.parse.quote(cfg.celery_backend_port)
_backend_database = urllib.parse.quote(cfg.celery_backend_database)
_backend_url = f'db+postgresql://{_backend_user}:{_backend_password}@{_backend_host}:{_backend_port}/{_backend_database}'


app = Celery(
    cfg.celery_id,
    broker=cfg.celery_broker_uri,
    backend=_backend_url,
    include=[
        'vv8web_task_queue.tasks.vv8_worker_tasks',
        'vv8web_task_queue.tasks.log_parser_tasks'
    ]
)


app.conf.task_default_queue = 'default'
app.conf.task_routes = (
    Queue('default', routing_key='default'),
    Queue('url', routing_key='url'),
    Queue('log_parser', routing_key='log_parser')
)
app.conf.task_default_exchange = 'default'
app.conf.task_default_exchange_type = 'direct'
app.conf.task_default_routing_key = 'default'
app.conf.task_routes = {
    'vv8web_task_queue.tasks.vv8_worker_tasks.process_url_task': {
        'queue': 'url'
    },
    'vv8web_task_queue.tasks.log_parser_tasks.parse_log_task': {
        'queue': 'log_parser'
    }
}


if __name__ == '__main__':
    app.start()
