import vv8db_sidecar.config as cfg
import urllib.parse
import atexit
import asyncio

from sqlalchemy.ext.asyncio import create_async_engine

_esc_db_user = urllib.parse.quote(cfg.database_username)
_esc_db_password = urllib.parse.quote(cfg.database_password)
_esc_db_host = urllib.parse.quote(cfg.database_host)
_esc_db_port = urllib.parse.quote(cfg.database_port)
_esc_db_name = urllib.parse.quote(cfg.database_name)

_engine_url = f'postgresql+asyncpg://{_esc_db_user}:{_esc_db_password}@{_esc_db_host}:{_esc_db_port}/{_esc_db_name}'
engine = create_async_engine(_engine_url)

# TODO: investigate need to dispose of engine at module close
# I've investgated adding a blocking call to async function to atexit, but it is difficult to get the event loop
# from synchronous code.
# asyncio.get_event_loop is deprecated, and
# asyncio.get_running_loop "can only be called from a coroutine or a callback" (src: https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.get_running_loop)
