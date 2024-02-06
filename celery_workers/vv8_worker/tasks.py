import subprocess as sp
import os
from signal import SIGINT
import os.path
import glob
import shutil
import time
import multiprocessing as m
from typing import List, Optional, TypedDict
from bson import ObjectId
import random
import fasteners
from vv8_worker.app import celery_app
from vv8_worker.config.mongo_config import GridFSTask



# PROXY_COMMAND = "/usr/local/web_page_replay_go/wpr record --inject_scripts /usr/local/web_page_replay_go/deterministic.js --https_cert_file /usr/local/web_page_replay_go/ecdsa_cert.pem,/usr/local/web_page_replay_go/wpr_cert.pem --https_key_file /usr/local/web_page_replay_go/ecdsa_key.pem,/usr/local/web_page_replay_go/wpr_key.pem --http_port {} --https_port {} {}"
PROXY_COMMAND = ["/usr/local/web_page_replay_go/wpr", "record", "--inject_scripts", "/usr/local/web_page_replay_go/deterministic.js", "--https_cert_file", "/usr/local/web_page_replay_go/ecdsa_cert.pem,/usr/local/web_page_replay_go/wpr_cert.pem", "--https_key_file", "/usr/local/web_page_replay_go/ecdsa_key.pem,/usr/local/web_page_replay_go/wpr_key.pem"]
dirname = os.path.dirname(__file__)

class CrawlerConfig(TypedDict):
    disable_screenshot: bool
    disable_har: bool
    disable_artifact_collection: bool
    crawler_args: List[str]
    mongo_id: Optional[str]
    delete_log_after_parsing: bool


def remove_entry(filepath):
    if os.path.isdir(filepath):
        shutil.rmtree(filepath)
    else:
        os.remove(filepath)


@celery_app.task(base=GridFSTask, bind=True, name='vv8_worker.process_url')
def process_url(self, url: str, submission_id: str, config: CrawlerConfig):
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
    if config['disable_screenshot']:
        config['crawler_args'].append('--disable-screenshot')
    if not config['disable_har']:
        proxy_launched = False
        print("Starting proxy!")
        while not proxy_launched:
            http_proxy = random.randint(2024, 60000)
            https_proxy = random.randint(2024, 60000)
            http_lock = fasteners.InterProcessLock(f'/tmp/http_proxy_{http_proxy}.lock')
            https_lock = fasteners.InterProcessLock(f'/tmp/https_proxy_{https_proxy}.lock')
            if not http_lock.acquire(blocking=False) or not https_lock.acquire(blocking=False):
                continue
            http_lock.acquire()
            https_lock.acquire()
            # --host-resolver-rules="MAP *:80 127.0.0.1:AAAA,MAP *:443 127.0.0.1:BBBB,EXCLUDE localhost" --ignore-certificate-errors-spki-list=PhrPvGIaAMmd29hj8BCZOq096yj7uMpRNHpn5PDxI6I=,2HcXCSKKJS0lEXLQEWhpHUfGuojiU0tiT5gOF9LP6IQ=
            config['crawler_args'].append(f'--host-resolver-rules="MAP *:80 127.0.0.1:{http_proxy},MAP *:443 127.0.0.1:{https_proxy},EXCLUDE localhost"')
            config['crawler_args'].append(f'--ignore-certificate-errors-spki-list=PhrPvGIaAMmd29hj8BCZOq096yj7uMpRNHpn5PDxI6I=,2HcXCSKKJS0lEXLQEWhpHUfGuojiU0tiT5gOF9LP6IQ=')
            proxy_proc = sp.Popen(PROXY_COMMAND + ["--http_port", str(http_proxy), "--https_port", str(https_proxy), f'{wd_path}/{submission_id}.har'], stdout=sp.DEVNULL, stderr=sp.DEVNULL)
            # wait for proxy to launch
            time.sleep(3)                
            if proxy_proc.poll() is None:
                proxy_launched = True
            else:
                http_lock.release()
                https_lock.release()
                raise Exception("Proxy failed")
                

    print(config['crawler_args'])
    ret_code = -1
    crawler_proc = sp.Popen(
        [
            'node',
            crawler_path,
            'visit',
            url,
            str(submission_id)] + config['crawler_args'],
        cwd=wd_path,
    )
    try:
        ret_code = crawler_proc.wait(timeout=config['hard_timeout'])
    except sp.TimeoutExpired as _:
        print('Browser process forcibly killed due to timeout being exceeded')
        sp.run(['pkill', '-P', f'{crawler_proc.pid}'])
        crawler_proc.kill()
    self.update_state(state='PROGRESS', meta={
        'status': 'Uploading artifacts to mongodb'
    })
    if proxy_launched:
        proxy_proc.send_signal(SIGINT)
        while proxy_proc.poll() is None: # wait till the proxy exists!
            time.sleep(1)
        http_lock.release()
        https_lock.release()
    screenshot_ids = []
    for screenshot in glob.glob(f'{wd_path}/*.png'):
        if not config['disable_screenshot']:
            shutil.copy(screenshot,
                        f"/app/screenshots/{screenshot.split('/')[-1]}" 
                        )
            if not config['disable_artifact_collection']:
                file_id = self.gridfs.upload_from_stream(
                    screenshot,
                    open(screenshot, 'rb'),
                    chunk_size_bytes=1024 * 1024,
                    metadata={"contentType": "image/png"})
                screenshot_ids.append(file_id)
        os.remove(screenshot)
    har_ids = []
    for har in glob.glob(f"{wd_path}/*.har"):
        if not config['disable_har']:
            shutil.copy(har, f"/app/har/{har.split('/')[-1]}")
            if (not config['disable_artifact_collection']):
                file_id = self.gridfs.upload_from_stream(
                    har,
                    open(har, 'rb'),
                    chunk_size_bytes=1024 * 1024,
                    metadata={"contentType": "text/plain"}) 
                har_ids.append(file_id)
            os.remove(har)
    log_ids = []
    for entry in glob.glob(os.path.join(wd_path, 'vv8*.log')):
        if not config['disable_artifact_collection']:
            file_id = self.gridfs.upload_from_stream(
                entry,
                open(entry, 'rb'),
                chunk_size_bytes=1024 * 1024,
                metadata={"contentType": "text/plain"})
            log_ids.append(file_id)
    if not config['disable_artifact_collection']:
        self.mongo['vv8_logs'].update_one(
            {'_id': ObjectId(config['mongo_id'])},
            {'$set': {
                'screenshot_ids': screenshot_ids,
                'har_ids': har_ids,
                'log_ids': log_ids
            }})
    if ret_code != 0:
        if config['delete_log_after_parsing']:
            shutil.rmtree(wd_path)
        raise Exception('Crawler failed')
    end = time.perf_counter()
    self.update_state(state='SUCCESS', meta={
        'status': 'Crawling done',
        'time': end - start,
        'end_tSime': time.time()})
