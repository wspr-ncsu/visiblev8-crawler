FROM python:3-slim

# Create vv8 user
RUN groupadd -g 1001 -f vv8; \
    useradd -u 1001 -g 1001 -s /bin/bash -m vv8
ENV PATH="${PATH}:/app"

WORKDIR /app
RUN chown -R vv8:vv8 /app

COPY --chown=vv8:vv8 ./requirements.txt ./requirements.txt
RUN pip install --no-cache --upgrade -r ./requirements.txt

# Copy requirements for coverage from here
COPY --chown=vv8:vv8 ./test_requirements.txt ./test_requirements.txt
RUN pip install --no-cache --upgrade -r ./test_requirements.txt

RUN pip install coverage

COPY --chown=vv8:vv8 ./vv8db_sidecar ./vv8db_sidecar
COPY --chown=vv8:vv8 ./tests ./tests

ENV VV8_DB_USERNAME vv8
ENV VV8_DB_PASSWORD vv8
ENV VV8_DB_HOST database
ENV VV8_DB_PORT 5432
ENV VV8_DB_NAME vv8_logs

# CMD uvicorn vv8db_sidecar.server:app --host 0.0.0.0 --port 80

RUN coverage run -m unittest discover coverage -s ./tests/unit -t ./
RUN coverage report -m