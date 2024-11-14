import unittest

from app.quickbookspayments.httpclients import RequestType, RequestInterface, RequestFactory, IntuitRequest


class RequestTest(unittest.TestCase):

    # Test if we can create a request through the factory method
    def test_can_create_request_through_factory_method(self) -> None:
        intuit_request = RequestFactory.create_standard_intuit_request(RequestType.OAUTH)

        self.assertIsInstance(
            intuit_request,
            IntuitRequest
        )

    # Test the request method functionality
    def test_request_method(self) -> None:
        intuit_request = RequestFactory.create_standard_intuit_request(RequestType.OAUTH)
        intuit_request.set_method(RequestInterface.GET)
        self.assertEqual(
            "GET",
            intuit_request.get_method()
        )
        intuit_request.set_method(RequestInterface.POST)
        self.assertEqual(
            "POST",
            intuit_request.get_method()
        )


if __name__ == '__main__':
    unittest.main()
