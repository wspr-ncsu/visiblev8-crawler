#!/usr/bin/env python3

import os
import pandas as pd
import time
import csv
from requests import get
from typing import Tuple
import argparse

URL = "https://api.ecrimex.net"
OP_API = None # Enter key here

parser = argparse.ArgumentParser(description="Automated phishing site crawler")
parser.add_argument('-k', '--kitphishr')
args = parser.parse_args()

# returns (JSON, "") on success and (None, "error message") on failure
def get_openphish_feed() -> Tuple[dict, str]:
    url = f"{URL}/phish"
    resp = get(url, headers={"Authorization": f"{OP_API}"})
    if resp.status_code != 200:
        return None, resp.text
    return resp.json(), ""

t = int(time.time())
os.system(f"wget -O data/phishtank-{t}.csv https://data.phishtank.com/data/online-valid.csv")
# os.system(f"wget -O data/openphish-{t}.txt https://openphish.com/feed.txt")

dic_op, out = get_openphish_feed()
phishing_list = dic_op["_embedded"]["phish"]

with open(f"data/openphish-{t}.txt", "w") as f:
    for i in range(len(phishing_list)):
        f.write(phishing_list[i]["url"] + "\n")

# df = pd.read_csv(f"data/phishtank-{t}.csv")['url']
# df.to_csv(f'data/phishtank-{t}.txt', header=False, index=False)

df = pd.read_csv(f"data/phishtank-{t}.csv",)['url']
df.to_csv(f'data/phishtank-{t}.txt', sep='\n', quoting=csv.QUOTE_NONE, header=False, index=False)

files = [f'data/openphish-{t}.txt', f'data/phishtank-{t}.txt']

for f in files:
    print(f"Crawling urls in {f}")
    if os.system(f"python3 vv8-cli.py crawl -f {f}") is not 0:
        exit(1)
    
if args.kitphishr is None:
    if input("Run Kitphishr? (y/n)") != "y":
        print("Stopping...")
        exit(0)

    kit_path = input("Enter Kitphishr path: ")
else:
    kit_path = args.kitphishr

for f in files:
    print(f"Submitting urls in {f} to kitphishr (using {kit_path})")
    os.system(f"cat {f} | {kit_path} -c 250 -v -d -o vv8-kitphishr-output")
