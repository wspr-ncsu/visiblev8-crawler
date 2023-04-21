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
    pull_proc = sbp.run(['docker', 'pull', 'visiblev8/vv8-base:latest'], cwd=data_directory)
    if pull_proc.returncode != 0:
        print('Failed to pull latest images for visiblev8 for vv8-crawler server')
        os._exit(-1)
    up_proc = sbp.run(['docker', 'compose', 'up', '--build', '-d', '--force-recreate', '--scale', f'vv8_worker={instance_count}', '--scale', f'log_parser_worker={instance_count}'], cwd=data_directory)
    if up_proc.returncode != 0:
        print('Failed to create vv8-crawler server')
        os._exit(-1)

def follow_logs(data_directory: str):
    proc = sbp.run(['docker', 'compose', 'logs', '-f'], cwd=data_directory)
    if proc.returncode != 0:
        print('Failed to follow logs of vv8-crawler server')
        os._exit(-1)

def crash_and_burn(data_directory: str, instance_count: int):
    remove(data_directory)
    burnimate_proc = sbp.run(['sudo', 'rm', '--verbose', '-rf', 'vv8db2/*', 'har/*', 'parsed_logs/*', 'raw_logs/*', 'screenshots', 'mongo/data', './scripts/.vv8.db' ], cwd=data_directory)
    if burnimate_proc.returncode != 0:
        print('Failed to remove artifacts for vv8-crawler server')
        os._exit(-1)
    crash_everything_proc = sbp.run(['sudo', 'docker', 'system', 'prune', '-a', '-f'], cwd=data_directory)
    if crash_everything_proc.returncode != 0:
        print('Failed to clear docker cache for vv8-crawler server')
        os._exit(-1)
    create(data_directory, instance_count)

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
    elif args.crash_and_burn:
        from rich import prompt
        if prompt.Confirm.ask('Are you sure you want to delete all your work and start over?', default=False):
            crash_and_burn(data_store.data_directory, data_store.instance_count)
        else:
            pass
    elif args.follow_logs:
        follow_logs(data_store.data_directory)

def docker_parse_args(docker_arg_parser: argparse.ArgumentParser):
    docker_arg_parser.add_argument('-s', '--start', help='start the vv8-crawler server', action='store_true')
    docker_arg_parser.add_argument('-t', '--stop', help='stop the vv8-crawler server', action='store_true')
    docker_arg_parser.add_argument('-r', '--rebuild', help='rebuild the vv8-crawler server', action='store_true')
    docker_arg_parser.add_argument('-f', '--follow-logs', help='follow the logs of the vv8-crawler server', action='store_true')
    docker_arg_parser.add_argument('-cb', '--crash-and-burn', help='throw way all work done on the vv8-crawler server and start over', action='store_true')