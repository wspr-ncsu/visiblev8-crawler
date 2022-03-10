from vv8web_task_queue.app import app


@app.task
def test_task(msg, sender_name):
    import os
    hostname = os.environ['HOSTNAME']
    return f'processed: "{msg}" from {sender_name} on {hostname}'
