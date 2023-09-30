import subprocess as sp
import os
import os.path
import glob
import shutil
import time
import multiprocessing as m
from typing import List, Optional, TypedDict, Tuple
from bson import ObjectId
from filelock import FileLock, Timeout
from time import sleep
import random
from vv8_worker.app import celery_app
from vv8_worker.config.mongo_config import GridFSTask

dirname = os.path.dirname(__file__)
lock_dir = '/tmp/proxylocks/'
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


def get_port(uid: str, wd : str) -> Tuple[FileLock, sp.Popen, int, str]:
    port = random.randint(9000, 9999)
    lock_file_path = os.path.join(lock_dir, f'{port}.lock')
    if os.path.exists(lock_file_path):
        port = random.randint(9000, 9999)
        lock_file_path = os.path.join(lock_dir, f'{port}.lock')
        lock = FileLock(lock_file_path)  
    lock = FileLock(lock_file_path, timeout=60)
    try:
        lock.acquire(timeout=60)
        flow_file = f'{wd}/{uid}.har'
        mitmdump_command = [
            'mitmdump',
            '-p', str(port),
            # "--certs", "*=/home/vv8/.mitmproxy/mitmproxy-ca-cert.pem",
            # "--mode", "socks5",
            "-s", "/app/vv8_worker/savehar.py",
            # "--set", f"hardump={wd}/{uid}.har",
            "-w", flow_file,
        ]
        # Start mitmdump in a subprocess
        # Wait 2 seconds for the ProxyProcess
        
        proc = sp.Popen(mitmdump_command)
        sleep(2)

    except Timeout:
        print(f"Could not acquire the lock for UID {uid}.")
        lock.release()
        return None, None, 0, f"Could not acquire the lock for UID {uid}."
    return lock, proc, port, ""
    
def release_port(fl: FileLock, pipe: sp.Popen, port: int):
    fl.release()
    pipe.terminate()
    os.remove("/tmp/proxylocks/{}.lock".format(port))
       
    
@celery_app.task(base=GridFSTask, bind=True, name='vv8_worker.process_url')
def process_url(self, url: str, submission_id: str, config: CrawlerConfig):
    print(f'vv8_worker process_url: url: {url}, submission_id: {submission_id}')
    start = time.perf_counter()
    crawler_path = os.path.join('/app', 'node/crawler.js') 
    fl, proxy_proc, proxy_port = (None, None, None)
    
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
    if not config['disable_har']:
        fl, proxy_proc, proxy_port, proxy_error = get_port(uid=str(submission_id), wd=wd_path)
        if proxy_error:
            raise Exception("Failed to start Proxy: ", proxy_error)
        config['crawler_args'].append('--proxy-server=127.0.0.1:{}'.format(proxy_port))
    # Run crawler
    self.update_state(state='PROGRESS', meta={'status': 'Running crawler'})
    if config['disable_screenshot']:
        config['crawler_args'].append('--disable-screenshot')

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
    if proxy_proc != None:
        proxy_proc.terminate()
        sleep(2)
        fl.release()
        os.remove(f"{lock_dir}{proxy_port}.lock")
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
        'end_time': time.time()})
