from fastapi import APIRouter
from urllib.parse import urlparse
from vv8db_sidecar.models.parsed_log_model import ParsedLogModel
from vv8db_sidecar.models.submission_model import SubmissionModel
from vv8db_sidecar.db_conn_manager import engine
from sqlalchemy import insert


router = APIRouter(
    prefix='/api/v1'
)


@router.post('/submission')
async def post_submission(submission: SubmissionModel):
    print('Received url submission')
    # since this is only called from the web server we assume the url is valid
    scheme, domain, path, _, params, query, fragment = urlparse(submission.url)
    stmt = insert('vv8_logs.submissions').values(
        url_scheme=scheme, url_domain=domain, url_path=path, url_query_params=params,
        url_fragment=fragment)
    async with engine.connect() as conn:
        conn.execute(stmt)
        conn.commit()


@router.post('/parsedlog')
async def post_parsed_log(parsed_log: ParsedLogModel):
    print('Received parsed log')
    print(parsed_log)
    '''
    submission_id = parsed_log.submission_id
    insert_isolates_stmt = insert('vv8logs.isolates').values([
        {
            'isolate_value': isolate.isolate_value,
            'submission_id': submission_id
        }
        for isolate in parsed_log.isolates
    ])
    async with engine.connect() as conn:
        ret_val = conn.execute(insert_isolates_stmt)
        conn.commit()
        print(ret_val)
    '''