import argparse
from enum import Enum

from bson import ObjectId
import local_data_store
import docker
import os
import requests
from rich.console import Console
from rich.table import Table
import datetime
import json
from rich.json import JSON
from pymongo import MongoClient
import gridfs

class MetaDataType(Enum):
    status = 'status'
    screenshot = 'screenshots'
    har = 'hars'
    raw_log = 'raw_logs'

    def __str__(self):
        return self.value
    
def format_row(table: Table, status, row):
    args = (row[0], row[1], row[2], JSON(json.dumps(status['crawler_args'])))
    vv8_worker_status = status['vv8_worker_status']
    vv8_worker_row = ()
    if vv8_worker_status == 'SUCCESS':
        vv8_worker_status = f"[green]{vv8_worker_status}[/green]"
        if status['vv8_worker_info']['time']:
            vv8_worker_row = (vv8_worker_status,
                            f"{status['vv8_worker_info']['time']} seconds",
                            datetime.datetime.fromtimestamp(status['vv8_worker_info']['end_time'])
                            .strftime('%Y-%m-%d %H:%M:%S'))
    elif vv8_worker_status == 'FAILURE':
        vv8_worker_status = f"[red]{vv8_worker_status}, {status['vv8_worker_info']['status']}[/red]"
        vv8_worker_row = (vv8_worker_status, None, None)
    else:
        if status['vv8_worker_info'] is None:
            vv8_worker_row = (vv8_worker_status, None, None)
        else:
            vv8_worker_status = f"[yellow]{status['vv8_worker_info']['status']}[/yellow]"
            vv8_worker_row = (vv8_worker_status, None, None)
    if not status['log_parser_was_executed']:
        args += vv8_worker_row
        table.add_row(*args)
        return
    post_processors_data = (
        status['postprocessors_used'],
        status['postprocessors_output_format'],
        str(status['postprocessors_delete_log_after_parsing'])
    )
    log_parser_worker_status = status['log_parser_worker_status']
    log_parser_worker_row = []
    if log_parser_worker_status == 'SUCCESS':
        log_parser_worker_status = f"[green]{log_parser_worker_status}[/green]"
        log_parser_worker_row = (log_parser_worker_status,
                                f"{status['log_parser_worker_info']['time']} seconds",
                                datetime.datetime.fromtimestamp(status['log_parser_worker_info']['end_time'])
                                .strftime('%Y-%m-%d %H:%M:%S'))
    elif log_parser_worker_status == 'FAILURE':
        log_parser_worker_status = f"[red]{log_parser_worker_status}, {status['log_parser_worker_info']['status']}[/red]"
        log_parser_worker_row = (log_parser_worker_status, None, None)
    else:
        if status['log_parser_worker_info'] is None:
            log_parser_worker_row = (log_parser_worker_status, None, None)
        else:
            log_parser_worker_status = f"[yellow]{status['log_parser_worker_info']['status']}[/yellow]"
            log_parser_worker_row = (log_parser_worker_status, None, None)
    args += vv8_worker_row
    args += post_processors_data
    args += log_parser_worker_row
    table.add_row(*args)


def fetch(args: argparse.Namespace):
    data_store = local_data_store.init()
    if data_store.server_type == 'local':
        docker.wakeup(data_store.data_directory)
    url_data = data_store.db.execute('SELECT * FROM submissions WHERE url = ?', (args.url,)).fetchall()
    submission_id = None
    if url_data is None:
        print('could not find submission for url')
        os._exit(-1)
        return
    match args.metadata_type:
            case MetaDataType.status:
                table = Table(title="VisibleV8 Submissions")
                table.add_column("Submission UID", overflow='fold')
                table.add_column("URL", overflow='fold')
                table.add_column("Start Time", overflow='fold')
                table.add_column("Arguments used for crawler", overflow='fold')
                table.add_column("VV8 crawler task status", overflow='fold')
                table.add_column("Time taken by VV8 crawler", overflow='fold')
                table.add_column("Crawling ended at", overflow='fold')
                table.add_column("Postprocessors requested", overflow='fold')
                table.add_column("Postprocessors output format", overflow='fold')
                table.add_column("Was log deleted", overflow='fold')
                table.add_column("Log parser task status", overflow='fold')
                table.add_column("Time taken by log parser", overflow='fold')
                table.add_column("Log parsing ended at", overflow='fold')
                for row in url_data:
                    submission_id = row[0]
                    r = requests.post(f'http://{data_store.hostname}:4000/api/v1/status/{submission_id}')
                    status = r.json()
                    if r.status_code != 200:
                        continue
                    format_row(table, status, row)
                console = Console()
                console.print(table)
            case MetaDataType.screenshot:
                mgocl = MongoClient(f'mongodb://vv8:vv8@{data_store.hostname}:27017/')['admin']
                fs = gridfs.GridFS(mgocl)
                table = Table(title="Downloaded screenshots")
                table.add_column("File names")
                table.add_column("Submission UID")
                table.add_column("URL")
                table.add_column("Start Time")
                for row in url_data:
                    submission_id = row[0]
                    r = requests.post(f'http://{data_store.hostname}:4000/api/v1/status/{submission_id}')
                    if r.status_code != 200:
                        continue
                    status = r.json()
                    if status['vv8_worker_status'] == 'SUCCESS' or status['vv8_worker_status'] == 'FAILURE':
                        mongo_id = ObjectId(status['mongo_id'])
                        vv8_entry = mgocl['vv8_logs'].find_one({ '_id': mongo_id })
                        if vv8_entry is None or 'screenshot_ids' not in vv8_entry or len(vv8_entry['screenshot_ids']) == 0:
                            print(f'vv8 worker has not generated a screenshot yet for {row[1]} for submission {row[0]}')
                            continue
                        table.add_row(f'{row[0]}.png', row[0],  row[1], row[2])
                        screenshot_id = vv8_entry['screenshot_ids'][0]
                        with open(f'{submission_id}.png', 'wb') as f:
                            f.write(fs.get(screenshot_id).read())
                    else:
                        print(f'vv8 worker has not generated a screenshot yet {row[1]}')
                        os._exit(-1)
                console = Console()
                console.print(table, overflow='fold')
            case MetaDataType.har:
                mgocl = MongoClient(f'mongodb://vv8:vv8@{data_store.hostname}:27017/')['admin']
                fs = gridfs.GridFS(mgocl)
                table = Table(title="Downloaded har files")
                table.add_column("File names")
                table.add_column("Submission UID")
                table.add_column("URL")
                table.add_column("Start Time")
                for row in url_data:
                    submission_id = row[0]
                    r = requests.post(f'http://{data_store.hostname}:4000/api/v1/status/{submission_id}')
                    if r.status_code != 200:
                        continue
                    status = r.json()
                    if status['vv8_worker_status'] == 'SUCCESS' or status['vv8_worker_status'] == 'FAILURE':
                        mongo_id = ObjectId(status['mongo_id'])
                        vv8_entry = mgocl['vv8_logs'].find_one({ '_id': mongo_id })
                        if vv8_entry is None or 'har_ids' not in vv8_entry or len(vv8_entry['har_ids']) == 0:
                            print(f'vv8 worker has not generated a har file for {row[1]} for submission {submission_id}')
                            continue
                        table.add_row(f'{row[0]}.har', row[0],  row[1], row[2])
                        har_id = vv8_entry['har_ids'][0]
                        with open(f'{submission_id}.har', 'wb') as f:
                            f.write(fs.get(har_id).read())
                    else:
                        print(f'vv8 worker has not generated a har file yet {row[1]} for submission {submission_id}')
                        os._exit(-1)
                console = Console()
                console.print(table)
            case MetaDataType.raw_log:
                mgocl = MongoClient(f'mongodb://vv8:vv8@{data_store.hostname}:27017/')['admin']
                fs = gridfs.GridFS(mgocl)
                table = Table(title="Downloaded VisibleV8 logs")
                table.add_column("File names")
                table.add_column("Submission UID")
                table.add_column("URL")
                table.add_column("Start Time")
                for row in url_data:
                    submission_id = row[0]
                    r = requests.post(f'http://{data_store.hostname}:4000/api/v1/status/{submission_id}')
                    if r.status_code != 200:
                        continue
                    status = r.json()
                    if status['vv8_worker_status'] == 'SUCCESS' or status['vv8_worker_status'] == 'FAILURE':
                        mongo_id = ObjectId(status['mongo_id'])
                        vv8_entry = mgocl['vv8_logs'].find_one({ '_id': mongo_id })
                        if vv8_entry is None or 'har_ids' not in vv8_entry or len(vv8_entry['har_ids']) == 0:
                            print(f'vv8 worker has not generated a har file for {row[1]} for submission {submission_id}')
                            continue
                        log_ids = vv8_entry['log_ids']
                        os.mkdir(f'{submission_id}')
                        for log_id in log_ids:
                            table.add_row(f'{row[0]}/{log_id}.log', row[0],  row[1], row[2])
                            with open(f'{submission_id}/{log_id}.log', 'wb') as f:
                                f.write(fs.get(log_id).read())
                    else:
                        print(f'vv8 worker has not generated a har file yet {row[1]} for submission {submission_id}')
                        os._exit(-1)
                console = Console()
                console.print(table)

def fetch_parse_args(fetch_arg_parser: argparse.ArgumentParser):
    fetch_arg_parser.add_argument(dest='metadata_type', help='the type of metadata to fetch', type=MetaDataType, choices=list(MetaDataType))
    fetch_arg_parser.add_argument('url', help='the url to fetch metadata for')