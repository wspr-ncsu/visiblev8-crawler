import subprocess as sp
import os
import os.path
import glob
import shutil

from vv8_worker.app import celery_app


dirname = os.path.dirname(__file__)


def remove_entry(filepath):
    if os.path.isdir(filepath):
        shutil.rmtree(filepath)
    else:
        os.remove(filepath)


@celery_app.task(bind=True, name='vv8_worker.process_url')
def process_url(self, url, submission_id):
    print(f'vv8_worker process_url: url: {url}, submission_id: {submission_id}')
    crawler_path = os.path.join('/app', 'node/crawler.js')
    if not os.path.isfile(crawler_path):
        raise Exception(f'Crawler script cannot be found or does not exist. Expected path: {crawler_path}')
    base_wd_path = os.path.join(dirname, 'raw_logs')
    if not os.path.isdir(base_wd_path):
        os.mkdir(base_wd_path)
    # create working directory for this task
    wd_path = os.path.join(base_wd_path, submission_id)
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
        ['node', crawler_path, 'visit', url, str(submission_id)],
        cwd=wd_path
    )
    crawler_proc.wait()
    for screenshot in glob.glob("{}/*.png".format(wd_path)):
        shutil.copy(screenshot, "/app/screenshots/{}".format(screenshot.split("/")[-1]))
        os.remove(screenshot)
    for har in glob.glob("{}/*.har".format(wd_path)):
        shutil.copy(har, "/app/har/{}".format(har.split("/")[-1]))
        os.remove(har)
