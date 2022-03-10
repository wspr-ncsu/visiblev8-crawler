import vv8web_task_queue.config as cfg

from celery import Celery


app = Celery(
    cfg.celery_id,
    broker=cfg.celery_broker_uri,
    include=['vv8web_task_queue.tasks']
)


if __name__ == '__main__':
    app.start()
