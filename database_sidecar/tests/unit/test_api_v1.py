import unittest
from urllib.parse import urlparse
from vv8db_sidecar.routers.api_v1 import api_v1
from vv8db_sidecar.models.parsed_log_model import ParsedLogModel
from vv8db_sidecar.models.submission_model import SubmissionModel
from vv8db_sidecar.models.submission_response_model import SubmissionResponseModel


# Testing api_v1 in the Database sidecar. We need to test two functions: postsubmission and post_parsed_log
class BackendApiTests(unittest.TestCase):
    def test_postsubmission(self):

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

        # Create new submission model for testing
        testSub = SubmissionModel('akamai.net.txt')

        # Send the submission model through postsubmission
        # Check to make sure the response is of type SubmissionResponseModel
        # (No failure testing bc we assume any url that has made it this far is valid)
        subReturn = null

        try:
            subReturn = api_v1.postsubmission(testSub)
            self.assertIsInstance(subReturn, SubmissionResponseModel)
        except BaseException:
            self.fail("dbsidecar.api_vi_test.test_postsubmission has failed.")

        # Test to make sure the submission response is what we expected
        self.assertEqual(subReturn.submission_id, 1)


    def itpass(self):
        return

'''
    def test_post_parsed_log(self):
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

        # Create new parsed log model for testing
        testSub = ParsedLogModel
        testSub.url = 'akamai.net_parsed.json'

        # Submit testSub, then check the database(?) to see if it was submitted?
        try:
            subReturn = api_v1.post_parsed_log(testSub)
        except BaseException:
            self.fail("dbsidecar.api_vi_test.test_post_parsed_log has failed.")
'''


if __name__ == '__main__':
    unittest.main()
