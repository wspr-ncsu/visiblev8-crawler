FROM python:3.10-slim

# Create vv8 user
RUN groupadd -g 1001 -f vv8; \
    useradd -u 1001 -g 1001 -s /bin/bash -m vv8
ENV PATH="${PATH}:/app"

WORKDIR /app
RUN chown -R vv8:vv8 /app

COPY --chown=vv8:vv8 ./requirements.txt ./requirements.txt

RUN pip install --no-cache --upgrade -r ./requirements.txt

COPY --chown=vv8:vv8 ./vv8db_sidecar ./vv8db_sidecar

EXPOSE 80/tcp

CMD uvicorn vv8db_sidecar.server:app --host 0.0.0.0 --port 80 --workers 4
