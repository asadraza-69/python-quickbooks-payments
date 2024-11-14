import random
import string

class ClientContext:
    SANDBOX_URL = "https://sandbox.api.intuit.com"
    PRODUCTION_URL = "https://api.intuit.com"

    def __init__(self, context=None):
        self.access_token = None
        self.refresh_token = None
        self.environment = None
        self.base_url = None

        if context:
            self.access_token = context.get('access_token')
            self.refresh_token = context.get('refresh_token')
            self.set_environment(context.get('environment', ""))

    @staticmethod
    def generate_request_id():
        characters = string.ascii_letters + string.digits
        random_string = ''.join(random.choice(characters) for _ in range(20))
        return random_string

    def get_standard_header_with_request_id(self, request_id):
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Request-Id': request_id,
            'Authorization': f"Bearer {self.access_token}"
        }

    def get_standard_header_with_request_id_for_delete(self, request_id):
        return {
            'Content-Type': 'application/json',
            'Request-Id': request_id,
            'Authorization': f"Bearer {self.access_token}"
        }

    def get_non_auth_header_with_request_id(self, request_id):
        return {
            'Accept': 'application/json',
            'Request-Id': request_id,
            'Content-Type': 'application/json'
        }

    def get_access_token(self):
        return self.access_token

    def set_access_token(self, access_token):
        self.access_token = access_token

    def get_refresh_token(self):
        return self.refresh_token

    def set_refresh_token(self, refresh_token):
        self.refresh_token = refresh_token

    def set_environment(self, environment):
        env = environment.lower()
        if env.startswith("prod"):
            self.base_url = ClientContext.PRODUCTION_URL
        else:
            self.base_url = ClientContext.SANDBOX_URL

    def get_base_url(self):
        return self.base_url

    def set_base_url(self, base_url):
        self.base_url = base_url
