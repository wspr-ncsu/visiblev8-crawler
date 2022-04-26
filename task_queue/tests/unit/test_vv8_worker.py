import unittest
import uuid
import io

# from vv8web_task_queue.tasks import log_parser_tasks as parse_log
from vv8web_task_queue.tasks import vv8_worker_tasks as vv8_worker


# Testing log_parser_tasks, sending a valid webpage and two invalid ones to ensure
# our backend is connected correctly.
class Vv8WorkerTests(unittest.TestCase):

    def test_valid_vv8_worker_tasks(self):
        url = 'https://google.com'
        submission_id = 1

        temp_request_id = vv8_worker.process_url_task.request.id
        vv8_worker.process_url_task.request.id = str(uuid.uuid4())
        log = vv8_worker.process_url_task.run(url, submission_id)
        vv8_worker.process_url_task.request.id = temp_request_id

        line_tags = {'~', '@', '$', '!', 'c', 'n', 'g', 's'}
        for line in io.StringIO(log):
            self.assertTrue(line[0] in line_tags)

        self.assertTrue(isinstance(log, str))
        self.assertTrue(len(log) > 0)


if __name__ == '__main__':
    unittest.main()

