import vv8web_task_queue.tasks as tasks


def schedule_process_url_task(url):
    print(f'schedule process_url_task')
    tasks.process_url_task.apply_async((url,))
