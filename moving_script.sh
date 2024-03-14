# copy queue.py
# copy queue.sh
# copy q_unqueue.sh
# copy url_dictionary.out
# change path in every dictionary key (Replace All from VS Code) (eg. vv8-crawler-slim-v4 -> vv8-crawler-slim-v5)
# add to .gitignore

# cd to previous vv8_crawler directory
# mv ALL_EXTENSIONS40k/ /home/npantel/vv8-crawler-slim-v5/celery_workers/vv8_worker/vv8_crawler

# add to .dockerignore (inside celery_workers)
# (PROBABLY NOT) change the 2 folders that communicate (and are connected) so extensions don't get overwritten

# change tasks.py (inside vv8_worker)
# change crawler.js (inside vv8_crawler)
# change vv8_worker.dockerfile


# add fv8_with.deb inside the docker folder
# add fv8_without.deb inside the docker folder

# how it looks like (+ moving extension folders):
# Changes not staged for commit:
#   (use "git add <file>..." to update what will be committed)
#   (use "git restore <file>..." to discard changes in working directory)
#         modified:   .gitignore
#         modified:   celery_workers/vv8_worker.dockerfile
#         modified:   celery_workers/vv8_worker/tasks.py
#         modified:   celery_workers/vv8_worker/vv8_crawler/crawler.js

# Untracked files:
#   (use "git add <file>..." to include in what will be committed)
#         celery_workers/.dockerignore
#         moving_script.sh
#         q_unqueue.sh
#         queue.py
#         queue.sh
