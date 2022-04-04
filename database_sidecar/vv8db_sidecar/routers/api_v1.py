#import sqlalchemy as sqla
import sqlalchemy.sql as sql

from fastapi import APIRouter
from urllib.parse import urlparse
from vv8db_sidecar.models.parsed_log_model import ParsedLogModel
from vv8db_sidecar.models.submission_model import SubmissionModel
from vv8db_sidecar.models.submission_response_model import SubmissionResponseModel
from vv8db_sidecar.db_conn_manager import engine


router = APIRouter(
    prefix='/api/v1'
)


@router.post('/submission')
async def post_submission(submission: SubmissionModel):
    print('Received url submission')
    # since this is only called from the web server we assume the url is valid
    scheme, domain, path, _, query, fragment = urlparse(submission.url)
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
    return SubmissionResponseModel(submission_id)


@router.post('/parsedlog')
async def post_parsed_log(parsed_log: ParsedLogModel):
    print('Received parsed log')
    submission_id = parsed_log.submission_id
    isolates_table = sql.table(
        'isolates',
        sql.column('isolate_id'),
        sql.column('isolate_value'),
        sql.column('submission_id'),
        schema='vv8_logs'
    )
    window_origin_table = sql.table(
        'window_origins',
        sql.column('window_origin_id'),
        sql.column('isolate_id'),
        sql.column('url'),
        sql.column('submission_id'),
        schema='vv8_logs'
    )
    execution_context_table = sql.table(
        'execution_contexts',
        sql.column('context_id'),
        sql.column('window_id'),
        sql.column('isolate_id'),
        sql.column('sort_index'),
        sql.column('url'),
        sql.column('script_id'),
        sql.column('src'),
        sql.column('submission_id'),
        schema='vv8_logs'
    )
    log_entry_table = sql.table(
        'log_entries',
        sql.column('sort_index'),
        sql.column('log_type'),
        sql.column('src_offset'),
        sql.column('context_id'),
        sql.column('object'),
        sql.column('function'),
        sql.column('property'),
        sql.column('arguments'),
        sql.column('submission_id'),
        schema='vv8_logs'
    )
    submission_table = sql.table(
        'submissions',
        sql.column('submission_id'),
        sql.column('end_time'),
        schema='vv8_logs'
    )

    insert_isolates_stmt = isolates_table.insert().values([
        {
            'isolate_value': isolate.isolate_value,
            'submission_id': submission_id
        }
        for isolate in parsed_log.isolates
    ]).returning(isolates_table.c.isolate_id)

    async with engine.connect() as conn:
        isolate_cursor = await conn.execute(insert_isolates_stmt)
        isolate_all_resp = isolate_cursor.all()
        isolate_map = {
            iso.isolate_value: iso_resp[0]
            for iso_resp, iso in zip(isolate_all_resp, parsed_log.isolates)
        }

        insert_window_origins_stmt = window_origin_table.insert().values([
            {
                'isolate_id': isolate_map[wo.isolate_id],
                'url': wo.url,
                'submission_id': submission_id
            }
            for wo in parsed_log.window_origins
        ]).returning(window_origin_table.c.window_origin_id)
        window_origin_cursor = await conn.execute(insert_window_origins_stmt)
        window_origin_all_resp = window_origin_cursor.all()
        window_origin_map = {
            wo.url: wo_resp[0]
            for wo_resp, wo in zip(window_origin_all_resp, parsed_log.window_origins)
        }

        insert_executions_contexts_stmt = execution_context_table.insert().values([
            {
                'window_id': window_origin_map[ec.window_origin],
                'isolate_id': isolate_map[ec.isolate_id],
                'sort_index': ec.sort_index,
                'url': ec.script_url,
                'script_id': ec.script_id,
                'src': ec.src,
                'submission_id': submission_id
            }
            for ec in parsed_log.execution_contexts
        ]).returning(execution_context_table.c.context_id)
        execution_context_cursor = await conn.execute(insert_executions_contexts_stmt)
        execution_context_all_resp = execution_context_cursor.all()
        execution_context_map = {
            ec.script_id: ec_resp[0]
            for ec_resp, ec in zip(execution_context_all_resp, parsed_log.execution_contexts)
        }

        insert_log_entries_stmt = log_entry_table.insert().values([
            {
                'sort_index': le.sort_index,
                'log_type': le.log_type,
                'src_offset': le.src_offset,
                'context_id': None if le.context_id is None else execution_context_map[le.context_id],
                'object': le.obj,
                'function': le.func,
                'property': le.prop,
                'arguments': None if le.args is None else ':'.join(le.args),
                'submission_id': submission_id
            }
            for le in parsed_log.log_entries
        ])
        await conn.execute(insert_log_entries_stmt)

        update_sub_stmt = submission_table.update().values(end_time=sql.functions.current_timestamp())
        update_sub_stmt = update_sub_stmt.values(end_time=sql.functions.current_timestamp())
        update_sub_stmt = update_sub_stmt.where(submission_table.c.submission_id==submission_id)
        print(update_sub_stmt)
        await conn.execute(update_sub_stmt)

        await conn.commit()
