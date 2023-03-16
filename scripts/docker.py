import subprocess as sbp
import argparse
import local_data_store
import os

def wakeup(data_directory: str):
    proc = sbp.run(['docker', 'compose', 'start'], cwd=data_directory)
    if proc.returncode != 0:
        print('Failed to wake up vv8-crawler server')
        os._exit(-1)

def shutdown(data_directory: str):
    proc = sbp.run(['docker', 'compose', 'stop'], cwd=data_directory)
    if proc.returncode != 0:
        print('Failed to shutdown vv8-crawler server')
        os._exit(-1)

def remove(data_directory: str):
    proc = sbp.run(['docker', 'compose', 'down'], cwd=data_directory)
    if proc.returncode != 0:
        print('Failed to remove vv8-crawler server')
        os._exit(-1)

def create(data_directory: str, instance_count: int):
    proc = sbp.run(['docker', 'compose', 'up', '--build', '-d', '--scale', f'vv8_worker={instance_count}', '--scale', f'log_parser_worker={instance_count}'], cwd=data_directory)
    if proc.returncode != 0:
        print('Failed to create vv8-crawler server')
        os._exit(-1)

def docker(args: argparse.Namespace):
    data_store = local_data_store.init()
    if not (data_store.server_type == 'local'):
        print('vv8-crawler server is not running locally')
        os._exit(-1)
    if args.start:
        wakeup(data_store.data_directory)
    elif args.stop:
        shutdown(data_store.data_directory)
    elif args.rebuild:
        remove(data_store.data_directory)
        create(data_store.data_directory, data_store.instance_count)

def docker_parse_args(docker_arg_parser: argparse.ArgumentParser):
    docker_arg_parser.add_argument('-s', '--start', help='start the vv8-crawler server', action='store_true')
    docker_arg_parser.add_argument('-t', '--stop', help='stop the vv8-crawler server', action='store_true')
    docker_arg_parser.add_argument('-r', '--rebuild', help='rebuild the vv8-crawler server', action='store_true')