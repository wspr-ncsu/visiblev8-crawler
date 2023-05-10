# VisibleV8 Crawler

The VisibleV8 Crawler is a framework which makes large scale crawling of URLs with [VisibleV8](https://github.com/wspr-ncsu/visiblev8) much easier.

## Setup

> **Note**
> This tool requires Python 3.10 or above. If your OS python3 version is <3.10, you can use [`pyenv`](https://github.com/pyenv/pyenv) to setup a specific version of Python.

To setup VisibleV8 Crawler install `docker` and `docker-compose`, and run the following command

```sh
pip install -r ./scripts/requirements.txt
python ./scripts/vv8-cli.py setup
```

> **Warning**
> Make sure that you are able to use `docker` and `docker compose` without using sudo. ([instructions here](https://docs.docker.com/engine/install/linux-postinstall/))

If you plan to use visiblev8 crawler a lot, you can alias the script to the `vv8cli` command using:

```sh
alias vv8cli="python3 $(pwd)/scripts/vv8-cli.py" 
```

> **Note**
> vv8 crawler cli scripts can also be used for a shared remote server by choosing the remote installation option during the setup wizard. The list of URLs (and their submission IDs) that have been run by you (and their associated submission ids) are stored locally in a sqlite3 database at `./scripts/.vv8.db`

## Run a single URL

```sh
python3 ./scripts/vv8-cli.py crawl -u 'https://google.com'
```

If you want to apply a specific vv8-postprocessor, you can use:

```sh
python3 ./scripts/vv8-cli.py crawl -u 'https://google.com' -pp 'Mfeatures'
```

By default the postprocessed data will be written to an associated postgresql database which can be accessed using the following command if setup locally

```sh
psql --host=0.0.0.0 --port=5434 --dbname=vv8_backend --username=vv8
```

> **Note** If prompted for a password, the password is by default `vv8`

If you want to pass more flags to the crawler (say you want to only stay on a specific page for 5s) and have the VisibleV8 binary run in the old headless mode

```sh
python3 ./scripts/vv8-cli.py crawl -u 'https://google.com' -pp 'Mfeatures' --loiter-time 5 --headless="old"
```

## Run a list of URLs

VV8 Crawler can also be used to crawl multiple URLs in one go:

```sh
python3 ./scripts/vv8-cli.py crawl -f file.txt
```

> **Note**
> `file.txt` is a file consisting of multiple urls seperated by newlines like such:
> ```txt
> https://google.com
> https://amazon.com
> https://microsoft.com
> ```

## Run a list of URLs in tranco format

If you have a list of URLs in the tranco CSV format, you can directly run it using
```sh
python3 ./scripts/vv8-cli.py crawl -c list.csv
```

## Run a specific URL

```sh
python3 ./scripts/vv8-cli.py crawl -u 'https://google.com'
```

## Monitoring the status of a crawl

The VisibleV8 crawler provides a flower Web UI to keep track of all URLs being crawled and postprocessed. The interface is accessible at `http://localhost:5555`. 

If you are running the server locally, you can use `python3 ./scripts/vv8-cli.py docker -f` to get a rolling log of everything the the crawler does.

> **Note**
> If you are using the crawler in a ssh session you can make use of [port-forwarding](https://help.ubuntu.com/community/SSH/OpenSSH/PortForwarding) to browse the web UI.

## Fetch status of a crawl by URL

```sh
python3 ./scripts/vv8-cli.py fetch status 'https://google.com'
```

## Fetch generated metadata by URL

We try to generate a har file, a screenshot and the VisibleV8 logs for every URL run and store it on mongodb, to fetch them you need to run `python3 ./scripts/vv8-cli.py fetch <metadata_name> 'https://google.com'`

```sh
python3 ./scripts/vv8-cli.py fetch screenshots 'https://google.com'
```

You can request the following things:

- `screenshots`
- `raw_logs`
- `hars`
- `status`

This command will download the files to the current directory.

## Advanced usage

### Using a different version of VisibleV8

To use a different instrumented chrome binary (or a different version of VisibleV8) you can edit https://github.com/rekap-ncsu/vv8-crawler-slim/blob/main/celery_workers/vv8_worker.dockerfile and make the following modifications

```diff
# Copy chromium with VV8
- COPY --from=visiblev8/vv8-base:latest /opt/chromium.org/chromium/* /opt/chromium.org/chromium/
+ COPY ./chrome_installer.deb .
+ RUN apt install -y ./chrome_installer.deb
```

### Using a custom variant of the vv8-postprocessor binary

Chose the option to build postprocessors locally in the setup script.

Navigate to the `celery_workers/visiblev8` folder and make changes to the local checkout of the postprocessors once you are done making the changes, re-run the setup script.

If you plan on using a custom postgresql schema to store your data, you should also edit [`vv8_backend_database/init/postgres_schema.sql`](https://github.com/rekap-ncsu/vv8-crawler-slim/blob/main/vv8_backend_database/init/postgres_schema.sql) to intialize the schema you want to dump data to.

### Using extensions

You can copy your extension directory into the `celery_worker/vv8_worker/vv8_crawler` directory and add the following two lines to [`celery_workers/vv8_worker/vv8_crawler/crawler.js`](https://github.com/rekap-ncsu/vv8-crawler-slim/blob/main/celery_workers/vv8_worker/vv8_crawler/crawler.js)

```diff
    const default_crawler_args = [
                    "--disable-setuid-sandbox",
                    "--no-sandbox",
+                    `--load-extension=/app/node/extension_name`,
+                    `--disable-extensions-except=/app/node/extension_name`,
                    //'--enable-logging=stderr',
                    '--enable-automation',
                    //'--v=1'
                ];
```

> **Note**
> If your extension loads content-scripts you will also want to use the `--no-headless` flag when crawling like such:
> ```sh
> python3 ./scripts/vv8-cli.py crawl -u 'https://google.com' -pp 'Mfeatures' --no-headless
> ```

## Adding a custom user-agent/having the browser perform a custom action

To add a custom useragent, or have the browser perform a custom action, you can edit [`celery_workers/vv8_worker/vv8_crawler/crawler.js`](https://github.com/rekap-ncsu/vv8-crawler-slim/blob/main/celery_workers/vv8_worker/vv8_crawler/crawler.js). The `crawler.js` file is expected to be edited and customized, and is mounted as a volume in the docker conatiner making changes instantaneous.

## Sequential crawling

When running the setup script, you can set the number of workers to 1. This will ensure only one celery worker gets created disabling concurrent crawling. The sequence of the crawls will depend on their ordering in the csv/txt file being passed to the crawl script. 
