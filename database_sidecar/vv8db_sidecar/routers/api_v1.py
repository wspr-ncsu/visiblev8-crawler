#import sqlalchemy as sqla
from ast import stmt
import sqlalchemy.sql as sql
from sqlalchemy import insert, update, select
from vv8db_sidecar.database_models.parsed_log_model import LogEntry, Isolates, WindowOrigins, ExecutionContexts, Relationships, Submission
import urllib.parse
import time

from typing import Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic.dataclasses import dataclass
from urllib.parse import urlparse
from vv8db_sidecar.models.parsed_log_model import ParsedLogModel, RelationshipType
from vv8db_sidecar.models.submission_model import SubmissionModel
from vv8db_sidecar.models.submission_response_model import SubmissionResponseModel
from vv8db_sidecar.db_conn_manager import SessionLocal
from vv8db_sidecar.util.database_util import log_entry_count

router = APIRouter(
    prefix='/api/v1'
)


# Used to create new submissions
# Returns submission id
@router.post('/submission')
async def post_submission(submission: SubmissionModel):
    print('Received url submission')
    # since this is only called from the web server we assume the url is valid
    scheme, domain, path, _, query, fragment = urlparse(submission.url)
    async with SessionLocal() as conn:
        submissions = await conn.scalars(
            insert(Submission)
            .returning(Submission),
                [{
                    'url_scheme': scheme,
                    'url_domain': domain,
                    'url_path': path,
                    'url_query_params': query,
                    'url_fragment': fragment
                }])
        await conn.commit()
        assert submissions[0]
    return SubmissionResponseModel(submissions[0].submission_id)


# Used to insert a parsed log with a given submission id
# Implementation note: SQL Alchemy does not work well with "text" types that include "RETUNING"
#     Need to use SQL Alchemy statement builder to get multiple retuning values
@router.post('/parsedlog')
async def post_parsed_log(parsed_log: ParsedLogModel):
    submission_id = parsed_log.submission_id
    print(f'Received parsed log: {submission_id} {time.time()}')
    total_start = time.perf_counter()
    async with SessionLocal() as conn:
        #
        # Insert Isolates
        #
        isolate_args = [
            {
                'isolate_value': isolate.isolate_value,
                'submission_id': submission_id
            }
            for isolate in parsed_log.isolates
        ]
        isolates = await conn.scalars(insert(Isolates).returning(Isolates), isolate_args)
        isolate_map = { iso.isolate_value: iso.isolate_id for iso in isolates }
        #
        # Window Origins
        #
        window_origin_args = [
            {
                'isolate_id': isolate_map[wo.isolate_id],
                'url': wo.url,
                'submission_id': submission_id
            }
            for wo in parsed_log.window_origins
        ]
        window_origins = await conn.scalars(insert(WindowOrigins).returning(WindowOrigins), window_origin_args)
        window_origin_map = { wo.url: wo.window_origin_id for wo in window_origins }
        #
        # Execution Contexts
        #
        execution_context_args = [
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
        ]
        execution_context = await conn.scalars(insert(ExecutionContexts).returning(ExecutionContexts), execution_context_args)
        execution_context_map = { ec.script_id: ec.context_id for ec in execution_context}
        #
        # Log Entries
        #
        log_entry_args = [
            {
                'sort_index': le.sort_index,
                'log_type': le.log_type.value,
                'src_offset': le.src_offset,
                'context_id': None if le.context_id is None else execution_context_map[le.context_id],
                'object': le.obj,
                'function': le.func,
                'property': le.prop,
                'arguments': None if le.args is None else ':'.join(le.args),
                'submission_id': submission_id
            }
            for le in parsed_log.log_entries
        ]
        await conn.execute(insert(LogEntry), log_entry_args)
        #
        # Relationships
        #
        relationship_args = []
        for r in parsed_log.relationships:
            if r.relationship_type == RelationshipType.execution_hierarchy:
                relationship_args.append({
                    'relationship_type': RelationshipType.execution_hierarchy,
                    'from_entity': -1 if r.from_entity is None else execution_context_map[int(r.from_entity)],
                    'to_entity': -1 if r.to_entity is None else execution_context_map[int(r.to_entity)],
                    'submission_id': submission_id
                })
        await conn.execute(insert(Relationships), relationship_args)
        #
        # Update Submission
        #
        await conn.execute(update(Submission), [ {'submission_id': submission_id, 'end_time':sql.functions.current_timestamp()} ])
        await conn.commit()


@dataclass
class SubmissionIdExistsResponse:
    submission_id: int
    exists: bool


# used to check if a given submission id exists
@router.get('/submission/{submission_id}/exists', response_model=SubmissionIdExistsResponse)
async def get_submission_ids(submission_id: int):
    async with SessionLocal() as conn:
        all_resp = await conn.execute(
            select(Submission)
                .where(Submission.submission_id==submission_id)
                .where(Submission.end_time.isnot(None)))
        if len(all_resp) == 0:
            # No submission found
            raise HTTPException(status_code=404, detail="Submission not found")
        else:
            # found submission
            assert len(all_resp) == 1
            assert all_resp[0][0] == submission_id
            return SubmissionIdExistsResponse(submission_id, True)


@dataclass
class RecentSubmissionResponse:
    submission_id: int | None


# Used to get the most recent submission id for a given url
@router.get('/submission', response_model=RecentSubmissionResponse)
async def get_recent_submission(url: str):
    print('GET SUBMISSION', url)
    raw_url = urllib.parse.unquote(url)
    scheme, domain, path, _, query, fragment = urllib.parse.urlparse(raw_url)
    async with SessionLocal() as conn:
        all_resp = await conn.execute(
            select(Submission)
                .where(Submission.url_scheme == scheme)
                .where(Submission.url_domain == domain)
                .where(Submission.url_path == path)
                .where(Submission.url_query_params == query)
                .where(Submission.url_fragment == fragment)
                .order_by(Submission.start_time.desc())
                .limit(1)
            ).mappings().all()
    if len(all_resp) == 0:
        return RecentSubmissionResponse(None)
    elif len(all_resp) == 1:
        return RecentSubmissionResponse(all_resp[0][0])
    else:
        raise HTTPException(status_code=500)


@router.get('/submission/{submission_id}/gets')
async def get_submission_id_gets(submission_id: int):
    async with SessionLocal() as conn:
        all_resp = await conn.execute(
            select(Submission)
                .where(Submission.submission_id==submission_id)
                .where(Submission.log_type=='get')).mappings()
    return all_resp.all()


@router.get('/submission/{submission_id}/gets/count')
async def get_submission_id_gets_count(submission_id: int):
    return await log_entry_count(submission_id, 'get')


@router.get('/submission/{submission_id}/sets')
async def get_submission_id_sets(submission_id: int):
    async with SessionLocal() as conn:
        all_resp = await conn.execute(
            select(Submission)
                .where(Submission.submission_id==submission_id)
                .where(Submission.log_type=='set')).mappings()
    return all_resp.all()

@router.get('/submission/{submission_id}/sets/count')
async def get_submission_id_sets_count(submission_id: int):
    return await log_entry_count(submission_id, 'set')


@router.get('/submission/{submission_id}/constructions')
async def get_submission_id_constructions(submission_id: int):
    async with SessionLocal() as conn:
        all_resp = await conn.execute(
            select(Submission)
                .where(Submission.submission_id==submission_id)
                .where(Submission.log_type=='new')).mappings().all()
    output = [
        dict(row)
        for row in all_resp
    ]
    for x in output:
        x['arguments'] = x['arguments'].split(':')
    return all_resp


@router.get('/submission/{submission_id}/constructions/count')
async def get_submission_id_constructions_count(submission_id: int):
    return await log_entry_count(submission_id, 'new')


@router.get('/submission/{submission_id}/calls')
async def get_submission_id_calls(submission_id: int):
    async with SessionLocal() as conn:
        all_resp = await conn.execute(
            select(Submission)
                .where(Submission.submission_id==submission_id)
                .where(Submission.log_type=='call')).mappings().all()
    output = [
        dict(row)
        for row in all_resp
    ]
    for x in output:
        x['arguments'] = x['arguments'].split(':')
    return output


@router.get('/submission/{submission_id}/calls/count')
async def get_submission_id_calls_count(submission_id: int):
    return await log_entry_count(submission_id, 'call')


@router.get('/submission/{submission_id}/{script_id}/source')
async def get_submission_id_context_source(submission_id: int, script_id: int):
    async with SessionLocal() as conn:
        cursor = await conn.execute(
            select(ExecutionContexts.src)
            .where(ExecutionContexts.submission_id==submission_id)
            .where(ExecutionContexts.script_id==script_id))
        all_resp = cursor.mappings().all()
    if len(all_resp) == 0:
        raise HTTPException(status_code=404)
    elif len(all_resp) == 1:
        return all_resp[0][0]
    raise HTTPException(status_code=500)


@router.get('/submission/{submission_id}/executiontree')
async def submission_execution_tree(submission_id: int):
    rel_stmt = sql.text('''
        SELECT ec1.script_id AS from_script_id, ec2.script_id AS to_script_id
        FROM vv8_logs.relationships r
        LEFT JOIN vv8_logs.execution_contexts ec1
            ON r.submission_id = ec1.submission_id
            AND r.from_entity = ec1.context_id
        LEFT JOIN vv8_logs.execution_contexts ec2
            ON r.submission_id = ec2.submission_id
            AND r.to_entity = ec2.context_id
        WHERE
            r.submission_id = :submission_id
            AND r.relationship_type = :relationship_type;
    ''')
    async with SessionLocal() as conn:
        cursor = await conn.execute(
            rel_stmt,
            {
                'submission_id': submission_id,
                'relationship_type': RelationshipType.execution_hierarchy
            }
        )
        all_resp = cursor.mappings().all()
        cursor.close()
        rels = [
            dict(row)
            for row in all_resp
        ]
    root = {
        'label': None,
        'children': []
    }
    node_map = {None: root}
    for r in rels:
        to_entity = r['to_script_id']
        from_entity = r['from_script_id']
        if to_entity == None:
            continue
        if from_entity in node_map:
            from_node = node_map[from_entity]
            if to_entity in node_map:
                to_node = node_map[to_entity]
            else:
                to_node = node_map[to_entity] = {
                    'label': to_entity,
                    'children': []
                }
            if to_node not in from_node['children']:
                from_node['children'].append(to_node)
        else:
            if to_entity in node_map:
                to_node = node_map[to_entity]
            else:
                to_node = node_map[to_entity] = {
                    'label': to_entity,
                    'children': []
                }
            node_map[from_entity] = {
                'label': from_entity,
                'children': [to_node]
            }
    # Note: If there is a cycle in the execution context tree. Then this endpoint will raise an error
    #     and fail to parse the tree into json
    return root

# Get the last ten submissions from the database
@router.get('/history')
async def get_history():
    async with SessionLocal() as conn:
        cursor = await conn.execute(
            select(Submission)
            .where(Submission.end_time != None)
            .order_by(Submission.submission_id.desc())
            )
        all_resp = cursor.mappings().all()
    return all_resp
