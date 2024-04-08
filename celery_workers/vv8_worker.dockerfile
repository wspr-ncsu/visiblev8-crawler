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

# COPY ./chromium_112_no_fv8.deb .
# RUN apt install -y ./chromium_112_no_fv8.deb

# THIS WAS THE PREVIOUS ONE
# COPY ./chromium_112_fv8_July1.deb .
# RUN apt install -y ./chromium_112_fv8_July1.deb

COPY ./chromium_122_fv8_Apr24.deb .
RUN apt install -y ./chromium_122_fv8_Apr24.deb


ENV DISPLAY :99
ENV XDG_CURRENT_DESKTOP XFCE

# Add the missing GPG key for the Google Chrome repository
# RUN apt-get update && \
#     apt install -y gnupg && \
#     apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E88979FB9B30ACF2 && \
#     apt-get update

# RUN apt-get update && \
#     apt-get install -y gnupg && \
#     apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys E88979FB9B30ACF2 && \
#     apt-get update

# RUN apt-get update && apt-get install -y gnupg
# RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E88979FB9B30ACF2
# RUN apt-get update

# RUN apt-get update && apt-get install -y wget gnupg
# RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
# RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list
# RUN apt-get update

RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
RUN sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN sudo apt update
RUN sudo apt install google-chrome-stable



RUN apt update && \
    apt install -y curl && \
    apt install -y --no-install-recommends xvfb && \
    apt install -y --no-install-recommends xauth && \
    apt install -y libnss3-dev && \
    apt install -y libgbm-dev && \
    apt install -y libasound2-dev && \
    apt install -y --no-install-recommends xfce4 && \
    apt install -y --no-install-recommends xdg-utils && \
    apt-get install -y tigervnc-standalone-server && \
    apt install -y tigervnc-common && \ 
    apt install -y gnome-terminal && \
    apt install -y procps
# Gnome-terminal is for debugging purposes

# Create vv8 user
RUN groupadd -g 1001 -f vv8; \
    useradd -u 1001 -g 1001 -s /bin/bash -m vv8
ENV PATH="${PATH}:/home/vv8/.local/bin"

RUN     git clone --branch v1.4.0 --single-branch https://github.com/novnc/noVNC.git /opt/noVNC; \
    git clone --branch v0.11.0 --single-branch https://github.com/novnc/websockify.git /opt/noVNC/utils/websockify; \
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

CMD ["/entrypoint.sh"]
