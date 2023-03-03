#!/usr/bin/env bash

source env/bin/activate # Activate python venv
cd celery_workers
. set_env.sh # Sets environmental variables from .env (host, port, credentials, etc.)
./send_task.py thousand.txt # Runs script with a thousand urls (folder also contains: one, ten, hundred, million)

