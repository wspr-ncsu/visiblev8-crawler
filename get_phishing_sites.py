#!/usr/bin/env python3

import os
import pandas as pd
import time
import csv

t = int(time.time())
os.system(f"wget -O data/phishtank-{t}.csv https://data.phishtank.com/data/online-valid.csv")
os.system(f"wget -O data/openphish-{t}.txt https://openphish.com/feed.txt")

df = pd.read_csv(f"data/phishtank-{t}.csv")['url']
df.to_csv(f'data/phishtank-{t}.txt', header=False, index=False)

df = pd.read_csv(f"data/phishtank-{t}.csv",)['url']
df.to_csv(f'data/phishtank-{t}.txt', sep='\n', quoting=csv.QUOTE_NONE, header=False, index=False)

files = [f'data/openphish-{t}.txt', f'data/phishtank-{t}.txt']

for f in files:
    print(f"Crawling urls in {f}")
    os.system(f"python3 vv8-cli.py crawl -f {f}")
