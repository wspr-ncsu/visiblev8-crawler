import sqlalchemy.sql as sql
from sqlalchemy import select
from vv8db_sidecar.db_conn_manager import engine
from vv8db_sidecar.database_models.parsed_log_model import LogEntry

async def log_entry_count(submission_id, log_type):
    async with engine.connect() as conn:
        cursor = await conn.execute(
            select(sql.func.count(LogEntry.log_entry_id))
            .where(LogEntry.submission_id==submission_id)
            .where(LogEntry.log_type==log_type))
        count = cursor.scalar()
    return count
