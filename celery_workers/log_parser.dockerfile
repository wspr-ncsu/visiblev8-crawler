FROM golang:1.20 AS build

WORKDIR /postprocessors
RUN apt update
RUN apt install -y --no-install-recommends git make build-essential curl
RUN git clone https://github.com/sohomdatta1/visiblev8.git
WORKDIR /postprocessors/visiblev8/post-processor
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
ENV PATH="${PATH}:/root/.cargo/bin" 
RUN git pull origin multiorigin
RUN go build .

FROM visiblev8/vv8-base:latest as vv8

FROM python:3.10-slim

# Create vv8 user
RUN groupadd -g 1001 -f vv8; \
    useradd -u 1001 -g 1001 -s /bin/bash -m vv8
ENV PATH="${PATH}:/home/vv8/.local/bin" 

WORKDIR /app
RUN chown -R vv8:vv8 /app

COPY --chown=vv8:vv8 --from=vv8 /artifacts/ /artifacts/
COPY --chown=vv8:vv8 --from=build ./postprocessors/visiblev8/post-processor/ /app/post-processors

VOLUME /workdir

USER vv8

# Add working dir to python path
ENV PYTHONPATH "${PYTHONPATH}:/app"

# Install python modules
COPY --chown=vv8:vv8 ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

# Copy app
COPY --chown=vv8:vv8 ./log_parser_worker ./log_parser_worker

CMD celery -A log_parser_worker.app worker -Q log_parser -l INFO
