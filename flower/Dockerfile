FROM mher/flower:latest

USER root

VOLUME /etc/db

ENV FLOWER_UNAUTHORIZED_API=True

CMD [ "sh", "-c", "celery --broker=redis://$CELERY_BROKER:6379/0 flower --port=5555 --persistent=True --db=/etc/db/flower.db" ]
