import vv8db_sidecar.routers.api_v1 as api_v1
import asyncio

from unittest.mock import patch, MagicMock
from unittest import TestCase
from urllib.parse import urlparse
from vv8db_sidecar.models.parsed_log_model import ParsedLogModel
from vv8db_sidecar.models.submission_model import SubmissionModel
from vv8db_sidecar.models.submission_response_model import SubmissionResponseModel
from vv8db_sidecar.routers.api_v1 import (
    post_submission, post_parsed_log, get_submission_ids, get_recent_submission,
    get_submission_id_gets, get_submission_id_gets_count, get_submission_id_sets,
    get_submission_id_sets_count, get_submission_id_constructions,
    get_submission_id_constructions_count, get_submission_id_calls,
    get_submission_id_calls_count, get_submission_id_context_source
)
from fastapi import APIRouter, HTTPException


# Testing api_v1 in the Database sidecar.
class BackendApiTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.loop = asyncio.new_event_loop()

    @classmethod
    def tearDownClass(cls):
        loop = cls.loop
        cls.loop = None
        del loop

    @patch('sqlalchemy.ext.asyncio.engine.AsyncEngine.connect', return_value=MagicMock())
    def test_post_submission(self, engine_connect_mock):
        cursor_mock = engine_connect_mock.return_value.__aenter__.return_value
        resp_mock = cursor_mock.execute.return_value = MagicMock()
        resp_mock.all.return_value = [(1,)]

        submission = SubmissionModel(url='http://google.com')
        resp = self.loop.run_until_complete(post_submission(submission))
        self.assertTrue(resp.submission_id == 1)

    @patch('sqlalchemy.ext.asyncio.engine.AsyncEngine.connect', return_value=MagicMock())
    def test_post_parse_log(self, engine_connect_mock):
        parsed_log = ParsedLogModel(submission_id=1)
        resp = self.loop.run_until_complete(post_parsed_log(parsed_log))
        self.assertIsNone(resp)

    @patch('sqlalchemy.ext.asyncio.engine.AsyncEngine.connect', return_value=MagicMock())
    def test_get_submission_ids(self, engine_connect_mock):
        cursor_mock = engine_connect_mock.return_value.__aenter__.return_value
        resp_mock = cursor_mock.execute.return_value = MagicMock()

        # Test no submission id
        resp_mock.all.return_value = []
        with self.assertRaises(HTTPException) as ex:
            self.loop.run_until_complete(get_submission_ids(1))
        self.assertEqual(ex.exception.status_code, 404)
        
        # Test with submission id
        resp_mock.all.return_value = [(1,)]
        resp = self.loop.run_until_complete(get_submission_ids(1))
        self.assertEqual(resp.submission_id, 1)
        self.assertTrue(resp.exists)

    @patch('sqlalchemy.ext.asyncio.engine.AsyncEngine.connect', return_value=MagicMock())
    def test_get_recent_submission(self, engine_connect_mock):
        cursor_mock = engine_connect_mock.return_value.__aenter__.return_value
        resp_mock = cursor_mock.execute.return_value = MagicMock()

        # Test no recent submissions
        resp_mock.all.return_value = []
        resp = self.loop.run_until_complete(get_recent_submission('http://foo.com'))
        self.assertIsNone(resp.submission_id)

        # Test valid response
        resp_mock.all.return_value = [(1,)]
        resp = self.loop.run_until_complete(get_recent_submission('http://foo.com'))
        self.assertEqual(resp.submission_id, 1)

        # Test error
        resp_mock.all.return_value = [(1,), (2,)]
        with self.assertRaises(HTTPException) as ex:
            resp = self.loop.run_until_complete(get_recent_submission('http://foo.com'))
        self.assertEqual(ex.exception.status_code, 500)

    @patch('sqlalchemy.ext.asyncio.engine.AsyncEngine.connect', return_value=MagicMock())
    def test_submission_id_gets(self, engine_connect_mock):
        cursor_mock = engine_connect_mock.return_value.__aenter__.return_value
        resp_mock = cursor_mock.execute.return_value = MagicMock()
        resp_mock.mappings.return_value.all.return_value = [{'foo': 'bar'}]

        resp = self.loop.run_until_complete(get_submission_id_gets(1))
        self.assertEqual([{'foo': 'bar'}], resp)

    @patch('sqlalchemy.ext.asyncio.engine.AsyncEngine.connect', return_value=MagicMock())
    def test_get_submission_id_gets_count(self, engine_connect_mock):
        cursor_mock = engine_connect_mock.return_value.__aenter__.return_value
        resp_mock = cursor_mock.execute.return_value = MagicMock()
        resp_mock.scalar.return_value = 10

        resp = self.loop.run_until_complete(get_submission_id_gets_count(1))
        self.assertEqual(resp, 10)

    @patch('sqlalchemy.ext.asyncio.engine.AsyncEngine.connect', return_value=MagicMock())
    def test_submission_id_sets(self, engine_connect_mock):
        cursor_mock = engine_connect_mock.return_value.__aenter__.return_value
        resp_mock = cursor_mock.execute.return_value = MagicMock()
        resp_mock.mappings.return_value.all.return_value = [{'foo': 'bar'}]

        resp = self.loop.run_until_complete(get_submission_id_sets(1))
        self.assertEqual([{'foo': 'bar'}], resp)

    @patch('sqlalchemy.ext.asyncio.engine.AsyncEngine.connect', return_value=MagicMock())
    def test_get_submission_id_sets_count(self, engine_connect_mock):
        cursor_mock = engine_connect_mock.return_value.__aenter__.return_value
        resp_mock = cursor_mock.execute.return_value = MagicMock()
        resp_mock.scalar.return_value = 10

        resp = self.loop.run_until_complete(get_submission_id_sets_count(1))
        self.assertEqual(resp, 10)

    @patch('sqlalchemy.ext.asyncio.engine.AsyncEngine.connect', return_value=MagicMock())
    def test_get_submission_id_constructions(self, engine_connect_mock):
        cursor_mock = engine_connect_mock.return_value.__aenter__.return_value
        resp_mock = cursor_mock.execute.return_value = MagicMock()
        resp_mock.mappings.return_value.all.return_value = [{'arguments': 'foo'}]

        resp = self.loop.run_until_complete(get_submission_id_constructions(1))
        self.assertEqual([{'arguments': 'foo'}], resp)

    @patch('sqlalchemy.ext.asyncio.engine.AsyncEngine.connect', return_value=MagicMock())
    def test_get_get_submission_id_constructions_count(self, engine_connect_mock):
        cursor_mock = engine_connect_mock.return_value.__aenter__.return_value
        resp_mock = cursor_mock.execute.return_value = MagicMock()
        resp_mock.scalar.return_value = 10

        resp = self.loop.run_until_complete(get_submission_id_constructions_count(1))
        self.assertEqual(resp, 10)

    @patch('sqlalchemy.ext.asyncio.engine.AsyncEngine.connect', return_value=MagicMock())
    def test_get_submission_id_calls(self, engine_connect_mock):
        cursor_mock = engine_connect_mock.return_value.__aenter__.return_value
        resp_mock = cursor_mock.execute.return_value = MagicMock()
        resp_mock.mappings.return_value.all.return_value = [{'arguments': 'foo'}]

        resp = self.loop.run_until_complete(get_submission_id_calls(1))
        self.assertEqual([{'arguments': ['foo']}], resp)

    @patch('sqlalchemy.ext.asyncio.engine.AsyncEngine.connect', return_value=MagicMock())
    def test_get_get_submission_id_calls_count(self, engine_connect_mock):
        cursor_mock = engine_connect_mock.return_value.__aenter__.return_value
        resp_mock = cursor_mock.execute.return_value = MagicMock()
        resp_mock.scalar.return_value = 10

        resp = self.loop.run_until_complete(get_submission_id_calls_count(1))
        self.assertEqual(resp, 10)

    @patch('sqlalchemy.ext.asyncio.engine.AsyncEngine.connect', return_value=MagicMock())
    def test_get_submission_id_context_source(self, engine_connect_mock):
        cursor_mock = engine_connect_mock.return_value.__aenter__.return_value
        resp_mock = cursor_mock.execute.return_value = MagicMock()

        # Test not found
        resp_mock.all.return_value = []
        with self.assertRaises(HTTPException) as ex:
            resp = self.loop.run_until_complete(get_submission_id_context_source(1, 2))
        self.assertEqual(ex.exception.status_code, 404)

        # Test valid response
        resp_mock.all.return_value = [('source code',)]
        resp = self.loop.run_until_complete(get_submission_id_context_source(1, 2))
        self.assertEqual(resp, 'source code')

        # Test error
        resp_mock.all.return_value = [('this',), ('shouldnt',), ('happen',)]
        with self.assertRaises(HTTPException) as ex:
            resp = self.loop.run_until_complete(get_submission_id_context_source(1, 2))
        self.assertEqual(ex.exception.status_code, 500)


if __name__ == '__main__':
    unittest.main()
