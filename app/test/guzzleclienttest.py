import unittest
from app.quickbookspayments.oauth.oauth2authenticator import OAuth2Authenticator
from app.quickbookspayments.httpclients.request.requestfactory import RequestFactory
from app.quickbookspayments.httpclients.request.intuitrequest import IntuitRequest
from app.quickbookspayments.httpclients.core.guzzleclient import GuzzleClient



class GuzzleClientTest(unittest.TestCase):

    def create_client(self) -> OAuth2Authenticator:
        oauth2_helper = OAuth2Authenticator.create({
            'client_id': 'Q0K5t9wvMNSAMxsxfydrKY9RqBwIMCLF2wt8kOs9L4z6V69XuY',
            'client_secret': 'DoMR0sxz4aRqpizlc1XD5hwVLcN1Ep8MtPuOIJFs',
            'redirect_uri': 'https://developer.intuit.com/v2/OAuth2Playground/RedirectUrl',
            'environment': 'development'
        })
        return oauth2_helper

    def test_exchange_code_request_sent_by_guzzle_client(self):
        oauth2_helper = self.create_client()
        code = "AB11582326772xz6uxiWcSg4OxkVr6uzEiwibGVBKm32MuiEle"
        request = oauth2_helper.create_request_to_exchange(code)
        client = GuzzleClient()
        response = client.send(request)
        self.assertEqual(
            response.get_url(),
            request.get_url()
        )

    def test_success_refresh_token_sent_by_guzzle_client(self):
        oauth2_helper = self.create_client()
        token = "AB11582326772xz6uxiWcSg4OxkVr6uzEiwibGVBKm32MuiEle"
        request = oauth2_helper.create_request_to_refresh(token)
        client = GuzzleClient()
        response = client.send(request)
        response_body = json.loads(response.get_body())
        self.assertEqual(
            token,
            response_body["refresh_token"]
        )


if __name__ == '__main__':
    unittest.main()
