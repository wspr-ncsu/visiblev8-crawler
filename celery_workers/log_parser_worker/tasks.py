import requests
from log_parser_worker import log_parser
from log_parser_worker.app import celery_app
import log_parser_worker.config.database_sidecar_config as cfg
import time


@celery_app.task(name='log_parser_worker.parse_log')
def parse_log(log, submission_id):
    print(f'log_parser parse_log_task: log: {log[:30]}, submission_id: {submission_id}')
    # Nested import is used since definition to task function has to exist to schedule a task
    # This is not a pretty solution, but it is a side effect of how celery works.
    # Ideally celery would not need a function definition to schedule a task, but it is what it is
    parsed_log_post_url = f'http://{cfg.db_sc_host}:{cfg.db_sc_port}/api/v1/parsedlog'
    parsed_log = log_parser.parse_log(log, submission_id)
    # Send log data to database
    r = requests.post(parsed_log_post_url, json=parsed_log.to_json())
    # Raise error if HTTP error occured
    r.raise_for_status()
