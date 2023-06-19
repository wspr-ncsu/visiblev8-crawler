#!/bin/bash

# INDIR="celery_workers/vv8_worker/vv8_crawler/extensionsSome/"
# INDIR="celery_workers/vv8_worker/vv8_crawler/extracted/"
# INDIR="celery_workers/vv8_worker/vv8_crawler/extensionsDefault129/"
# INDIR="celery_workers/vv8_worker/vv8_crawler/selected_extensions/"

# TODO:
# 1) docker compose down
# 1b) delete some of the stuff, not the DB, not the raw_logs
    # sudo rm -rf har/ redis_data/ parsed_logs/ screenshots/ mongo/data/ ./scripts/.vv8.db
# 1c) maybe add the docker remove and the docker stop/start stuff from here: https://github.com/moby/moby/issues/10589#issuecomment-222468296
# 2) docker setup -y -y -160 -y
# 3) requeue next URL [eg: [2] of list of [12-15]

INDIR="celery_workers/vv8_worker/vv8_crawler/ALL_EXTENSIONS40k/"

for i in {0..1}
do
    first="$i"
    last="$((i+1))"
    session_name="queue-$i"
    tmux new-session -d -s $session_name "bash python3 queue.py -i $INDIR -s $first -e $last"
done

# first=0
# last=1
# INDIR="celery_workers/vv8_worker/vv8_crawler/ALL_EXTENSIONS40k/"
# # INDIR="celery_workers/vv8_worker/vv8_crawler/out_mal_ext_34/"
# python3 queue.py -i $INDIR -s $first -e $last

# tmux new-session -d -s my_session 'ruby run.rb'

#   catapultos:
    # restart: unless-stopped
    # ports:
    #   - "8080:8080/tcp"
    #   - "8081:8081/tcp"
    # build:
    #   context: ./celery_workers
    #   dockerfile: catapultos.dockerfile
    # image: catapultos