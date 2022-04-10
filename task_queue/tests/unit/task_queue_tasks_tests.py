import unittest
from task_queue.vv8web_task_queue.tasks import log_parser_tasks as parse_log
from task_queue.vv8web_task_queue.tasks import vv8_worker_tasks as vv8_worker


# Testing api_v1 and a little bit of webpage, sending a valid webpage and two invalid ones to ensure
# our backend url validation works correctly.
class BackendApiTests(unittest.TestCase):
    def test_log_parser_tasks(self):
        self.fail("Not yet implemented")

    def test_vv8_worker_tasks(self):
        self.fail("Not yet implemented")


if __name__ == '__main__':
    unittest.main()
