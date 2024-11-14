# Import necessary modules and classes
import json
import random
import string

from app.quickbookspayments.oauth.oauth2authenticator import OAuth2Authenticator
from app.quickbookspayments.paymentclient import PaymentClient


# Function to create the PaymentClient instance
def create_client() -> PaymentClient:
    return PaymentClient()


# Function to create the OAuth2Authenticator instance
def create_oauth2_helper() -> OAuth2Authenticator:
    oauth2_helper = OAuth2Authenticator.create({
        'client_id': 'ABv5rkSV3iPCNQWrge5vQThCPY2QXLNR035dep5vfFfS9lVmQV',
        'client_secret': 'D9rTK64BsGi3fsQ8J5cuF4gmwIXG36u92hCTCLJT',
        'redirect_uri': 'https://developer.intuit.com/v2/OAuth2Playground/RedirectUrl',
        'environment': 'sandbox'
    })
    return oauth2_helper


def generate_request_id():
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(20))
    return random_string


if __name__ == '__main__':
    # Create a PaymentClient instance
    client = create_client()

    # Create an OAuth2Authenticator instance
    oauth2_helper = create_oauth2_helper()

    # Define the scope for OAuth
    scope = "com.intuit.quickbooks.accounting openid profile email phone address"

    # Generate the authorization code URL
    authorization_code_url = oauth2_helper.generate_auth_code_url(scope)
    # Redirect User to the authorization_code_url, and a code will be sent to your redirect_uri as query parameter

    # Simulate receiving a code after user authorization
    code = generate_request_id()

    # Create a request to exchange the code for tokens
    request = oauth2_helper.create_request_to_exchange(code)

    # Send the request using the client
    response = client.send(request)

    # Check if the response indicates a failure
    if response.failed():
        code = response.get_status_code()
        error_message = response.get_body()
        print(f"code is {code}")
        print(f"body is {error_message}")
    else:
        # Get the keys from the response
        response_body = json.loads(response.get_body())
        refresh_token = response_body["refresh_token"]
        print(f"Refresh token: {refresh_token}")
        # Example refresh token: AB11570127472xkApQcZmbTMGfzzEOgMWl2Br5h8IEgxRULUbO
