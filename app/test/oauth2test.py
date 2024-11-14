import unittest

from app.quickbookspayments.httpclients.request.requestinterface import RequestInterface
from app.quickbookspayments.oauth.discoverysandboxurls import DiscoverySandboxURLs, OAuth1Encrypter
from app.quickbookspayments.oauth.oauth1encrypter import OAuth1Encrypter
from app.quickbookspayments.oauth.oauth2authenticator import OAuth2Authenticator


class OAuth2Test(unittest.TestCase):
    # Private method to create an OAuth2Authenticator client
    def create_client(self) -> 'OAuth2Authenticator':
        oauth2_helper = OAuth2Authenticator.create({
            'client_id': 'L0vmMZIfwUBfv9PPM96dzMTYATnLs6TSAe5SyVkt1Z4MAsvlCU',
            'client_secret': '2ZZnCnnDyoZxUlVCP1D9X7khxA3zuXMyJE4cHXdq',
            'redirect_uri': 'https://developer.intuit.com/v2/OAuth2Playground/RedirectUrl',
            'environment': 'development'
        })
        return oauth2_helper

    # Test to check if the OAuth2Helper is created correctly with the provided values
    def test_can_create_an_oauth2_helper_with_values(self) -> None:
        oauth2_helper = self.create_client()
        self.assertEqual(
            'L0vmMZIfwUBfv9PPM96dzMTYATnLs6TSAe5SyVkt1Z4MAsvlCU',
            oauth2_helper.get_client_id()
        )
        self.assertEqual(
            '2ZZnCnnDyoZxUlVCP1D9X7khxA3zuXMyJE4cHXdq',
            oauth2_helper.get_client_secret()
        )
        self.assertEqual(
            'https://developer.intuit.com/v2/OAuth2Playground/RedirectUrl',
            oauth2_helper.get_redirect_uri()
        )
        self.assertIsInstance(
            oauth2_helper.get_discovery_urls(),
            DiscoverySandboxURLs
        )

    # Test to check if the correct discovery URLs are loaded
    def test_if_correct_discovery_urls_load(self) -> None:
        oauth2_helper = self.create_client()
        discovery_url = oauth2_helper.get_discovery_urls()
        self.assertEqual(
            "https://sandbox-accounts.platform.intuit.com/v1/openid_connect/userinfo",
            discovery_url.get_userinfo_endpoint_url()
        )

    # Test to check if the state can be changed
    def test_if_state_can_be_changed(self) -> None:
        oauth2_helper = self.create_client()
        self.assertIsNone(
            oauth2_helper.get_state()
        )
        scope = "com.intuit.quickbooks.accounting openid profile email phone address"
        authorization_code_url = oauth2_helper.generate_auth_code_url(scope)
        self.assertIsNotNone(
            oauth2_helper.get_state()
        )

        oauth2_helper.set_state("intuit")
        authorization_code_url = oauth2_helper.generate_auth_code_url(scope)
        self.assertEqual(
            "intuit",
            oauth2_helper.get_state()
        )

        authorization_code_url = oauth2_helper.generate_auth_code_url(scope, "turbo")
        self.assertEqual(
            "turbo",
            oauth2_helper.get_state()
        )

    # Test to generate the authorization code URL
    def test_generate_authorization_code_url(self) -> None:
        oauth2_helper = self.create_client()
        scope = "com.intuit.quickbooks.accounting openid profile email phone address"
        state = "aState" + str(randint(100000, 999999))

        authorization_code_url = oauth2_helper.generate_auth_code_url(scope, state)
        expected_url = (
                "https://appcenter.intuit.com/connect/oauth2?client_id=L0vmMZIfwUBfv9PPM96dzMTYATnLs6TSAe5SyVkt1Z4MAsvlCU"
                "&scope=com.intuit.quickbooks.accounting%20openid%20profile%20email%20phone%20address"
                "&redirect_uri=https%3A%2F%2Fdeveloper.intuit.com%2Fv2%2FOAuth2Playground%2FRedirectUrl"
                "&response_type=code&state=" + state
        )
        self.assertEqual(expected_url, authorization_code_url)

    # Test to check if exchange code for tokens works correctly
    def test_if_exchange_code_for_tokens_is_correct(self) -> None:
        oauth2_helper = self.create_client()
        code = "someCode"
        request = oauth2_helper.create_request_to_exchange(code)
        self.assertIsInstance(
            request,
            RequestInterface
        )

        body = request.get_body()
        self.assertIsInstance(
            body,
            str
        )
        array = body.split('&')
        set_code = array[1].split('=')[1]

        self.assertEqual(
            code,
            set_code
        )

        authorization_header = "Basic TDB2bU1aSWZ3VUJmdjlQUE05NmR6TVRZQVRuTHM2VFNBZTVTeVZrdDFaNE1Bc3ZsQ1U6MlpabkNubkR5b1p4VWxWQ1AxRDlYN2toeEEzenVYTXlKRTRjSFhkcQ=="
        header = request.get_header()
        self.assertIsInstance(
            header,
            dict
        )

        generated_authorization_header = header['Authorization']
        self.assertEqual(
            authorization_header,
            generated_authorization_header
        )

    # Test to request a refresh token
    def test_can_request_refresh_token(self) -> None:
        oauth2_helper = self.create_client()
        refresh_token = "someRefreshToken"
        request = oauth2_helper.create_request_to_refresh(refresh_token)
        self.assertIsInstance(
            request,
            RequestInterface
        )

        body = request.get_body()
        self.assertIsInstance(body, str)
        body_array = body.split('&')
        refresh_token_generated = body_array[1].split('=')[1]

        self.assertEqual(
            refresh_token_generated,
            refresh_token
        )

    # Test to revoke a token
    def test_can_revoke(self) -> None:
        oauth2_helper = self.create_client()
        refresh_token = "someRefreshToken"
        request = oauth2_helper.create_request_to_revoke(refresh_token)

        body = json.dumps({"token": refresh_token})
        actual_body = request.get_body()

        self.assertEqual(
            actual_body,
            body
        )

    # Test to get user info
    def test_get_user_info(self) -> None:
        oauth2_helper = self.create_client()
        access_token = "accessToken"
        request = oauth2_helper.create_request_for_user_info(access_token)
        self.assertIsInstance(
            request,
            RequestInterface
        )

        header = request.get_header()
        self.assertEqual(
            header['Authorization'],
            "Bearer " + access_token
        )

    # Test to check if OAuth1 signature generator signs correctly
    def test_oauth1_sig_generator_sign_correctly(self) -> None:
        consumer_key = "qyprdUSoVpIHrtBp0eDMTHGz8UXuSz"
        consumer_secret = "TKKBfdlU1I1GEqB9P3AZlybdC8YxW5qFSbuShkG7"
        oauth1_access_token = "qyprd5jgTqKPpZvNUM5OOLDEoPthaUnYRkDGP5o8Z4vmbUx5"
        oauth1_token_secret = "kFKirS5qfbj1j5naG2eRiHMROwsAS1AhW4aNweI1"
        scopes = "com.intuit.quickbooks.accounting"
        encrypter = OAuth1Encrypter(consumer_key, consumer_secret, oauth1_access_token, oauth1_token_secret)
        encrypter.set_nounce_for_test("NjM2OTI4NDM3NDQzNjQyNDUw")
        encrypter.set_time_for_test("1557272144")

        authorization_header_info = encrypter.get_oauth_header(
            "https://developer-sandbox.api.intuit.com/v2/oauth2/tokens/migrate",
            {},
            RequestInterface.POST
        )
        array = authorization_header_info.split(",")
        sig = array[6].split("=")
        result = sig[1].replace('"', "").replace("'", "")
        self.assertEqual(
            result,
            "hbXtg1Foug2WKXEu%2Fz1lRpe5rbk%3D"
        )


if __name__ == '__main__':
    unittest.main()
