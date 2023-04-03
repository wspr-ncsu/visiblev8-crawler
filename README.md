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
> `file.txt` is a file consisting of multiple urls seperated by newlines

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
