import vv8web_task_queue.tasks as tasks


def schedule_process_url_task(url, submission_id):
    tasks.process_url_task.apply_async((url, submission_id))


def schedule_log_parse_task(log, submission_id):
    tasks.parse_log_task.apply_async((log, submission_id))
