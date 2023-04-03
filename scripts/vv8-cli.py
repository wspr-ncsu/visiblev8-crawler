import argparse
import crawl
import setup
import fetch
import docker

from enum import Enum

class Mode(Enum):
    crawl = 'crawl'
    fetch = 'fetch'
    setup = 'setup'
    docker = 'docker'

    def __str__(self):
        return self.value

def main():
    parser = argparse.ArgumentParser(prog='vv8-cli',
                    description='A cli to run basic vv8 crawler jobs from the command line')
    mode = parser.add_subparsers(dest='mode', title='various actions that can be performed using the cli')
    crawl_arg_parser = mode.add_parser(Mode.crawl.value, help='crawl a list of urls')
    crawl.crawler_parse_args(crawl_arg_parser)
    setup_arg_parser = mode.add_parser(Mode.setup.value, help='setup vv8 cli and crawler (in case you want to run the crawler locally)')
    setup.setup_parse_args(setup_arg_parser)
    fetch_arg_parser = mode.add_parser(Mode.fetch.value, help='fetch some attributes of a submission')
    fetch.fetch_parse_args(fetch_arg_parser)
    docker_arg_parser = mode.add_parser(Mode.docker.value, help='manage local docker instance of vv8-crawler server, only available for local installs')
    docker.docker_parse_args(docker_arg_parser)

    opts, unkown_args = parser.parse_known_args()


    if opts.mode != Mode.crawl.value and unkown_args:
        print('ignoring unknown args: ', unkown_args)
        parser.print_usage()
        return

    match opts.mode:
        case Mode.crawl.value:
            crawl.crawler(opts, unkown_args)
        case Mode.setup.value:
            setup.setup(opts)
        case Mode.fetch.value:
            fetch.fetch(opts)
        case Mode.docker.value:
            docker.docker(opts)

if __name__ == '__main__':
    main()