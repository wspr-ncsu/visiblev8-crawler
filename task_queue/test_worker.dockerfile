FROM python:3-slim

# Install python modules
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

WORKDIR /app
# Add working dir to python path
ENV PYTHONPATH "${PYTHONPATH}:/app"

COPY ./vv8web_task_queue ./vv8web_task_queue

ENV VV8_CELERY_BROKER=""
ENV VV8_CELERY_BROKER_PORT="6379"
ENV VV8_CELERY_ID="broker"

CMD celery -A vv8web_task_queue.app worker -l INFO
