FROM jsu6/visiblev8:crawler

FROM python:3-slim

USER root

COPY ./chromium-build-deps.sh ./

# Install node, npm and chromium dependencies
RUN apt-get update; \
    apt-get install -y --no-install-recommends \
        nodejs npm lsb-release; \
    ./chromium-build-deps.sh \
        --no-syms \
        --no-arm \
        --no-chromeos-fonts \
        --no-nacl \
        --no-backwards-compatible \
        --no-prompt

# Copy chromium with VV8
COPY --from=jsu6/visiblev8:crawler /opt/chromium.org/chromium/* /opt/chromium.org/chromium/

# Create vv8 user
RUN groupadd -g 1001 -f vv8; \
    useradd -u 1001 -g 1001 -s /bin/bash -m vv8
ENV PATH="${PATH}:/home/vv8/.local/bin"

WORKDIR /app
RUN chown -R vv8:vv8 /app

USER vv8

# Add working dir to python path
ENV PYTHONPATH "${PYTHONPATH}:/app"

# Move vv8 crawler to app dir
#COPY --from=jsu6/visiblev8:crawler --chown=vv8:vv8 /home/node/install ./node
COPY --chown=vv8:vv8 ./vv8_worker ./node
WORKDIR /app/node
RUN npm install
WORKDIR /app

# Install python modules
COPY --chown=vv8:vv8 ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
RUN pip install coverage

# Copy app
COPY --chown=vv8:vv8 ./vv8web_task_queue ./vv8web_task_queue
COPY --chown=vv8:vv8 ./tests ./tests

# Copy requirements for coverage from here
COPY --chown=vv8:vv8 ./test_requirements.txt ./test_requirements.txt
RUN pip install --no-cache --upgrade -r ./test_requirements.txt

RUN pip install coverage

# CMD celery -A vv8web_task_queue.app.app worker -Q url -l INFO

# These env vars are required for celery despite celery not being used during unittests
ENV VV8_CELERY_BROKER task_queue_broker
ENV VV8_CELERY_BROKER_PORT 6379
ENV VV8_CELERY_ID vv8_worker
ENV VV8_CELERY_BACKEND_USER vv8
ENV VV8_CELERY_BACKEND_PASSWORD vv8
ENV VV8_CELERY_BACKEND_HOST database
ENV VV8_CELERY_BACKEND_PORT 5432
ENV VV8_CELERY_BACKEND_DATABASE celery_backend

# python test file, Compose up docker, remote connect on VS Code
# command to run file (so far): sudo docker build -f ./vv8_worker.test.dockerfile -t vv8_worker_test ./
#RUN python3 -m unittest discover -s ./tests/unit -t ./
RUN coverage run -m unittest discover coverage -s ./tests/unit -t ./
RUN coverage report -m
