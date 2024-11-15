import json

from random import randint
from app.quickbookspayments.oauth.oauth2authenticator import OAuth2Authenticator


class OAuth2Test:
    # Private method to create an OAuth2Authenticator client
    @staticmethod
    def create_client() -> 'OAuth2Authenticator':
        oauth2_helper = OAuth2Authenticator.create({
            'client_id': 'ABv5rkSV3iPCNQWrge5vQThCPY2QXLNR035dep5vfFfS9lVmQV',
            'client_secret': 'D9rTK64BsGi3fsQ8J5cuF4gmwIXG36u92hCTCLJT',
            'redirect_uri': 'https://developer.intuit.com/v2/OAuth2Playground/RedirectUrl',
            'environment': 'development'
        })
        return oauth2_helper


if __name__ == '__main__':
    oauth2_helper = OAuth2Test.create_client()
    get_client_id = oauth2_helper.get_client_id()
    get_client_secret = oauth2_helper.get_client_secret()

    get_redirect_uri = oauth2_helper.get_redirect_uri()
    discovery_url = oauth2_helper.get_discovery_urls()
    endpoint = discovery_url.get_userinfo_endpoint_url()
    state = oauth2_helper.get_state()

    scope = "com.intuit.quickbooks.accounting openid profile email phone address"
    authorization_code_url = oauth2_helper.generate_auth_code_url(scope)
    state = oauth2_helper.get_state()
    oauth2_helper.set_state("intuit")
    authorization_code_url = oauth2_helper.generate_auth_code_url(scope, "turbo")

    scope = "com.intuit.quickbooks.accounting openid profile email phone address"
    state = "aState" + str(randint(100000, 999999))
    authorization_code_url = oauth2_helper.generate_auth_code_url(scope, state)
    expected_url = (
            "https://appcenter.intuit.com/connect/oauth2?client_id=ABv5rkSV3iPCNQWrge5vQThCPY2QXLNR035dep5vfFfS9lVmQV"
            "&scope=com.intuit.quickbooks.accounting%20openid%20profile%20email%20phone%20address"
            "&redirect_uri=https%3A%2F%2Fdeveloper.intuit.com%2Fv2%2FOAuth2Playground%2FRedirectUrl"
            "&response_type=code&state=" + state
    )
    request = oauth2_helper.create_request_to_exchange("code")
    body = request.get_body()
    array = body.split('&')
    set_code = array[1].split('=')[1]
    header = request.get_header()
    authorization_header = "Basic TDB2bU1aSWZ3VUJmdjlQUE05NmR6TVRZQVRuTHM2VFNBZTVTeVZrdDFaNE1Bc3ZsQ1U6MlpabkNubkR5b1p4VWxWQ1AxRDlYN2toeEEzenVYTXlKRTRjSFhkcQ=="
    generated_authorization_header = header['Authorization']

    body = request.get_body()
    body_array = body.split('&')
    refresh_token_generated = body_array[1].split('=')[1]

    request = oauth2_helper.create_request_to_revoke(refresh_token)
    body = json.dumps({"token": refresh_token})
    actual_body = request.get_body()

    request = oauth2_helper.create_request_for_user_info(access_token)
    header = request.get_header()
