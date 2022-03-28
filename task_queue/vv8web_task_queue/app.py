import vv8web_task_queue.config as cfg

from celery import Celery


app = Celery(
    cfg.celery_id,
    broker=cfg.celery_broker_uri,
    include=['vv8web_task_queue.tasks']
)


app.conf.task_routes = {
    'vv8web_task_queue.tasks.process_url_task': {
        'queue': 'url'
    }
}


if __name__ == '__main__':
    app.start()
