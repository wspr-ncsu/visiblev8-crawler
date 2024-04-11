FROM mher/flower:latest

USER root

VOLUME /etc/db

ENV FLOWER_UNAUTHORIZED_API=True

CMD [ "celery", "--broker=redis://task_queue_broker:6379/0", "flower", "--port=5555", "--persistent=True", "--db=/etc/db/flower.db" ]