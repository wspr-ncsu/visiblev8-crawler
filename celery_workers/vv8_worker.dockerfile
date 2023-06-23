# install GoLang
# FROM golang:1.17 AS gola

# # Set destination for COPY
# WORKDIR /app

# # RUN go clean -cache
# # RUN go clean -modcache

# RUN go get github.com/catapult-project/catapult/web_page_replay_go

# # # Download Go modules
# # COPY go.mod go.sum ./
# # RUN go mod download

# # # Copy the source code. Note the slash at the end, as explained in
# # # https://docs.docker.com/engine/reference/builder/#copy
# # COPY *.go ./

# # Build
# # RUN CGO_ENABLED=0 GOOS=linux go build -o /docker-gs-ping

# # Optional:
# # To bind to a TCP port, runtime parameters must be supplied to the docker command.
# # But we can document in the Dockerfile what ports
# # the application is going to listen on by default.
# # https://docs.docker.com/engine/reference/builder/#expose
# EXPOSE 8080
# EXPOSE 8081

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
# COPY --from=visiblev8/vv8-base:latest /opt/chromium.org/chromium/ /opt/chromium.org/chromium/
# COPY --from=visiblev8/vv8-base:latest /artifacts/ /artifacts/

# COPY ./chromium_112_fv8_May1.deb .
# RUN apt install -y ./chromium_112_fv8_May1.deb

COPY ./chromium_112_no_fv8.deb .
RUN apt install -y ./chromium_112_no_fv8.deb

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
    apt install -y --no-install-recommends xdg-utils && \
    apt-get install -y tigervnc-standalone-server tigervnc-common

# Create vv8 user
RUN groupadd -g 1001 -f vv8; \
    useradd -u 1001 -g 1001 -s /bin/bash -m vv8
ENV PATH="${PATH}:/home/vv8/.local/bin"

RUN     git clone --branch v1.2.0 --single-branch https://github.com/novnc/noVNC.git /opt/noVNC; \
    git clone --branch v0.9.0 --single-branch https://github.com/novnc/websockify.git /opt/noVNC/utils/websockify; \
    ln -s /opt/noVNC/vnc.html /opt/noVNC/index.html

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

COPY ./vv8_worker/entrypoint.sh /entrypoint.sh

# make sure we can run without a UI
ENV DISPLAY :99

ENV DISPLAY=:1 \
    VNC_PORT=5901 \
    NO_VNC_PORT=6901 \
    VNC_COL_DEPTH=32 \
    VNC_RESOLUTION=1920x1080

# TODO: spawn catapult
# we are gonna have 30 instances of catapult
# copy catapult files from gola
# COPY --from=gola /usr/local/go/ /usr/local/go/
# COPY --from=gola /app/ /app/

CMD ["/entrypoint.sh"]

# how to install on Ubuntu
# sudo apt install golang-go
# go get github.com/catapult-project/catapult/web_page_replay_go
# /home/npantel/go/src/github.com/catapult-project/catapult/web_page_replay_go

# cd $HOME/go or $HOME/Projects/Go on VM vv8Build
# mkdir src/github.com/catapult-project
# cd src/github.com/catapult-project
# git clone git@github.com:catapult-project/catapult.git
# cd $HOME/go/src/ or HOME/Projects/Go/src on VM vv8Build
# go mod init github.com/catapult-project

# cd path_to_web_page_replay_go
# go run src/wpr.go record --http_port=8080 --https_port=8081 /tmp/archive.wprgo

# other tab:
# run chrome with flags