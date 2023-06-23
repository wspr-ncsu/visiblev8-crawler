"""Schedule crawling jobs
Usage:
    queue.py -i <indirflag>
    queue.py -i <indirflag> -s <starturl> -e <endurl>
"""
import os
from typing import List, Dict
from docopt import docopt
import subprocess
import json
from time import sleep

LAST_EXTENSION = -1  # set to ```-1``` if you want to run all extensions available

ZERO = 0
MAX_URLS = 12
URLS_VISITED = [
    "https://vv8-test.jsapi.tech/arguments-test.html",
    "https://example.com",
    "https://google.com",
    "https://cnn.com",
    "https://ebay.com",
    "https://facebook.com",
    "https://amazon.com",
    "https://tiktok.com",
    "https://youtube.com",
    "https://twitter.com",
    "https://apple.com",
    "https://microsoft.com",
]
SLEEP_EVERY = 160


def main(arguments, urls: List[str] = URLS_VISITED):
    # check if extra arguments were passed about the number of URLs we want to run on
    if arguments["<starturl>"] and arguments["<endurl>"]:
        start = int(arguments["<starturl>"])
        end = int(arguments["<endurl>"])
    else:
        start = ZERO
        end = MAX_URLS
    DIR_INPUT = arguments["<indirflag>"]
    # TODO: load dictionary, if less than 12 urls, add the stuff from url list (listA+listB)[:12]
    # add at least the first 3 from the above list
    input_dict = load_urls("url_dictionary.out")
    ext_length = len(os.listdir(DIR_INPUT))
    if LAST_EXTENSION != -1:
        ext_length = LAST_EXTENSION
    for k, each_file in enumerate(sorted(os.listdir(DIR_INPUT)[:ext_length])):
        if k % SLEEP_EVERY == 0 and k > 0:
            sleep(60)
        path = os.getcwd()
        full_path = f"{path}/{DIR_INPUT}{each_file}"
        if full_path not in input_dict.keys():
            continue
        manifest_urls = input_dict[full_path]
        # add at least 3 URLs from the chosen 12
        # if len(manifest_urls) == 12:
        #     urls = manifest_urls + URLS_VISITED[:3]
        # else:
        #     urls = manifest_urls + URLS_VISITED
        #     urls = urls[:12]
        urls = manifest_urls + URLS_VISITED
        urls = urls[:12]
        for url in sorted(urls[start:end]):
            # the directory changes here so we only want last part of directory
            initial_path = "/".join(DIR_INPUT.split("/")[-2:])
            extension_abs_path = f"{initial_path}{each_file}"
            print(extension_abs_path)
            disable_gpu = "--disable-gpu"
            disable_network_request = "--disable-features=NetworkService"
            disable_artifacts_flag = "disable_artifact_collection"
            timeout = "-t 120"
            flag_ext1 = f"--load-extension=/app/node/{extension_abs_path}"
            flag_ext2 = f"--disable-extensions-except=/app/node/{extension_abs_path}"
            # catapult1 = '--host-resolver-rules="MAP *:80 127.0.0.1:8080, MAP *:443 127.0.0.1:8081,EXCLUDE localhost" --ignore-certificate-errors-spki-list=PhrPvGIaAMmd29hj8BCZOq096yj7uMpRNHpn5PDxI6I='
            catapult1 = '--host-resolver-rules="MAP *:443 127.0.0.1:8081" --ignore-certificate-errors-spki-list=PhrPvGIaAMmd29hj8BCZOq096yj7uMpRNHpn5PDxI6I='
            # subprocess.run(
            #     [
            #         "python3",
            #         "./scripts/vv8-cli.py",
            #         "crawl",
            #         "-pp",
            #         "Mfeatures",
            #         "-d",
            #         "--show-chrome-log",
            #         flag_ext1,
            #         "-u",
            #         url
            #         # flag_ext2,
            #     ],
            #     shell=False,
            # )
            # DELETE OUTPUT
            # cmd = f"python3 ./scripts/vv8-cli.py crawl -pp Mfeatures -d --no-headless --show-chrome-log --disable-artifact-collection --disable-screenshots --disable-har {flag_ext1} {flag_ext2} -u {url}"
            # KEEP OUTPUT
            cmd = f"python3 ./scripts/vv8-cli.py crawl -pp Mfeatures --no-headless --show-chrome-log {flag_ext1} {flag_ext2} {timeout} -u {url}"
            # NOT DELETE OUTPUT + CATAPULT
            # cmd = f"python3 ./scripts/vv8-cli.py crawl -pp Mfeatures --no-headless --show-chrome-log --disable-gpu {catapult1} --js-flags='--no-lazy' {flag_ext1} {flag_ext2} -u {url}"
            # cmd = f"python3 ./scripts/vv8-cli.py crawl -pp Mfeatures --no-headless --show-chrome-log --disable-gpu --disable-screenshots --js-flags='--no-lazy' {flag_ext1} -u {url}"
            # QUEUE WITHOUT EXTENSIONS + CATAPULT
            # cmd = f"python3 ./scripts/vv8-cli.py crawl -pp Mfeatures --no-headless --show-chrome-log --disable-gpu {catapult1} --js-flags='--no-lazy' -u {url}"
            print(cmd)
            os.system(cmd)


def load_urls(json_file: str) -> Dict[str, List[str]]:
    with open(json_file, "r") as fout:
        data = json.load(fout)
    return data


if __name__ == "__main__":
    arguments = docopt(__doc__, version="Schedule jobs on vv8+fv8 crawler 1.0")
    main(arguments)

# python3 ./scripts/vv8-cli.py crawl -u 'https://vv8-test.jsapi.tech/arguments-test.html' -pp 'Mfeatures' --load-extension=/app/node/extensionsSome/postMessage-logger-v3 --disable-extensions-except=/app/node/extensionsSome/postMessage-logger-v3
