FROM visiblev8/vv8-base:latest

FROM python:3.10

USER root

COPY ./vv8_worker/chromium-build-deps.sh ./

RUN apt-get update && apt install -y lsb-release;

# Install nodejs, npm
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash -

# Install chromium dependencies
RUN apt install -y --no-install-recommends nodejs file sudo; \
    ./chromium-build-deps.sh \
        --no-syms \
        --no-arm \
        --no-chromeos-fonts \
        --no-nacl \
        --no-backwards-compatible \
        --no-prompt

# Copy chromium with VV8
COPY --from=visiblev8/vv8-base:latest /opt/chromium.org/chromium/ /opt/chromium.org/chromium/
COPY --from=visiblev8/vv8-base:latest /artifacts/ /artifacts/


ENV DISPLAY :99
ENV XDG_CURRENT_DESKTOP XFCE

RUN apt update && \
    apt install -y curl && \
    apt install -y --no-install-recommends xvfb && \
    apt install -y --no-install-recommends xauth && \
    apt install -y libnss3-dev && \
    apt install -y libgbm-dev && \
    apt install -y libasound2-dev && \
    apt install -y --no-install-recommends xfce4 && \
    apt install -y --no-install-recommends xdg-utils

# Create vv8 user
RUN groupadd -g 1001 -f vv8; \
    useradd -u 1001 -g 1001 -s /bin/bash -m vv8
ENV PATH="${PATH}:/home/vv8/.local/bin"

WORKDIR /app
RUN chown -R vv8:vv8 /app

USER vv8

# Add working dir to python path
ENV PYTHONPATH "${PYTHONPATH}:/app"

VOLUME /app/node
# Move vv8 crawler to app dir
COPY --chown=vv8:vv8 ./vv8_worker/vv8_crawler/package.json ./node/package.json
WORKDIR /app/node
RUN npm install --loglevel verbose
WORKDIR /app

# Install python modules
COPY --chown=vv8:vv8 ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

# Copy app
COPY --chown=vv8:vv8 ./vv8_worker ./vv8_worker

# make sure we can run without a UI
ENV DISPLAY :99

CMD Xvfb -listen tcp :99 -screen 0 1280x720x24 -ac & celery -A vv8_worker.app worker -Q crawler -l INFO -c ${CELERY_CONCURRENCY}
