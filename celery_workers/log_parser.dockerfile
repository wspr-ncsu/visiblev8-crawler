FROM golang:1.20 AS gobuild

WORKDIR /postprocessors
RUN apt update
RUN apt install -y --no-install-recommends git
RUN git clone https://github.com/wspr-ncsu/visiblev8.git
WORKDIR /postprocessors/visiblev8/post-processor
#RUN go get -u github.ncsu.edu/jjuecks/vv8-post-processor
RUN go build

FROM python:3.10-slim

# Create vv8 user
RUN groupadd -g 1001 -f vv8; \
    useradd -u 1001 -g 1001 -s /bin/bash -m vv8
ENV PATH="${PATH}:/home/vv8/.local/bin" 

WORKDIR /app
RUN chown -R vv8:vv8 /app

COPY --chown=vv8:vv8 --from=gobuild ./postprocessors/visiblev8/post-processor /app/post-processors

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
