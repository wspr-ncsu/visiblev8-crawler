import sys
from unittest.mock import patch, Mock, MagicMock
# Need to mock imports inside api_v1
celery_mock = sys.modules['celery'] = Mock()
celery_mock.Celery = Mock()


import unittest
import asyncio

from vv8web.routers import api_v1
from vv8web.routers.api_v1 import is_url_valid, post_url_check, post_url_submit, UrlRequestModel, UrlSubmitRequestModel
from vv8web_task_queue.tasks.vv8_worker_tasks import process_url_task
from vv8web_task_queue.tasks.log_parser_tasks import parse_log_task

# Testing api_v1 and a little bit of webpage, sending a valid webpage and two invalid ones to ensure
# our backend url validation works correctly.
class BackendApiTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.loop = asyncio.new_event_loop()

    @classmethod
    def tearDownClass(cls):
        loop = cls.loop
        cls.loop = None
        del loop

    # This method tests api_v1's is_user_valid
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
        self.assertTrue(self.loop.run_until_complete(is_url_valid(googleWeb)))
        # Testing invalid URLs
        self.assertFalse(self.loop.run_until_complete(is_url_valid(invalidWeb)))
        self.assertFalse(self.loop.run_until_complete(is_url_valid(invalidWeb2)))
        self.assertFalse(self.loop.run_until_complete(is_url_valid(invalidWeb3)))
        self.assertFalse(self.loop.run_until_complete(is_url_valid(invalidWeb4)))

        with patch('aiohttp.ClientSession.get') as get_mock:
            get_mock.return_value.__aenter__.return_value.raise_for_status = MagicMock()
            get_mock.return_value.__aenter__.return_value.json.return_value = {"submission_id": 1}

            # Test valid and cached url
            request = UrlRequestModel(url='http://google.com')
            resp = self.loop.run_until_complete(post_url_check(request))
            self.assertTrue(resp.valid)
            self.assertTrue(resp.cached)

            # Test valid not cached url
            request = UrlRequestModel(url='http://google.com')
            get_mock.return_value.__aenter__.return_value.json.return_value = {"submission_id": None}
            resp = self.loop.run_until_complete(post_url_check(request))
            self.assertTrue(resp.valid)
            self.assertFalse(resp.cached)

            # Test invalid url
            request = UrlRequestModel(url='htpp://google.com')
            resp = self.loop.run_until_complete(post_url_check(request))
            self.assertFalse(resp.valid)

    @patch('aiohttp.ClientSession.get')
    @patch('aiohttp.ClientSession.post')
    def test_post_url_submit(self, post_mock, get_mock):
        get_mock.return_value.__aenter__.return_value.raise_for_status = MagicMock()
        get_mock.return_value.__aenter__.return_value.json.return_value = {"submission_id": 1}

        post_mock.return_value.__aenter__.return_value.raise_for_status = MagicMock()
        post_mock.return_value.__aenter__.return_value.json.return_value = {"submission_id": 1}

        # Test submit with cache
        request = UrlSubmitRequestModel(url='http://google.com', rerun=False)
        resp = self.loop.run_until_complete(post_url_submit(request))
        self.assertTrue(resp.submission_id == 1)

        # Test submit with rerun
        request = UrlSubmitRequestModel(url='http://google.com', rerun=True)
        resp = self.loop.run_until_complete(post_url_submit(request))
        self.assertTrue(resp.submission_id == 1)

        # Test submit with no cache
        get_mock.return_value.__aenter__.return_value.json.return_value = {"submission_id": None}
        request = UrlSubmitRequestModel(url='http://google.com', rerun=False)
        resp = self.loop.run_until_complete(post_url_submit(request))
        self.assertTrue(resp.submission_id == 1)

        try:
            self.loop.run_until_complete(api_v1.get_submission_gets(resp.submission_id))
            self.loop.run_until_complete(api_v1.get_submission_gets_count(resp.submission_id))
            self.loop.run_until_complete(api_v1.get_submission_sets(resp.submission_id))
            self.loop.run_until_complete(api_v1.get_submission_sets_count(resp.submission_id))
            self.loop.run_until_complete(api_v1.get_submission_constructions(resp.submission_id))
            self.loop.run_until_complete(api_v1.get_submission_constructions_count(resp.submission_id))
            self.loop.run_until_complete(api_v1.get_submission_calls(resp.submission_id))
            self.loop.run_until_complete(api_v1.get_submission_calls_count(resp.submission_id))
        except BaseException:
            self.fail("One of the api_v1 getter methods have thrown an error.")


if __name__ == '__main__':
    unittest.main()
