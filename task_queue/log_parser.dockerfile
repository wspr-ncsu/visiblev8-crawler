FROM python:3-slim

# Create vv8 user
RUN groupadd -g 1001 -f vv8; \
    useradd -u 1001 -g 1001 -s /bin/bash -m vv8
ENV PATH="${PATH}:/home/vv8/.local/bin"

WORKDIR /app
RUN chown -R vv8:vv8 /app

USER vv8

# Add working dir to python path
ENV PYTHONPATH "${PYTHONPATH}:/app"

# Install python modules
COPY --chown=vv8:vv8 ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

# Copy app
COPY --chown=vv8:vv8 ./vv8web_task_queue ./vv8web_task_queue

CMD celery -A vv8web_task_queue.app worker -Q log_parser -l INFO
