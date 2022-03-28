import config as cfg
import urllib.parse

from sqlalchemy import create_engine

_engine_url = f'sqlalchemy://{cfg.database_username}:{cfg.database_password}@{cfg.database_host}:{cfg.database_port}/{cfg.database_name}'
_engine_url = urllib.parse.quote(_engine_url)
engine = create_engine(_engine_url)
