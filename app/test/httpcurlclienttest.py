import unittest
from app.quickbookspayments.oauth.oauth2authenticator import OAuth2Authenticator
from app.quickbookspayments.httpclients.request.requestfactory import RequestFactory
from app.quickbookspayments.httpclients.request.intuitrequest import IntuitRequest
from app.quickbookspayments.httpclients.core.httpcurlclient import HttpCurlClient

class HttpCurlClientTest(unittest.TestCase):

    def create_client(self) -> OAuth2Authenticator:
        oauth2_helper = OAuth2Authenticator.create({
            'client_id': 'L0vmMZIfwUBfv9PPM96dzMTYATnLs6TSAe5SyVkt1Z4MAsvlCU',
            'client_secret': '2ZZnCnnDyoZxUlVCP1D9X7khxA3zuXMyJE4cHXdq',
            'redirect_uri': 'https://developer.intuit.com/v2/OAuth2Playground/RedirectUrl',
            'environment': 'development'
        })
        return oauth2_helper

    def enable_debug_for_curl(self, request, is_verify_ssl):
        curl_client = HttpCurlClient()
        curl_client.set_verify_ssl(is_verify_ssl)
        base_curl = curl_client.enable_debug()
        response = curl_client.send(request)
        information = curl_client.get_debug_info()
        request_header = information['request_header'].split('\n')

        for header in request_header:
            if 'Authorization' in header:
                authorization_value = header.split(":")
                self.assertEqual(
                    request.get_header()['Authorization'],
                    authorization_value[1].strip()
                )

        curl_url = information['url']
        self.assertEqual(request.get_url(), curl_url)

        ssl_verify_result = information['ssl_verify_result']
        self.assertEqual(ssl_verify_result, 0)

    def test_exchange_code_request_sent_by_curl_client(self):
        oauth2_helper = self.create_client()
        code = "L011557358660z3axu8cgM7YHVyRGAaU63Ap0hgtEzfdkgwu5d"
        request = oauth2_helper.create_request_to_exchange(code)
        self.enable_debug_for_curl(request, True)

    def test_refresh_token_request_sent_by_curl_client(self):
        oauth2_helper = self.create_client()
        token = "refreshToken"
        request = oauth2_helper.create_request_to_refresh(token)
        self.enable_debug_for_curl(request, True)

    def test_user_info_request_sent_by_curl_client(self):
        oauth2_helper = self.create_client()
        token = "accessToken"
        request = oauth2_helper.create_request_for_user_info(token)
        self.enable_debug_for_curl(request, True)

    def test_migrate_request_sent_by_curl_client(self):
        oauth2_helper = self.create_client()
        consumer_key = "qyprdUSoVpIHrtBp0eDMTHGz8UXuSz"
        consumer_secret = "TKKBfdlU1I1GEqB9P3AZlybdC8YxW5qFSbuShkG7"
        oauth1_access_token = "qyprd5jgTqKPpZvNUM5OOLDEoPthaUnYRkDGP5o8Z4vmbUx5"
        oauth1_token_secret = "kFKirS5qfbj1j5naG2eRiHMROwsAS1AhW4aNweI1"
        scopes = "com.intuit.quickbooks.accounting"
        request = oauth2_helper.create_request_to_migrate_token(consumer_key, consumer_secret, oauth1_access_token, oauth1_token_secret, scopes)
        self.enable_debug_for_curl(request, True)

    def test_do_not_verify_ssl(self):
        oauth2_helper = self.create_client()
        code = "L011557358660z3axu8cgM7YHVyRGAaU63Ap0hgtEzfdkgwu5d"
        request = oauth2_helper.create_request_to_exchange(code)
        self.enable_debug_for_curl(request, False)

if __name__ == '__main__':
    unittest.main()
