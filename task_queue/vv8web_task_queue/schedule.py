import vv8web_task_queue.tasks as tasks


def schedule_test_task(msg):
    import os
    hostname = os.environ['HOSTNAME']
    print(f'schedule task on {hostname}')
    tasks.test_task.apply_async((msg, hostname))


def schedule_process_url_task(url):
    print(f'schedule process_url_task')
    tasks.process_url_task.apply_async((url,))


if __name__ == '__main__':
    # this is for testing scheduling on different host from worker
    import sys
    import time

    num = 1
    while True:
        schedule_test_task(f'hello ({num})')
        schedule_process_url_task('https://google.com')
        num += 1
        time.sleep(1)
