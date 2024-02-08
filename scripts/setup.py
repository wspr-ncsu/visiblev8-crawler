import argparse
from pathlib import Path
from typing import Tuple
import local_data_store
import os
import time
from rich.prompt import Prompt, IntPrompt
import docker
import subprocess as sbp
import shutil

def setup(args: argparse.Namespace):
    url = 'http://localhost:4000'
    server_type = None
    instance_count = 1
    if args.local:
        (url, server_type, instance_count) = setup_local()
    else:
        type = Prompt.ask('Do you want to setup fully vv8 locally, use a remote server, or connect to remote databases?',
                              choices=['local', 'remote', 'connect'], default='local')
        if type == 'local':
            (url, server_type, instance_count) = setup_local()
        elif type == 'connect':
            (url, server_type, instance_count) = setup_local(connect_db=True)
        else:
            (url, server_type) = setup_remote()
    local_data_store.setup(url, server_type, instance_count)


def setup_local(connect_db=False):
    print('setting up local server')
    is_current_directory = Prompt.ask('Is your current directory the vv8-crawler repository? (y/n)', choices=['y', 'n'], default='y')
    if is_current_directory == 'y':
        instance_count = Prompt.ask('How many instances of browsers do you want to run?', default=f'{os.cpu_count() * 4}')
        build_postprocessors = Prompt.ask('Do you want to build the postprocessors? (y/n)', choices=['y', 'n'], default='n')
        if build_postprocessors == 'y':
            if not os.path.exists('./celery_workers/visiblev8'):
                sbp.run(['git', 'clone', 'https://github.com/wspr-ncsu/visiblev8.git', 'celery_workers/visiblev8'])
            shutil.copy( 'docker-compose.build.yaml', 'docker-compose.override.yaml' )
            sbp.run(['make', 'docker'], cwd='./celery_workers/visiblev8/post-processor')
        else:
            if os.path.exists('docker-compose.override.yaml'):
                os.remove('docker-compose.override.yaml')
        if not os.path.exists('parsed_logs'):
            os.mkdir('parsed_logs', mode=0o777)
            os.chmod('parsed_logs', 0o777)
        else:
            assert oct(os.stat('parsed_logs').st_mode)[-3:] == '777', 'parsed_logs directory exists but does not have 777 permissions'
        if not os.path.exists('screenshots'):
            os.mkdir('screenshots', mode=0o777)
            os.chmod('screenshots', 0o777)
        else:
            assert oct(os.stat('parsed_logs').st_mode)[-3:] == '777', 'parsed_logs directory exists but does not have 777 permissions'
        if not os.path.exists('har'):
            os.mkdir('har', mode=0o777)
            os.chmod('har', 0o777)
        else:
            assert oct(os.stat('har').st_mode)[-3:] == '777', 'har directory exists but does not have 777 permissions'
        if not os.path.exists('raw_logs'):
            os.mkdir('raw_logs', mode=0o777)
            os.chmod('raw_logs', 0o777)
        else:
            assert oct(os.stat('raw_logs').st_mode)[-3:] == '777', 'raw_logs directory exists but does not have 777 permissions'
        time.sleep(1)
        if connect_db:
            print('setting up connection to remote databases')
            print('configuring PostgreSQL server:')
            connect_config = {}
            connect_config['SQL_HOST'] = Prompt.ask('    Hostname:')
            connect_config['SQL_USER'] = Prompt.ask('    Username:')
            connect_config['SQL_PASSWORD'] = Prompt.ask('   Password:')
            connect_config['SQL_PORT'] = IntPrompt.ask('    Port:', default=5432)
            connect_config['SQL_DATABASE'] = Prompt.ask('    Database name:')
            
            print('configuring MongoDB server:')
            connect_config['MONGO_HOST'] = Prompt.ask('    Hostname:', default=connect_config['SQL_HOST'])
            connect_config['MONGO_USER'] = Prompt.ask('    Username:', default=connect_config['SQL_USER'])
            connect_config['MONGO_PASSWORD'] = Prompt.ask('   Password:')
            connect_config['MONGO_PORT'] = IntPrompt.ask('    Port:', default=27017)
            connect_config['MONGO_DATABASE'] = Prompt.ask('    Database name:', default=connect_config['SQL_DATABASE'])

            docker.create(Path.cwd(), int(instance_count), connect_config)
        else:
            docker.create(Path.cwd(), int(instance_count))
    else:
        print('Please run `vv8-cli setup` from inside the vv8-crawler repository')
        os._exit(-1)
    return ('0.0.0.0', 'local', instance_count)

def setup_remote() -> Tuple[str, str]:
    print('setting up cli to use remote/already setup server')
    url = Prompt.ask('What is the hostname of the vv8 crawler server?', default='localhost')
    return (url, 'remote')


def setup_parse_args(setup_arg_parser: argparse.ArgumentParser):
    setup_arg_parser.add_argument('-l', '--local', help='setup vv8 cli and crawler to use local server', action='store_true')