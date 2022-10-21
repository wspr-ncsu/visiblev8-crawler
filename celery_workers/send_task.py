#!/usr/bin/env python3.8

import os
from dotenv import load_dotenv

load_dotenv()
VV8_CELERY_BROKER=os.getenv('VV8_CELERY_BROKER')
VV8_CELERY_BROKER_PORT=os.getenv('VV8_CELERY_BROKER_PORT')
VV8_CELERY_ID=os.getenv('VV8_CELERY_ID')
VV8_CELERY_BACKEND_USER=os.getenv('VV8_CELERY_BROKER')
VV8_CELERY_BACKEND_PASSWORD=os.getenv('VV8_CELERY_BACKEND_PASSWORD')
VV8_CELERY_BACKEND_HOST=os.getenv('VV8_CELERY_BACKEND_HOST')
VV8_CELERY_BACKEND_PORT=os.getenv('VV8_CELERY_BACKEND_PORT')
VV8_CELERY_BACKEND_DATABASE=os.getenv('VV8_CELERY_BACKEND_DATABASE')


from vv8_worker.tasks import process_url
from celery import *


def main():
    url = "https://www.csc.ncsu.edu"
    submission_id = 1
    log = process_url.apply_async(
                kwargs={'url': url, 'submission_id': submission_id},
                queue="crawler",
                chain=[
                    signature('log_parser_worker.parse_log', kwargs={'submission_id': submission_id}, queue="log_parser")
                ]
            )
    print(log)

if __name__ == "__main__":
    main()

