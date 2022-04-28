import unittest
from urllib.parse import urlparse
from vv8db_sidecar.routers.api_v1 import api_v1
from vv8db_sidecar.models.parsed_log_model import ParsedLogModel
from vv8db_sidecar.models.submission_model import SubmissionModel
from vv8db_sidecar.models.submission_response_model import SubmissionResponseModel


@dataclass
class SubmissionIdExistsResponse:
    submission_id: int
    exists: bool


@dataclass
class RecentSubmissionResponse:
    submission_id: int | None


# Testing api_v1 in the Database sidecar.
class BackendApiTests(unittest.TestCase):

    # Quick method for try-excepts that are supposed to fail
    def itpass(self):
        return

    # This method tests postsubmission(), and makes sure many of the other simple functions can run without
    # breaking
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

        try:
            api_v1.get_recent_submission()
        except HTTPException:
            self.fail("get_recent_submission() threw unexpected HTTPException.")

        # Testing get_submission_id_gets and get_submission_id_sets
        try:
            self.assertNotEqual(api_v1.get_submission_id_sets_count(1), 0)
            self.assertNotEqual(api_v1.get_submission_id_constructions_count(1), 0)
            self.assertNotEqual(api_v1.get_submission_id_calls_count(1), 0)
            # Need to run these simply to ensure they can
            api_v1.get_history()

            api_v1.get_submission_ids(1)
            api_v1.get_submission_id_sets(1)
            api_v1.get_submission_id_gets(1)
            api_v1.get_submission_id_constructions(1)
            api_v1.get_submission_id_calls(1)

            api_v1.submission_execution_tree(1)
        except BaseException:
            self.fail("dbsidecar.api_vi_test.get_submission_id_gets or get_submission_id_sets has failed.")

    # This method is testing post_parsed_log() and get_submission_ids() with a valid submission
    def test_post_parsed_log(self):
        # Import our test documents and parsed test documents
        log_files = [
            'akamai.net.txt',
            # 'https-__appleinsider.com.txt',
            # 'https-__coinsbit.io.txt',
            # 'https-__iqoption.txt'
        ]
        parsed_files = [
            'akamai.net_parsed.json',
            # 'https-__appleinsider.com_parsed.json',
            # 'https-__coinsbit.io_parsed.json',
            # 'https-__iqoption_parsed.json'
        ]

        # Create new parsed log model for testing
        testSub = ParsedLogModel
        testSub.url = 'akamai.net_parsed.json'
        testSub.submission_id = 10

        # Submit testSub, then check the database(?) to see if it was submitted?
        try:
            subReturn = api_v1.post_parsed_log(testSub)
        except BaseException:
            self.fail("dbsidecar.api_vi_test.test_post_parsed_log has failed.")

        # Testing get_submission_ids()
        # Check to see if we can retrieve testSub's ID
        try:
            subId = api_v1.get_submission_ids(10)
            self.assertTrue( subId.exists )
        except BaseException:
            self.fail("dbsidecar.api_vi_test.test_get_submission_ids has failed.")
            
        # Error check for an invalid submission id
        try:
            subId = api_v1.get_submission_ids(11)
            self.fail("dbsidecar.api_vi_test.test_get_submission_ids has failed.")
        except HTTPException:
            self.itpass()
    
    # Testing get_recent_submissions() with no recent submissions and get_submission_ids() with no submissions.
    def test_get_recent_submission(self):

        try:
            noSub = api_v1.get_recent_submission()
            self.assertIsInstance(noSub, RecentSubmissionResponse)
        except HTTPException:
            self.fail("get_recent_submission() threw unexpected HTTPException.")

        try:
            api_v1.get_submission_ids(10)
            self.fail("test_get_recent_submission should have thrown an HTTPException")
        except HTTPException:
            self.itpass()

    # Testing get_submission_id_context_source() with no recent submissions
    def test_get_submission_id_context_source(self):

        try:
            api_v1.get_submission_id_context_source(10, 10)
            self.fail("test_get_recent_submission should have thrown an HTTPException")
        except HTTPException:
            self.itpass()


if __name__ == '__main__':
    unittest.main()