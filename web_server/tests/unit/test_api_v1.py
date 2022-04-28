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
        self.assertTrue(api_v1.is_url_valid(googleWeb))
        # Testing invalid URLs
        self.assertFalse(api_v1.is_url_valid(invalidWeb))
        self.assertFalse(api_v1.is_url_valid(invalidWeb2))
        self.assertFalse(api_v1.is_url_valid(invalidWeb3))
        self.assertFalse(api_v1.is_url_valid(invalidWeb4))

    # This method tests the valid and invalid condit
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
        hopetrue = api_v1.post_url_submit(googleWeb)
        # Test that Results were posted TODO
        self.assertIsNotNone(webpage.get_results())

        # Testing is_url_valid()
        self.assertTrue(api_v1.is_url_valid(googleWeb))

        # Check to make sure that URL was valid
        hopetrue.submission_id  # add assertion here

        # Run invalid URL, not quite sure what this will return but hopefully pass/fail
        hopefail = api_v1.postUrl(invalidWeb)
        # Test that no Results were posted TODO
        try:
            self.assertIsNone(webpage.get_results())
        except FileNotFoundError:
            self.itpass(self)
        # Check to make sure that URL was invalid
        self.assertFalse(hopefail.valid)

        try:
            hopefail2 = api_v1.post_url_submit(invalidWeb2)
        except HTTPException:
            self.itpass()

        # Run invalid URL, not quite sure what this will return but hopefully pass/fail
        try:
            self.assertIsNone(webpage.get_results())
        except FileNotFoundError:
            self.itpass(self)

        # Check to make sure that URL was invalid
        self.assertFalse(hopefail2.valid)

        try:
            api_v1.get_submission_gets(hopetrue.submission_id)
            api_v1.get_submission_gets_count(hopetrue.submission_id)
            api_v1.get_submission_sets(hopetrue.submission_id)
            api_v1.get_submission_sets_count(hopetrue.submission_id)
            api_v1.get_submission_constructions(hopetrue.submission_id)
            api_v1.get_submission_constructions_count(hopetrue.submission_id)
            api_v1.get_submission_calls(hopetrue.submission_id)
            api_v1.get_submission_calls_count(hopetrue.submission_id)
        except BaseException:
            self.fail("One of the api_v1 getter methods have thrown an error.")


    def test_helper_methods(self):


    def itpass(self):
        return


if __name__ == '__main__':
    unittest.main()

'''

get_submission_gets(submission_id: int)
get_submission_gets_count(submission_id: int)
get_submission_sets(submission_id: int):
get_submission_sets_count(submission_id: int)      
get_submission_constructions(submission_id: int):
get_submission_constructions_count(submission_id: int)
get_submission_calls(submission_id: int):
get_submission_calls_count(submission_id: int  
'''