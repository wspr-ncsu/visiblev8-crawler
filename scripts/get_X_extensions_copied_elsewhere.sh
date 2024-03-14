cd ../celery_workers/vv8_worker/vv8_crawler/ALL_EXTENSIONS40k/
find . -maxdepth 1 -type d | head -n 2 | xargs -I{} cp -r {} ../ALL_EXTENSIONS1k/
# head -n 2 | xargs -I{} cp -r {} ../ALL_EXTENSIONS1k/ # this doesn't work
# find /home/npantel/vv8-crawler-slim-v5/celery_workers/vv8_worker/vv8_crawler/ALL_EXTENSIONS40k/ -mindepth 1 -maxdepth 1 -type d | head -n 2 | xargs -I{} cp -r {} ../ALL_EXTENSIONS1k/ # copies multiple stuff not only directories
