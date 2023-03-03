#!/usr/bin/env python3.8

import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote
from dotenv import dotenv_values


def main():
    cfg = dotenv_values(".env")
    db_user = quote(cfg['VV8_DB_USERNAME'])
    db_password = quote(cfg['VV8_DB_PASSWORD'])
    db_host = quote(cfg['VV8_DB_HOST'])
    db_port = quote(cfg['VV8_DB_PORT'])
    db_name = quote(cfg['VV8_DB_NAME'])
    engine_url = f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    engine = create_engine(engine_url)

    df = pd.read_sql("SELECT * FROM vv8_logs.vv8_logs.submissions", engine)
    df.to_csv('data.csv')


if __name__ == "__main__":
    main()
