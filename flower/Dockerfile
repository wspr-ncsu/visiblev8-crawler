FROM mher/flower:latest

USER root

VOLUME /etc/db

CMD [ "celery", "--broker=redis://localhost:6379/0", "flower", "--port=5555", "--persistent=True", "--db=/etc/db/flower.db" ]