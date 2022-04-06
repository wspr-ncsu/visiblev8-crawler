import subprocess as sp
import os
import os.path
import glob
import shutil

from vv8web_task_queue.app import app


dirname = os.path.dirname(__file__)


def remove_entry(filepath):
    if os.path.isdir(filepath):
        shutil.rmtree(filepath)
    else:
        os.remove(filepath)


@app.task(bind=True)
def process_url_task(self, url, submission_id):
    print(f'vv8_worker process_url: url: {url}, submission_id: {submission_id}')
    crawler_path = os.path.join('/app', 'node/crawler.js')
    if not os.path.isfile(crawler_path):
        raise Exception(f'Crawler script cannot be found or does not exist. Expected path: {crawler_path}')
    base_wd_path = os.path.join(dirname, 'wd')
    if not os.path.isdir(base_wd_path):
        os.mkdir(base_wd_path)
    # create working directory for this task
    wd_path = os.path.join(base_wd_path, self.request.id)
    if os.path.exists(wd_path):
        # Remove all files from working directory
        for entry in glob.glob(os.path.join(wd_path, '*')):
            remove_entry(entry)
    else:
        os.mkdir(wd_path)
    with os.scandir(wd_path) as dir_it:
        for entry in dir_it:
            raise Exception('Working directory should be empty')
    # Run crawler
    crawler_proc = sp.Popen(
        ['node', crawler_path, 'visit', url],
        cwd=wd_path
    )
    crawler_proc.wait()
    # check for log
    with os.scandir(wd_path) as dir_it:
        logs = []
        for entry in dir_it:
            assert entry.is_file()
            assert entry.name.endswith('.log')
            with open(entry.path, 'rt') as fp:
                log = fp.read()
                if log[-1] != '\n':
                    log += '\n'
                logs.append(log)
    # Delete task working dir
    shutil.rmtree(wd_path)
    # Send logs to log_parser
    full_log = ''.join(logs)
    return full_log
