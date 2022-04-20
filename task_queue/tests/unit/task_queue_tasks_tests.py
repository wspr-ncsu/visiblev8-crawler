import unittest
from task_queue.vv8web_task_queue.tasks import log_parser_tasks as parse_log
from task_queue.vv8web_task_queue.tasks import vv8_worker_tasks as vv8_worker


# Testing log_parser_tasks, sending a valid webpage and two invalid ones to ensure
# our backend is connected correctly.
class BackendApiTests(unittest.TestCase):
    def test_log_parser_tasks(self):

        # Import our test documents and parsed test documents
        log_files = [
            'akamai.net.txt',
            'https-__appleinsider.com.txt',
            'https-__coinsbit.io.txt',
            'https-__iqoption.txt'
        ]
        parsed_files = [
            'akamai.net_parsed.json',
            'https-__appleinsider.com_parsed.json',
            'https-__coinsbit.io_parsed.json',
            'https-__iqoption_parsed.json'
        ]

        # Create a valid log and submission id for testing
        log = log_files[0]
        submission_id = 11

        try:
            # Submit it to log_parser_tasks and see if it submits correctly.
            var = parse_log.parse_log_task(log, submission_id)
        except BaseException:
            # if there is an https error, fail the test
            self.fail("Did not work")

        # Retrieve file from database with submission id and make sure it matches TODO

        # Create a invalid log and submission id for testing
        inval_log = 'https-__applenside.com.txt'
        inval_submission_id = 1111
        run = bool(False)

        try:
            # Submit it to log_parser_tasks and see if it submits correctly.
            var = parse_log.parse_log_task(inval_log, inval_submission_id)
            run = bool(True)
            self.fail("Should have failed.")
        except BaseException:
            # if there is an https error, fail the test
            self.assertFalse(run)

    def test_vv8_worker_tasks(self):

        # Import our test documents and parsed test documents
        log_files = [
            'akamai.net.txt',
            'https-__appleinsider.com.txt',
            'https-__coinsbit.io.txt',
            'https-__iqoption.txt'
        ]
        parsed_files = [
            'akamai.net_parsed.json',
            'https-__appleinsider.com_parsed.json',
            'https-__coinsbit.io_parsed.json',
            'https-__iqoption_parsed.json'
        ]

        # Create a valid log and submission id for testing
        url = log_files[0]
        submission_id = 1

        resp = "bad"

        try:
            resp = vv8_worker.process_url_task(self, url, submission_id)
        except BaseException:
            self.fail("Not yet implemented")

        if resp == "bad":
            self.fail("vv8 worker didn't return full log")

        filepath = "The File Path"  # TODO

        try:
            vv8_worker.remove_entry(filepath)
        except BaseException:
            self.fail("Not yet implemented")


if __name__ == '__main__':
    unittest.main()

'''
def parse_log_task(log, submission_id):
    print(f'log_parser parse_log_task: log: {log[:30]}, submission_id: {submission_id}')
    # Nested import is used since definition to task function has to exist to schedule a task
    # This is not a pretty solution, but it is a side effect of how celery works.
    # Ideally celery would not need a function definition to schedule a task, but it is what it is
    import vv8web_task_queue.config.database_sidecar_config as db_cfg
    parsed_log_post_url = f'http://{db_cfg.db_sc_host}:{db_cfg.db_sc_port}/api/v1/parsedlog'
    parsed_log = parse_log(log, submission_id)
    # Send log data to database
    r = requests.post(parsed_log_post_url, json=parsed_log.to_json())
    # Raise error if HTTP error occured
    r.raise_for_status()
'''