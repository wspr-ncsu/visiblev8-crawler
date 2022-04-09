import requests

from vv8web_task_queue.util.log_parser_v2 import parse_log
from vv8web_task_queue.app import app


@app.task
def parse_log_task(log, submission_id):
    print(f'log_parser parse_log_task: log: {log[:30]}, submission_id: {submission_id}')
    # Nested import is used since definition to task function has to exist to schedule a task
    # This is not a pretty solution, but it is a side effect of how celery works.
    # Ideally celery would not need a function definition to schedule a task, but it is what it is
    import vv8web_task_queue.config.database_sidecar_config as db_cfg
    parsed_log_post_url = f'http://{db_cfg.db_sc_host}:{db_cfg.db_sc_port}/api/v1/parsedlog'
    parsed_log = parse_log(log, submission_id)
    # Send log data to database
    r = requests.post(parsed_log_post_url, json=parsed_log.to_json())
    # Raise error if HTTP error occured
    r.raise_for_status()
