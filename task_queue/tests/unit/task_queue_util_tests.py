import unittest
from task_queue.vv8web_task_queue.util import log_parser_v2 as parse_log
from web_server.vv8web.routers import webpage as webpage


# Testing api_v1 and a little bit of webpage, sending a valid webpage and two invalid ones to ensure
# our backend url validation works correctly.
class BackendApiTests(unittest.TestCase):
    def test_api_connections(self):
        self.fail("Not yet implemented")


if __name__ == '__main__':
    unittest.main()
