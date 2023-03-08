import os
from pymongo import MongoClient
import gridfs

from celery import Task

class GridFSTask(Task):
    _gridfs = None
    _mongo = None

    @property
    def gridfs(self):
        if self._gridfs is None:
            mongo_username = os.environ.get('MONGO_USER')
            mongo_password = os.environ.get('MONGO_PASSWORD')
            mongo_host = os.environ.get('MONGO_HOST')
            mongo_port = os.environ.get('MONGO_PORT')
            mongo_database = os.environ.get('MONGO_DATABASE')

            mongo_client = MongoClient(f'mongodb://{mongo_username}:{mongo_password}@{mongo_host}:{mongo_port}/')
            mongo_db = mongo_client[mongo_database]
            gridfs_instance = gridfs.GridFSBucket(mongo_db)
            self._gridfs = gridfs_instance
        return self._gridfs

    @property
    def mongo(self):
        if self._mongo is None:
            mongo_username = os.environ.get('MONGO_USER')
            mongo_password = os.environ.get('MONGO_PASSWORD')
            mongo_host = os.environ.get('MONGO_HOST')
            mongo_port = os.environ.get('MONGO_PORT')
            mongo_database = os.environ.get('MONGO_DATABASE')

            mongo_client = MongoClient(f'mongodb://{mongo_username}:{mongo_password}@{mongo_host}:{mongo_port}/')
            mongo_db = mongo_client[mongo_database]
            self._mongo = mongo_db
        return self._mongo