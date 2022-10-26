FROM python:3.10-slim

WORKDIR /app

# Create vv8 user
RUN groupadd -g 1001 -f vv8; \
    useradd -u 1001 -g 1001 -s /bin/bash -m vv8
ENV PATH="${PATH}:/home/vv8/.local/bin"

WORKDIR /app
RUN chown -R vv8:vv8 /app

USER vv8

ENV PYTHONPATH "${PYTHONPATH}:/app"

# web server python requirements
COPY --chown=vv8:vv8 ./requirements.txt ./web_server_requirements.txt
RUN pip install --no-cache-dir --upgrade -r ./web_server_requirements.txt

COPY --chown=vv8:vv8 ./app ./app


EXPOSE 4000/tcp

CMD uvicorn app.main:app --host 0.0.0.0 --port 4000
