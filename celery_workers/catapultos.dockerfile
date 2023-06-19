# syntax=docker/dockerfile:1

FROM golang:1.20

USER root

# Create vv8 user
# RUN groupadd -g 1001 -f vv8; \
#     useradd -u 1001 -g 1001 -s /bin/bash -m vv8
# ENV PATH="${PATH}:/home/vv8/.local/bin"

# install catapult
WORKDIR $GOPATH/src
# RUN mkdir src
# RUN cd src 
RUN mkdir github.com
WORKDIR $GOPATH/src/github.com
RUN mkdir catapult-project
WORKDIR $GOPATH/src/github.com/catapult-project
# RUN git clone git@github.com:catapult-project/catapult.git
RUN git clone https://github.com/catapult-project/catapult.git
WORKDIR $GOPATH/src
RUN go mod init github.com/catapult-project

# Set destination for COPY
WORKDIR /app
# RUN chown -R vv8:vv8 /app

# USER vv8

# RUN git clone git@github.com:catapult-project/catapult.git

# Download Go modules
# COPY go.mod go.sum ./
# RUN go mod download

# Copy the source code. Note the slash at the end, as explained in
# https://docs.docker.com/engine/reference/builder/#copy
# COPY *.go ./

# Build
# RUN CGO_ENABLED=0 GOOS=linux go build -o /docker-gs-ping

# EXPOSE 8080
# EXPOSE 8081

# COPY --chown=vv8:vv8 ./catapultos ./catapultos
# COPY --chown=vv8:vv8 ./catapultos/entrypoint.sh /entrypoint.sh
COPY ./catapultos ./catapultos
COPY ./catapultos/entrypoint.sh /entrypoint.sh


WORKDIR $GOPATH/src/github.com/catapult-project/catapult/web_page_replay_go

# CMD ["go version"]
CMD ["/entrypoint.sh"]
# CMD ["/bin/bash", “-c”, "go run src/wpr.go record --http_port=8080 --https_port=8081 /app/archive.wprgo"]

