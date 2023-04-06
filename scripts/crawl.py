import argparse
from typing import List
import requests
import local_data_store
import docker
import csv
from datetime import datetime

class Crawler:
    def __init__(self, output_format: str, post_processors: str, delete_log_after_parsing: bool, crawler_args: List[str]):
        self.output_format = output_format
        self.post_processors = post_processors
        self.delete_log_after_parsing = delete_log_after_parsing
        self.crawler_args = crawler_args
        self.data_store = local_data_store.init()
        if self.data_store.server_type == 'local':
            docker.wakeup(self.data_store.data_directory)


    def crawl(self, urls: List[str])-> str:
        r = None
        submission_identifiers = []
        for url in urls:
            url = url.rstrip('\n')
            r = None
            if self.post_processors:
                print({
                    'url': url,
                    'rerun': True,
                    'crawler_args': self.crawler_args,
                    'parser_config': {
                        'parser': self.post_processors,
                        'delete_log_after_parsing': self.delete_log_after_parsing,
                        'output_format': self.output_format,
                        }
                    })
                r = requests.post(  f'http://{self.data_store.hostname}:4000/api/v1/urlsubmit', json={
                    'url': url,
                    'rerun': True,
                    'crawler_args': self.crawler_args,
                    'parser_config': {
                        'parser': self.post_processors,
                        'delete_log_after_parsing': self.delete_log_after_parsing,
                        'output_format': self.output_format,
                        }
                    })
            else:
                r = requests.post(  f'http://{self.data_store.hostname}:4000/api/v1/urlsubmit', json={'url': url, 'rerun': True})
            submission_id = r.json()['submission_id']
            submission_identifiers.append((submission_id, url, datetime.now()))
        self.data_store.db.executemany('INSERT INTO submissions VALUES ( ?, ?, ? )', submission_identifiers)
        self.data_store.commit()

def crawler( args: argparse.Namespace, unknown_args: list[str]):
    output_format = args.output_format
    parsers = args.post_processors
    delete_log_after_parsing = args.delete_log_after_parsing
    crawler_args = unknown_args
    crawler_inst = Crawler(output_format, parsers, delete_log_after_parsing, crawler_args)
    if args.url:
        crawler_inst.crawl([ args.url ])
    elif args.file:
        with open(args.file, 'r') as f:
            urls = f.readlines()
            crawler_inst.crawl(urls)
    elif args.csv:
        with open(args.csv, 'r') as f:
            raw_file_urls = list(csv.reader(f, delimiter=","))
            urls = []
            for data in raw_file_urls:
                urls.append(f'http://{data[1]}')
            crawler_inst.crawl(urls)
    else:
        raise Exception('No url or file specified') # This should never happen, cause arg parser should show an error if neithier url or file is specified

def crawler_parse_args(crawler_arg_parser: argparse.ArgumentParser):
    urls = crawler_arg_parser.add_mutually_exclusive_group(required=True)
    urls.add_argument('-u', '--url', help='url to crawl')
    urls.add_argument('-f', '--file', help='file containing list of urls to crawl seperated by newlines')
    urls.add_argument('-c', '--csv', help='file containing a csv in the tranco list format corresponding to the list of urls to traverse')
    crawler_arg_parser.add_argument('-pp', '--post-processors', help='Post processors to run on the crawled url')
    crawler_arg_parser.add_argument('-o', '--output-format', help='Output format to use for the parsed data', default='postgresql')
    crawler_arg_parser.add_argument('-d', '--delete-log-after-parsing', help='Parser to use for the crawled url', action='store_true')
