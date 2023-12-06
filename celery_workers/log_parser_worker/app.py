import log_parser_worker.config.celery_config as cfg

from celery import Celery
from kombu import Queue


celery_app = Celery(
    cfg.celery_id,
    broker=cfg.celery_broker_uri,
    backend=cfg.celery_backend_uri ,
    include=[
        'log_parser_worker.tasks'
    ]
)

celery_app.conf.update(
    result_extended = True,
    result_expire = 1
)


celery_app.conf.task_default_queue = 'default'
celery_app.conf.task_routes = (
    Queue('log_parser', routing_key='log_parser')
)
celery_app.conf.task_default_exchange = 'default'
celery_app.conf.task_default_exchange_type = 'direct'
celery_app.conf.task_default_routing_key = 'default'
celery_app.conf.task_routes = {
    'log_parser_worker.parse_log': {
        'queue': 'log_parser'
    }
}


if __name__ == '__main__':
    celery_app.start()
