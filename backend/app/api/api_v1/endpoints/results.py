import aiohttp
from fastapi import APIRouter, HTTPException

# This defines the router object and sets its prefix.
router = APIRouter()

@router.get('/{submission_id}/gets')
async def get_submission_gets(submission_id: int):
    get_url = f'http://database_sidecar:80/api/v1/submission/{submission_id}/gets'
    async with aiohttp.ClientSession() as session:
        async with session.get(get_url) as resp:
            resp.raise_for_status()
            return await resp.json()


@router.get('/{submission_id}/gets/count')
async def get_submission_gets_count(submission_id: int):
    get_url = f'http://database_sidecar:80/api/v1/submission/{submission_id}/gets/count'
    async with aiohttp.ClientSession() as session:
        async with session.get(get_url) as resp:
            resp.raise_for_status()
            return await resp.json()


@router.get('/{submission_id}/sets')
async def get_submission_sets(submission_id: int):
    get_url = f'http://database_sidecar:80/api/v1/submission/{submission_id}/sets'
    async with aiohttp.ClientSession() as session:
        async with session.get(get_url) as resp:
            resp.raise_for_status()
            return await resp.json()


@router.get('/{submission_id}/sets/count')
async def get_submission_sets_count(submission_id: int):
    get_url = f'http://database_sidecar:80/api/v1/submission/{submission_id}/sets/count'
    async with aiohttp.ClientSession() as session:
        async with session.get(get_url) as resp:
            resp.raise_for_status()
            return await resp.json()


@router.get('/{submission_id}/constructions')
async def get_submission_constructions(submission_id: int):
    get_url = f'http://database_sidecar:80/api/v1/submission/{submission_id}/constructions'
    async with aiohttp.ClientSession() as session:
        async with session.get(get_url) as resp:
            resp.raise_for_status()
            return await resp.json()


@router.get('/{submission_id}/constructions/count')
async def get_submission_constructions_count(submission_id: int):
    get_url = f'http://database_sidecar:80/api/v1/submission/{submission_id}/constructions/count'
    async with aiohttp.ClientSession() as session:
        async with session.get(get_url) as resp:
            resp.raise_for_status()
            return await resp.json()


@router.get('/{submission_id}/calls')
async def get_submission_calls(submission_id: int):
    get_url = f'http://database_sidecar:80/api/v1/submission/{submission_id}/calls'
    async with aiohttp.ClientSession() as session:
        async with session.get(get_url) as resp:
            resp.raise_for_status()
            return await resp.json()


@router.get('/{submission_id}/calls/count')
async def get_submission_calls_count(submission_id: int):
    get_url = f'http://database_sidecar:80/api/v1/submission/{submission_id}/calls/count'
    async with aiohttp.ClientSession() as session:
        async with session.get(get_url) as resp:
            resp.raise_for_status()
            return await resp.json()


@router.get('/{submission_id}/{script_id}/source')
async def get_submission_context_source(submission_id: int, script_id: int):
    get_url = f'http://database_sidecar:80/api/v1/submission/{submission_id}/{script_id}/source'
    async with aiohttp.ClientSession() as session:
        async with session.get(get_url) as resp:
            resp.raise_for_status()
            return await resp.json()

@router.get('/{submission_id}/executiontree')
async def get_submission_execution_tree(submission_id: int):
    get_url = f'http://database_sidecar:80/api/v1/submission/{submission_id}/executiontree'
    async with aiohttp.ClientSession() as session:
        async with session.get(get_url) as resp:
            resp.raise_for_status()
            return await resp.json()

# Get the 10 most recent submissions
@router.get('/history')
async def get_history():
    get_url = f'http://database_sidecar:80/api/v1/history'
    async with aiohttp.ClientSession() as session:
        async with session.get(get_url) as resp:
            resp.raise_for_status()
            return await resp.json()