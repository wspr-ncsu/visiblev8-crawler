import sqlalchemy.sql as sql

from vv8db_sidecar.db_conn_manager import engine


async def log_entry_count(submission_id, log_type):
    log_entry_table = sql.table(
        'log_entries',
        sql.column('log_entry_id'),
        sql.column('log_type'),
        sql.column('submission_id'),
        schema='vv8_logs'
    )
    stmt = (
        sql.select([sql.func.count()])
        .select_from(log_entry_table)
        .where(
            log_entry_table.c.submission_id==submission_id,
            log_entry_table.c.log_type==log_type)
    )
    async with engine.connect() as conn:
        cursor = await conn.execute(stmt)
        count = cursor.scalar()
    return count
