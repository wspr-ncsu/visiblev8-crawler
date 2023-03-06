#!/usr/bin/env python3

from celery import *
from vv8_worker.tasks import process_url
import os
from dotenv import load_dotenv
import sqlalchemy.sql as sql
from sqlalchemy.ext.asyncio import create_async_engine
from urllib.parse import urlparse, quote
import requests
from pydantic.dataclasses import dataclass
import aiohttp
import asyncio
import aiofiles
import argparse
from time import sleep

@dataclass
class SubmissionModel:
    url: str

load_dotenv()
VV8_CELERY_BROKER = os.getenv('VV8_CELERY_BROKER')
VV8_CELERY_BROKER_PORT = os.getenv('VV8_CELERY_BROKER_PORT')
VV8_CELERY_ID = os.getenv('VV8_CELERY_ID')
VV8_CELERY_BACKEND_USER = os.getenv('VV8_CELERY_BROKER')
VV8_CELERY_BACKEND_PASSWORD = os.getenv('VV8_CELERY_BACKEND_PASSWORD')
VV8_CELERY_BACKEND_HOST = os.getenv('VV8_CELERY_BACKEND_HOST')
VV8_CELERY_BACKEND_PORT = os.getenv('VV8_CELERY_BACKEND_PORT')
VV8_CELERY_BACKEND_DATABASE = os.getenv('VV8_CELERY_BACKEND_DATABASE')

POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_DB = os.getenv('POSTGRES_DB')
PGDATA = os.getenv('PGDATA')

VV8_DB_USERNAME = os.getenv('VV8_DB_USERNAME')
VV8_DB_PASSWORD = os.getenv('VV8_DB_PASSWORD')
VV8_DB_HOST = os.getenv('VV8_DB_HOST')
VV8_DB_PORT = os.getenv('VV8_DB_PORT')
VV8_DB_NAME = os.getenv('VV8_DB_NAME')
VV8_DB_SC_HOST = os.getenv('VV8_DB_SC_HOST')
VV8_DB_SC_PORT = os.getenv('VV8_DB_SC_PORT')


async def call_auto_task(urlstr: str, engine):
    database_username = os.environ['VV8_DB_USERNAME']
    database_password = os.environ['VV8_DB_PASSWORD']
    database_host = os.environ['VV8_DB_HOST']
    database_port = os.environ['VV8_DB_PORT']
    database_name = os.environ['VV8_DB_NAME']
    database_sc_host = os.environ['VV8_DB_SC_HOST']
    database_sc_port = os.environ['VV8_DB_SC_PORT']

    db_user = quote(database_username)
    db_password = quote(database_password)
    db_host = quote(database_host)
    db_port = quote(database_port)
    db_name = quote(database_name)
    
    url = urlstr
    sleep(0.1)
    print(f"Processing {url}...")
    # scheme, domain, path, _, query, fragment = urlparse(url)
    # submission_table = sql.table(
    #     'submissions',
    #     sql.column('submission_id'),
    #     sql.column('url_scheme'),
    #     sql.column('url_domain'),
    #     sql.column('url_path'),
    #     sql.column('url_query_params'),
    #     sql.column('url_fragment'),
    #     schema='vv8_logs')
    # stmt = submission_table.insert().values(
    #     url_scheme=scheme,
    #     url_domain=domain,
    #     url_path=path,
    #     url_query_params=query,
    #     url_fragment=fragment).returning(submission_table.c.submission_id)

    # with engine.connect() as conn:
    #     cursor = conn.execute(stmt)
    #     conn.commit()
    #     ret_vals = cursor.all()
    #     submission_id, = ret_vals[0]

    # sub_m = SubmissionModel(url)
    
    # submission_post_url = f'http://{database_sc_host}:7777/api/v1/submission'
    # r = requests.post(submission_post_url, json=sub_m.to_json())
    # r.raise_for_status()
    # async with aiohttp.ClientSession() as session:
    #     async with session.post(submission_post_url, json={'url': url}) as resp:
    #         resp.raise_for_status()
    #         sub_resp = await resp.json()
    #         submission_id = sub_resp['submission_id']
    
    # Group post to /submission
    # since this is only called from the web server we assume the url is valid
    scheme, domain, path, _, query, fragment = urlparse(url)
    submission_table = sql.table(
        'submissions',
        sql.column('submission_id'),
        sql.column('url_scheme'),
        sql.column('url_domain'),
        sql.column('url_path'),
        sql.column('url_query_params'),
        sql.column('url_fragment'),
        schema='vv8_logs'
    )
    
    stmt = submission_table.insert().values(
        url_scheme=scheme,
        url_domain=domain,
        url_path=path,
        url_query_params=query,
        url_fragment=fragment
    ).returning(
        submission_table.c.submission_id
    )
    
    async with engine.connect() as conn:
        cursor = await conn.execute(stmt)
        await conn.commit()
        ret_vals = cursor.all()
        assert len(ret_vals) == 1
        submission_id, = ret_vals[0]
    # return SubmissionResponseModel(submission_id)
    
    log = process_url.apply_async(
        kwargs={'url': url, 'submission_id': submission_id},
        queue="crawler",
        chain=[
            signature('log_parser_worker.parse_log', queue="log_parser")
        ]
    )

    
async def main():
    database_username = os.environ['VV8_DB_USERNAME']
    database_password = os.environ['VV8_DB_PASSWORD']
    database_host = os.environ['VV8_DB_HOST']
    database_port = os.environ['VV8_DB_PORT']
    database_name = os.environ['VV8_DB_NAME']
    database_sc_host = os.environ['VV8_DB_SC_HOST']
    database_sc_port = os.environ['VV8_DB_SC_PORT']

    db_user = quote(database_username)
    db_password = quote(database_password)
    db_host = quote(database_host)
    db_port = quote(database_port)
    db_name = quote(database_name)
    engine_url = f'postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    engine_obj = create_async_engine(engine_url)
    
    parser = argparse.ArgumentParser(description='VV8 URL Processor')
    parser.add_argument('infile', type=str, help='Input file')
    args = parser.parse_args()
    # lines = read_file(args.infile)
    
    async with aiofiles.open(args.infile, 'r') as f:
        url_read = await f.readline()
        url_clean = url_read.strip()
        while url_clean != '':
            await call_auto_task(url_clean, engine_obj)
            url_read = await f.readline()
            url_clean = url_read.strip()

if __name__ == "__main__":
    asyncio.run(main())
