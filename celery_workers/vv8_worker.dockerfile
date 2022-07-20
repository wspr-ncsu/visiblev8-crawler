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
COPY --chown=vv8:vv8 ./vv8_crawler ./node
WORKDIR /app/node
RUN npm install
WORKDIR /app

# Install python modules
COPY --chown=vv8:vv8 ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

# Copy app
COPY --chown=vv8:vv8 ./vv8_worker ./vv8_worker

CMD celery -A vv8_worker.app.app worker -Q url -l INFO
