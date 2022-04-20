import unittest
from vv8web.routers import api_v1 as api_v1
from vv8web.routers import webpage as webpage


# Testing api_v1 and a little bit of webpage, sending a valid webpage and two invalid ones to ensure
# our backend url validation works correctly.
class BackendApiTests(unittest.TestCase):
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
    
#    vv8 worker
#    api_v1
#    task queue unit tests