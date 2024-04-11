import argparse
from typing import List
import requests
import local_data_store
import docker
import csv
from datetime import datetime
import time


class Crawler:
    def __init__(
        self,
        output_format: str,
        post_processors: str,
        delete_log_after_parsing: bool,
        disable_artifact_collection: bool,
        disable_screenshots: bool,
        disable_har: bool,
        crawler_args: List[str],
        hard_timeout: int,
    ):
        self.output_format = output_format
        self.post_processors = post_processors
        self.delete_log_after_parsing = delete_log_after_parsing
        self.disable_artifact_collection = disable_artifact_collection
        self.disable_screenshots = disable_screenshots
        self.disable_har = disable_har
        self.crawler_args = crawler_args
        self.hard_timeout = hard_timeout
        self.prefetch_count = 128
        self.data_store = local_data_store.init()
        if self.data_store.server_type == "local":
            docker.wakeup(self.data_store.data_directory)

<<<<<<< HEAD
    def crawl(self, urls: List[str]) -> str:
=======
        if self.data_store.server_type == 'local':
            requests.get(f'http://{self.data_store.hostname}:5555/api/workers?refresh=1')
            print('Refreshing workers')
            req = requests.get(f'http://{self.data_store.hostname}:5555/api/workers')
            workers = req.json()
            for ke in workers:
                self.prefetch_count = workers[ke]["stats"]["prefetch_count"]
            print('Setting up prefetch counter')



    def crawl(self, urls: List[str])-> str:
>>>>>>> 8ba1f06f485deb315de7521588beff0172852b3a
        r = None
        submission_identifiers = []
        for url in urls:
            url = url.rstrip("\n")
            r = None
            while True:
                if self.data_store.server_type == 'local':
                    # Use the celery api to check if we have too many reserved tasks ?
                    req = requests.get(f'http://{self.data_store.hostname}:5555/api/tasks?state=RECEIVED')
                    if req.status_code != 200:
                        raise Exception(f'Failed to get workers from celery api. Status code: {req.status_code}')
                    else:
                        tasks = req.json()
                        no_of_tasks = 0
                        for _ke in tasks:
                            no_of_tasks += 1
                        if no_of_tasks >= self.prefetch_count:
                            print('Server is overloaded, sleep for some time')
                            time.sleep(5)
                        else:
                            break

            if self.post_processors:
                print(
                    {
                        "url": url,
                        "rerun": True,
                        "crawler_args": self.crawler_args,
                        "disable_artifact_collection": self.disable_artifact_collection,
                        "disable_screenshots": self.disable_screenshots,
                        "disable_har": self.disable_har,
                        "hard_timeout": self.hard_timeout,
                        "parser_config": {
                            "parser": self.post_processors,
                            "delete_log_after_parsing": self.delete_log_after_parsing,
                            "output_format": self.output_format,
                        },
                    }
                )
                r = requests.post(
                    f"http://{self.data_store.hostname}:4000/api/v1/urlsubmit",
                    json={
                        "url": url,
                        "rerun": True,
                        "crawler_args": self.crawler_args,
                        "disable_artifact_collection": self.disable_artifact_collection,
                        "disable_screenshots": self.disable_screenshots,
                        "disable_har": self.disable_har,
                        "hard_timeout": self.hard_timeout,
                        "parser_config": {
                            "parser": self.post_processors,
                            "delete_log_after_parsing": self.delete_log_after_parsing,
                            "output_format": self.output_format,
                        },
                    },
                )
            else:
                r = requests.post(
                    f"http://{self.data_store.hostname}:4000/api/v1/urlsubmit",
                    json={
                        "url": url,
                        "rerun": True,
                        "disable_screenshots": self.disable_screenshots,
                        "disable_har": self.disable_har,
                    },
                )
            submission_id = r.json()["submission_id"]
            submission_identifiers.append((submission_id, url, datetime.now()))
        self.data_store.db.executemany(
            "INSERT INTO submissions VALUES ( ?, ?, ? )", submission_identifiers
        )
        self.data_store.commit()


def crawler(args: argparse.Namespace, unknown_args: list[str]):
    output_format = args.output_format
    parsers = args.post_processors
    delete_log_after_parsing = args.delete_log_after_parsing
    disable_artifact_collection = args.disable_artifact_collection
    disable_screenshots = args.disable_screenshots
    disable_har = args.disable_har
    hard_timeout = int(args.timeout)
    crawler_args = unknown_args
    crawler_inst = Crawler(
        output_format,
        parsers,
        delete_log_after_parsing,
        disable_artifact_collection,
        disable_screenshots,
        disable_har,
        crawler_args,
        hard_timeout,
    )
    if args.url:
        crawler_inst.crawl([args.url])
    elif args.file:
        with open(args.file, "r") as f:
            urls = f.readlines()
            crawler_inst.crawl(urls)
    elif args.csv:
        with open(args.csv, "r") as f:
            raw_file_urls = list(csv.reader(f, delimiter=","))
            urls = []
            for data in raw_file_urls:
                urls.append(f"http://{data[1]}")
            crawler_inst.crawl(urls)
    else:
        raise Exception(
            "No url or file specified"
        )  # This should never happen, cause arg parser should show an error if neithier url or file is specified


def crawler_parse_args(crawler_arg_parser: argparse.ArgumentParser):
    urls = crawler_arg_parser.add_mutually_exclusive_group(required=True)
    urls.add_argument("-u", "--url", help="url to crawl")
    urls.add_argument(
        "-f",
        "--file",
        help="file containing list of urls to crawl seperated by newlines",
    )
    urls.add_argument(
        "-c",
        "--csv",
        help="file containing a csv in the tranco list format corresponding to the list of urls to traverse",
    )
    crawler_arg_parser.add_argument(
        "-pp", "--post-processors", help="Post processors to run on the crawled url"
    )
    crawler_arg_parser.add_argument(
        "-o",
        "--output-format",
        help="Output format to use for the parsed data",
        default="postgresql",
    )
    crawler_arg_parser.add_argument(
        "-d",
        "-dr",
        "--delete-log-after-parsing",
        help="Parser to use for the crawled url",
        action="store_true",
    )
    crawler_arg_parser.add_argument(
        "-ds",
        "--disable-screenshots",
        help="Prevents screenshots from being generated",
        action="store_true",
    )
    crawler_arg_parser.add_argument(
        "-dh",
        "--disable-har",
        help="Prevents har files from being generated",
        action="store_true",
    )
    crawler_arg_parser.add_argument(
        "-dac",
        "--disable-artifact-collection",
        help="Prevents artifacts from being uploaded to mongoDB",
        action="store_true",
    )
    crawler_arg_parser.add_argument(
        "-t",
        "--timeout",
        help="A timeout value that kills the browser after a certain amount of time has elapsed",
        default=str(10 * 60),
    )  # 10 minutes
