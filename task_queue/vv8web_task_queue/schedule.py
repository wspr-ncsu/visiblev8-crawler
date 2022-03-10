import vv8web_task_queue.tasks as tasks


def schedule_test_task(msg):
    import os
    hostname = os.environ['HOSTNAME']
    print(f'schedule task on {hostname}')
    tasks.test_task.apply_async((msg, hostname))


if __name__ == '__main__':
    # this is for testing scheduling on different host from worker
    import sys
    import time

    num = 1
    while True:
        if len(sys.argv) >= 2:
            schedule_test_task(f'{sys.argv[1]} ({num})')
        else:
            schedule_test_task(f'hello ({num})')
        num += 1
        time.sleep(1)
