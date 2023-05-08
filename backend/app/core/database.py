import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient

sql_username = os.environ.get('SQL_USERNAME')
sql_password = os.environ.get('SQL_PASSWORD')
sql_host = os.environ.get('SQL_HOST')
sql_port = os.environ.get('SQL_PORT')
sql_database = os.environ.get('SQL_DATABASE')

sql_engine = create_engine(
    f'postgresql+psycopg2://{sql_username}:{sql_password}@{sql_host}:{sql_port}/{sql_database}'
)
sql_session = sessionmaker(bind=sql_engine)

mongo_username = os.environ.get('MONGO_USER')
mongo_password = os.environ.get('MONGO_PASSWORD')
mongo_host = os.environ.get('MONGO_HOST')
mongo_port = os.environ.get('MONGO_PORT')
mongo_database = os.environ.get('MONGO_DATABASE')

mongo_client = MongoClient(
    f'mongodb://{mongo_username}:{mongo_password}@{mongo_host}:{mongo_port}/'
)

if not mongo_database:
    print('MONGO_DATABASE environment variable not set')
    sys.exit(-1)
mongo_db = mongo_client[mongo_database]
