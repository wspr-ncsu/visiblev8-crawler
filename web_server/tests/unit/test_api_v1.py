import unittest
from vv8web.routers import api_v1 as api_v1
from vv8web.routers import webpage as webpage
from vv8web_task_queue.tasks.vv8_worker_tasks import process_url_task
from vv8web_task_queue.tasks.log_parser_tasks import parse_log_task


class UrlSubmitRequestModel(BaseModel):
    url: str
    rerun: Optional[bool] = False


@dataclass
class UrlSubmitResponseModel:
    submission_id: int


# Testing api_v1 and a little bit of webpage, sending a valid webpage and two invalid ones to ensure
# our backend url validation works correctly.
class BackendApiTests(unittest.TestCase):
    def test_is_url_valid(self):
        # Valid URL
        googleWeb = "https://www.google.com"
        # Invalid http/https scheme
        invalidWeb = "htpps://www.google.com"
        # Invalid URL
        invalidWeb2 = "http://www.ggogle.com"
        # Invalid Character in URL
        invalidWeb3 = "http://www.?gogle.com"
        # Invalid URL length (0)
        invalidWeb4 = ""

        # Testing valid is_url_valid()
        self.assertTrue(api_v1.is_url_valid(googleWeb))
        # Testing invalid URLs
        self.assertFalse(api_v1.is_url_valid(invalidWeb))
        self.assertFalse(api_v1.is_url_valid(invalidWeb2))
        self.assertFalse(api_v1.is_url_valid(invalidWeb3))
        self.assertFalse(api_v1.is_url_valid(invalidWeb4))

    def test_post_url_check(self):

        # Valid URL
        googleWeb = "https://www.google.com"
        # Invalid http/https scheme
        invalidWeb = "htpps://www.google.com"

        # Testing api_v1.UrlRequestModel(googleWeb)
        self.assertTrue(api_v1.post_url_check(api_v1.UrlRequestModel(googleWeb)).valid)
        # Testing api_v1.UrlRequestModel(invalidWeb)
        self.assertFalse(api_v1.post_url_check(api_v1.UrlRequestModel(invalidWeb)).valid)

    def test_post_url_submit(self):
        # Valid URL
        googleWeb = "https://www.google.com"
        # Invalid http/https scheme
        invalidWeb = "htpps://www.google.com"

    def test_api_connections(self):

        # Valid URL
        googleWeb = "https://www.google.com"
        # Invalid http/https scheme
        invalidWeb = "htpps://www.google.com"
        # Invalid URL
        invalidWeb2 = "http://www.ggogle.com"

        # Run valid URL, not quite sure what this will return but hopefully pass/fail or bool
        hopetrue = api_v1.postUrl(googleWeb)
        # Test that Results were posted TODO
        self.assertIsNotNone(webpage.get_results())

        # Testing is_url_valid()
        self.assertTrue(api_v1.is_url_valid(googleWeb))


        # Check to make sure that URL was valid
        self.assertTrue(hopetrue.valid)  # add assertion here

        # Run invalid URL, not quite sure what this will return but hopefully pass/fail
        hopefail = api_v1.postUrl(invalidWeb)
        # Test that no Results were posted TODO
        try:
            self.assertIsNone(webpage.get_results())
        except FileNotFoundError:
            self.itpass(self)
        # Check to make sure that URL was invalid
        self.assertFalse(hopefail.valid)

        # Run invalid URL, not quite sure what this will return but hopefully pass/fail
        hopefail2 = api_v1.postUrl(invalidWeb2)
        # Test that no Results were posted TODO
        try:
            self.assertIsNone(webpage.get_results())
        except FileNotFoundError:
            self.itpass(self)
        # Check to make sure that URL was invalid
        self.assertFalse(hopefail2.valid)

    def itpass(self):
        return


if __name__ == '__main__':
    unittest.main()

'''
# Handles processing url submission and returns submission id
@router.post('/urlsubmit', response_model=UrlSubmitResponseModel)
async def post_url_submit(request: UrlSubmitRequestModel):
    url = request.url
    rerun = request.rerun
    if not await is_url_valid(url):
        raise HTTPException(status_code=400, detail='Invalid URL')
    submission_id = None
    async with aiohttp.ClientSession() as session:
        if not rerun:
            # If not rerun we need to check for a cached version of this url
            params = {'url': urllib.parse.quote(url)}
            async with session.get('http://database_sidecar:80/api/v1/submission', params=params) as resp:
                resp.raise_for_status()
                resp_data = await resp.json()
                submission_id = resp_data['submission_id']
                assert submission_id is None or isinstance(submission_id, int)
        if rerun or submission_id is None:
            # Create submission id
            async with session.post('http://database_sidecar:80/api/v1/submission', json={'url': url}) as resp:
                resp.raise_for_status()
                sub_resp = await resp.json()
                submission_id = sub_resp['submission_id']
            # Run the pipeline
            url_pipeline = celery.chain(process_url_task.s(), parse_log_task.s(submission_id))
            async_res = url_pipeline.apply_async((url, submission_id))
            # pipeline completion poll interval
            poll_interval = 0.5
            while not async_res.ready():
                await asyncio.sleep(poll_interval)
            # We do not need the result, so just forget it.
            # Need to call get() or forget() to release resources maintaining async state
            async_res.forget()
        # return submission id
        assert isinstance(submission_id, int)
        return UrlSubmitResponseModel(submission_id)


@router.get('/submission/{submission_id}/gets')
async def get_submission_gets(submission_id: int):
    get_url = f'http://database_sidecar:80/api/v1/submission/{submission_id}/gets'
    async with aiohttp.ClientSession() as session:
        async with session.get(get_url) as resp:
            resp.raise_for_status()
            return await resp.json()


@router.get('/submission/{submission_id}/gets/count')
async def get_submission_gets_count(submission_id: int):
    get_url = f'http://database_sidecar:80/api/v1/submission/{submission_id}/gets/count'
    async with aiohttp.ClientSession() as session:
        async with session.get(get_url) as resp:
            resp.raise_for_status()
            return await resp.json()


@router.get('/submission/{submission_id}/sets')
async def get_submission_sets(submission_id: int):
    get_url = f'http://database_sidecar:80/api/v1/submission/{submission_id}/sets'
    async with aiohttp.ClientSession() as session:
        async with session.get(get_url) as resp:
            resp.raise_for_status()
            return await resp.json()


@router.get('/submission/{submission_id}/sets/count')
async def get_submission_sets_count(submission_id: int):
    get_url = f'http://database_sidecar:80/api/v1/submission/{submission_id}/sets/count'
    async with aiohttp.ClientSession() as session:
        async with session.get(get_url) as resp:
            resp.raise_for_status()
            return await resp.json()


@router.get('/submission/{submission_id}/constructions')
async def get_submission_constructions(submission_id: int):
    get_url = f'http://database_sidecar:80/api/v1/submission/{submission_id}/constructions'
    async with aiohttp.ClientSession() as session:
        async with session.get(get_url) as resp:
            resp.raise_for_status()
            return await resp.json()


@router.get('/submission/{submission_id}/constructions/count')
async def get_submission_constructions_count(submission_id: int):
    get_url = f'http://database_sidecar:80/api/v1/submission/{submission_id}/constructions/count'
    async with aiohttp.ClientSession() as session:
        async with session.get(get_url) as resp:
            resp.raise_for_status()
            return await resp.json()


@router.get('/submission/{submission_id}/calls')
async def get_submission_calls(submission_id: int):
    get_url = f'http://database_sidecar:80/api/v1/submission/{submission_id}/calls'
    async with aiohttp.ClientSession() as session:
        async with session.get(get_url) as resp:
            resp.raise_for_status()
            return await resp.json()


@router.get('/submission/{submission_id}/calls/count')
async def get_submission_calls_count(submission_id: int):
    get_url = f'http://database_sidecar:80/api/v1/submission/{submission_id}/calls/count'
    async with aiohttp.ClientSession() as session:
        async with session.get(get_url) as resp:
            resp.raise_for_status()
            return await resp.json()
        
'''