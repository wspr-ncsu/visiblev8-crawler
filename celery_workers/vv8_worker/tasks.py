import subprocess as sp
import os
import os.path
import glob
import shutil
import time
from typing import List
from bson import ObjectId

from vv8_worker.app import celery_app
from vv8_worker.config.mongo_config import GridFSTask

dirname = os.path.dirname(__file__)

def remove_entry(filepath):
    if os.path.isdir(filepath):
        shutil.rmtree(filepath)
    else:
        os.remove(filepath)


@celery_app.task(base=GridFSTask, bind=True, name='vv8_worker.process_url')
def process_url(self, url: str, submission_id: str, mongo_id: str, disable_har: bool, disable_screenshot: bool, disable_artifact_collection: bool, crawler_args: List[str]):
    print(f'vv8_worker process_url: url: {url}, submission_id: {submission_id}')
    start = time.perf_counter()
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
    self.update_state(state='PROGRESS', meta={'status': 'Running crawler'})
    if disable_screenshot:
        crawler_args.append('--disable-screenshot')
    print(crawler_args)
    crawler_proc = sp.Popen(
        ['node', crawler_path, 'visit', url, str(submission_id)] + crawler_args,
        cwd=wd_path
    )
    crawler_proc.wait()
    self.update_state(state='PROGRESS', meta={'status': 'Uploading artifacts to mongodb'})
    screenshot_ids = []
    for screenshot in glob.glob("{}/*.png".format(wd_path)):
        if not disable_screenshot:
            shutil.copy(screenshot, "/app/screenshots/{}".format(screenshot.split("/")[-1]))
            if ( not disable_artifact_collection ):
                file_id = self.gridfs.upload_from_stream(screenshot, open(screenshot, 'rb'), chunk_size_bytes=1024 * 1024, metadata={"contentType": "image/png"})
                screenshot_ids.append(file_id)
        os.remove(screenshot)
    har_ids = []
    for har in glob.glob("{}/*.har".format(wd_path)):
        if not disable_har:
            shutil.copy(har, "/app/har/{}".format(har.split("/")[-1]))
            if (not disable_artifact_collection):
                file_id = self.gridfs.upload_from_stream(har, open(har, 'rb'), chunk_size_bytes=1024 * 1024, metadata={"contentType": "text/plain"})
                har_ids.append(file_id)
            os.remove(har)
    log_ids = []
    for entry in glob.glob(os.path.join(wd_path, 'vv8*.log')):
        if (not disable_artifact_collection):
            file_id = self.gridfs.upload_from_stream(entry, open(entry, 'rb'), chunk_size_bytes=1024 * 1024, metadata={"contentType": "text/plain"})
            log_ids.append(file_id)
    if (not disable_artifact_collection):
        self.mongo['vv8_logs'].update_one({ '_id': ObjectId(mongo_id) }, { '$set': { 'screenshot_ids': screenshot_ids, 'har_ids': har_ids, 'log_ids': log_ids } })
    if crawler_proc.returncode != 0:
        raise Exception('Crawler failed')
    end = time.perf_counter()
    self.update_state(state='SUCCESS', meta={'status': 'Crawling done', 'time': end - start, 'end_time': time.time()})
