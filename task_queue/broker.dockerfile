FROM redis:6.2

FROM python:3-slim

# Install python modules
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

# Set working dir to where the app will install
WORKDIR /app
# Add working dir to python path
ENV PYTHONPATH "${PYTHONPATH}:/app"

COPY ./vv8web_task_queue ./vv8web_task_queue

EXPOSE 6379/tcp

ENV VV8_CELERY_BROKER "localhost"
ENV VV8_CELERY_BROKER_PORT "6379"
ENV VV8_CELERY_ID "broker"

CMD python3 /app/vv8web_task_queue/app.py
