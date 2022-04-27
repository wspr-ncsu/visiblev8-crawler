FROM python:3-slim

# Create vv8 user
RUN groupadd -g 1001 -f vv8; \
    useradd -u 1001 -g 1001 -s /bin/bash -m vv8
ENV PATH="${PATH}:/app"

WORKDIR /app
RUN chown -R vv8:vv8 /app

COPY --chown=vv8:vv8 ./requirements.txt ./requirements.txt

RUN pip install --no-cache --upgrade -r ./requirements.txt

COPY --chown=vv8:vv8 ./vv8db_sidecar ./vv8db_sidecar
COPY --chown=vv8:vv8 ./tests ./tests

EXPOSE 80/tcp

# These env vars are required for celery despite celery not being used during unittests
ENV VV8_CELERY_BROKER task_queue_broker
ENV VV8_CELERY_BROKER_PORT 6379
ENV VV8_CELERY_ID vv8_worker
ENV VV8_CELERY_BACKEND_USER vv8
ENV VV8_CELERY_BACKEND_PASSWORD vv8
ENV VV8_CELERY_BACKEND_HOST database
ENV VV8_CELERY_BACKEND_PORT 5432
ENV VV8_CELERY_BACKEND_DATABASE celery_backend

# CMD uvicorn vv8db_sidecar.server:app --host 0.0.0.0 --port 80

RUN python3 -m unittest discover -s ./tests/unit -t ./
