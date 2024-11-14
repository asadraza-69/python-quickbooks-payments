import json
import base64
import random

from app.quickbookspayments.httpclients.request.requestinterface import RequestInterface
from src import RequestFactory
from app.quickbookspayments.httpclients.request.requesttype import RequestType
from .discoveryurls import DiscoveryURLs
from .discoverysandboxurls import DiscoverySandboxURLs
from .oauth1encrypter import OAuth1Encrypter
class OAuth2Authenticator:
    def __init__(self, settings):
        self.set_keys_from_map(settings)

    @staticmethod
    def create(settings):
        if settings:
            return OAuth2Authenticator(settings)
        else:
            raise ValueError("Empty OAuth keys")

    def set_keys_from_map(self, settings):
        try:
            self.set_client_id(settings['client_id'])
            self.set_client_secret(settings['client_secret'])
            self.set_redirect_uri(settings['redirect_uri'])
            self.set_environment(settings['environment'])
        except Exception as e:
            raise ValueError(f"Fail reading OAuth 2 keys from: {settings}")

    def set_environment(self, environment):
        env = environment.lower()
        if env.startswith("prod"):
            self.set_discovery_urls(DiscoveryURLs())
        else:
            self.set_discovery_urls(DiscoverySandboxURLs())

    def generate_auth_code_url(self, scope, user_defined_state="state") -> str:
        if self.is_user_pass_state(user_defined_state):
            self.set_state(user_defined_state)
        else:
            self.generate_state_if_not_set()
        self.set_scope(scope)

        return f"{self.get_discovery_urls().get_authorization_endpoint_url()}?" + \
               self.generate_query_parameter_string_for_authorization_code_url()

    def create_request_to_exchange(self, code):
        request = RequestFactory.create_standard_intuit_request(RequestType.OAUTH)
        request.set_method(RequestInterface.POST) \
               .set_url(self.get_discovery_urls().get_token_endpoint_url()) \
               .set_header(self.generate_header_for_token_request()) \
               .set_body(self.generate_body_for_token_request(code))
        return request

    def create_request_to_refresh(self, refresh_token):
        request = RequestFactory.create_standard_intuit_request(RequestType.OAUTH)
        request.set_method(RequestInterface.POST) \
               .set_url(self.get_discovery_urls().get_token_endpoint_url()) \
               .set_header(self.refresh_token_header()) \
               .set_body(self.refresh_token_body(refresh_token))
        return request

    def create_request_to_revoke(self, token):
        request = RequestFactory.create_standard_intuit_request(RequestType.OAUTH)
        request.set_method(RequestInterface.POST) \
               .set_url(self.get_discovery_urls().get_revocation_endpoint_url()) \
               .set_header(self.revoke_token_header()) \
               .set_body(self.revoke_token_body(token))
        return request

    def create_request_for_user_info(self, access_token):
        request = RequestFactory.create_standard_intuit_request(RequestType.USERINFO)
        request.set_method(RequestInterface.GET) \
               .set_url(self.get_discovery_urls().get_userinfo_endpoint_url()) \
               .set_header(self.user_info_header(access_token))
        return request

    def create_request_to_migrate_token(self, consumer_key, consumer_secret, oauth1_access_token, oauth1_token_secret, scopes):
        request = RequestFactory.create_standard_intuit_request(RequestType.OAUTH)
        oauth1_encrypter = OAuth1Encrypter(consumer_key, consumer_secret, oauth1_access_token, oauth1_token_secret)
        request.set_method(RequestInterface.POST) \
               .set_url(self.get_discovery_urls().get_migration_endpoint_url()) \
               .set_header(self.migration_authorization_header(oauth1_encrypter, self.get_discovery_urls().get_migration_endpoint_url())) \
               .set_body(self.migration_body(scopes))
        return request

    def migration_authorization_header(self, oauth1_encrypter, base_url):
        authorization_header_info = oauth1_encrypter.get_oauth_header(base_url, {}, RequestInterface.POST)
        return {
            'Accept': 'application/json',
            'Authorization': authorization_header_info,
            'Content-Type': 'application/json'
        }

    def migration_body(self, scope):
        body = {
            'scope': scope,
            'redirect_uri': "https://developer.intuit.com/v2/OAuth2Playground/RedirectUrl",
            'client_id': self.get_client_id(),
            'client_secret': self.get_client_secret()
        }
        return json.dumps(body)

    def user_info_header(self, access_token):
        return {
            'Accept': 'application/json',
            'Authorization': f"Bearer {access_token}"
        }

    def revoke_token_header(self):
        return {
            'Accept': 'application/json',
            'Authorization': self.generate_authorization_header(),
            'Content-Type': 'application/json'
        }

    def revoke_token_body(self, token):
        body = {
            "token": token
        }
        return json.dumps(body)

    def refresh_token_header(self):
        return {
            'Accept': "application/json",
            'Authorization': self.generate_authorization_header(),
            'Content-Type': "application/x-www-form-urlencoded",
        }

    def refresh_token_body(self, refresh_token):
        body = {
            'grant_type': 'refresh_token',
            'refresh_token': str(refresh_token)
        }
        return '&'.join(f"{key}={value}" for key, value in body.items())

    def generate_body_for_token_request(self, code):
        body = {
            'grant_type': 'authorization_code',
            'code': str(code),
            'redirect_uri': self.get_redirect_uri()
        }
        return '&'.join(f"{key}={value}" for key, value in body.items())

    def generate_header_for_token_request(self):
        return {
            'Accept': 'application/json',
            'Authorization': self.generate_authorization_header(),
            'Content-Type': 'application/x-www-form-urlencoded'
        }

    def generate_authorization_header(self):
        encoded_client_id_client_secrets = base64.b64encode(f"{self.get_client_id()}:{self.get_client_secret()}".encode()).decode()
        return f"Basic {encoded_client_id_client_secrets}"

    def is_user_pass_state(self, state):
        return not (state and state == "state")

    def generate_state_if_not_set(self):
        current_state = self.get_state()
        if current_state is None:
            tmp_state = ''.join(chr(random.randint(65, 90)) for _ in range(5))
            self.set_state(tmp_state)

    def generate_query_parameter_string_for_authorization_code_url(self):
        parameters = {
            'client_id': self.get_client_id(),
            'scope': self.get_scope(),
            'redirect_uri': self.get_redirect_uri(),
            'response_type': 'code',
            'state': self.get_state()
        }
        return '&'.join(f"{key}={value}" for key, value in parameters.items())

    def set_state(self, state):
        self.state = state

    def get_client_id(self):
        return self.client_id

    def set_client_id(self, client_id):
        self.client_id = client_id
        return self

    def get_client_secret(self):
        return self.client_secret

    def set_client_secret(self, client_secret):
        self.client_secret = client_secret
        return self

    def get_redirect_uri(self):
        return self.redirect_uri

    def set_redirect_uri(self, redirect_uri):
        self.redirect_uri = redirect_uri
        return self

    def get_state(self):
        return self.state

    def get_scope(self):
        return self.scope

    def set_scope(self, scope):
        self.scope = scope
        return self

    def get_discovery_urls(self):
        return self.discoveryURLs

    def set_discovery_urls(self, discovery_urls):
        self.discoveryURLs = discovery_urls
        return self

