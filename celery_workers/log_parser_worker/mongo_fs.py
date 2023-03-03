#!/usr/bin/env python3.8
import asyncio
import pymongo
import gridfs
import os


MONGO_USER = os.environ['MONGO_USER']
MONGO_PASSWORD = os.environ['MONGO_PASSWORD']
MONGO_HOST = os.environ['MONGO_HOST']
MONGO_PORT = os.environ['MONGO_PORT']


# async def func(fs: motor.motor_asyncio.AsyncIOMotorGridFSBucket):
#     async with fs.open_upload_stream(
#             "test_file", metadata={"contentType": "text/plain"}) as gridin:
#         gridin.write(b'First part\n')
#         gridin.write(b'Second part')

fs = None


def get_fs():
    if fs is None:
        conn_url = f'mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/admin'
        client = pymongo.MongoClient(conn_url)
        db = client['db']
        fs = gridfs.GridFS(db)
    return fs
