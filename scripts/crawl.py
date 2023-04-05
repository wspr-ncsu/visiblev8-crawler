import argparse
import requests
import local_data_store
import docker
from datetime import datetime

def crawler( args: argparse.Namespace, unknown_args: list[str]):
    data_store = local_data_store.init()
    if data_store.server_type == 'local':
        docker.wakeup(data_store.data_directory)
    output_format = args.output_format
    parsers = args.post_processors
    delete_log_after_parse = args.delete_log_after_parse
    crawler_arguments = unknown_args
    if args.url:
        r = None
        if parsers:
            r = requests.post(  f'http://{data_store.hostname}:4000/api/v1/urlsubmit', json={
                'url': args.url,
                'rerun': True,
                'parser_config': {
                    'parser': parsers,
                    'delete_log_after_parsing': delete_log_after_parse,
                    'output_format': output_format
                    },
                'crawler_args': crawler_arguments
                })
        else:
            r = requests.post(  f'http://{data_store.hostname}:4000/api/v1/urlsubmit', json={
                'url': args.url,
                'rerun': True, 
                'crawler_args': crawler_arguments
            })
        submission_id = r.json()['submission_id']
        data_store.db.execute('INSERT INTO submissions VALUES ( ?, ?, ? )', (submission_id, args.url, datetime.now(),))
        data_store.commit()
    elif args.file:
        with open(args.file, 'r') as f:
            urls = f.readlines()
            submission_identifiers = []
            for url in urls:
                url = url.rstrip('\n')
                r = None
                if parsers:
                    r = requests.post(  f'http://{data_store.hostname}:4000/api/v1/urlsubmit', json={
                'url': args.url,
                'rerun': True,
                'parser_config': {
                    'parser': parsers,
                    'delete_log_after_parsing': delete_log_after_parse,
                    'output_format': output_format,
                    'crawler_args': crawler_arguments
                    }
                })
                else:
                    r = requests.post(  f'http://{data_store.hostname}:4000/api/v1/urlsubmit', json={'url': url, 'rerun': True})
                submission_id = r.json()['submission_id']
                submission_identifiers.append((submission_id, url, datetime.now()))
            data_store.db.executemany('INSERT INTO submissions VALUES ( ?, ?, ? )', submission_identifiers)
            data_store.commit()
    else:
        raise Exception('No url or file specified') # This should never happen, cause arg parser should show an error if neithier url or file is specified

def crawler_parse_args(crawler_arg_parser: argparse.ArgumentParser):
    urls = crawler_arg_parser.add_mutually_exclusive_group(required=True)
    urls.add_argument('-u', '--url', help='url to crawl')
    urls.add_argument('-f', '--file', help='file containing list of urls to crawl seperated by newlines')
    crawler_arg_parser.add_argument('-pp', '--post-processors', help='Post processors to run on the crawled url')
    crawler_arg_parser.add_argument('-o', '--output-format', help='Output format to use for the parsed data', default='postgresql')
    crawler_arg_parser.add_argument('-d', '--delete-log-after-parse', help='Parser to use for the crawled url', action='store_true')
