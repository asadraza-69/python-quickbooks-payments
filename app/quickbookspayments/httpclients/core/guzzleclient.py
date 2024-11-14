import requests
from app.quickbookspayments.httpclients.core.httpclientinterface import HttpClientInterface
from app.quickbookspayments.httpclients.request.requestinterface import RequestInterface
from app.quickbookspayments.httpclients.response.responsefactory import ResponseFactory
from app.quickbookspayments.httpclients.response.responseinterface import ResponseInterface


class GuzzleClient(HttpClientInterface):
    def __init__(self):
        try:
            self.guzzle_client = requests.Session()
        except ImportError:
            raise RuntimeError("Cannot find requests library.")

        self.connection_time_out = 10
        self.request_time_out = 100
        self.is_verify_ssl = True
        self.last_request = None
        self.enable_debug = False
        self.information = None

    def set_timeout(self, user_set_connection_timeout: int, user_set_request_timeout: int) -> None:
        self.connection_time_out = user_set_connection_timeout
        self.request_time_out = user_set_request_timeout

    def set_verify_ssl(self, is_built_in_ssl_verifier_used: bool) -> None:
        self.is_verify_ssl = is_built_in_ssl_verifier_used

    def send(self, request: RequestInterface) -> ResponseInterface:
        if not request:
            raise RuntimeError("Cannot send an empty request.")
        self.last_request = request
        guzzle_options = self.prepare(request)
        try:
            guzzle_response = self.guzzle_client.request(
                method=request.get_method(), url=request.get_url(), **guzzle_options)
        except requests.exceptions.RequestException as e:
            return self.create_response_for_failure_request(e, request)
        return self.create_response_for_successful_request(guzzle_response, request)

    def create_response_for_failure_request(self, e, request: RequestInterface):
        body = e.response.text if e.response else ""
        headers = {k: v for k, v in e.response.headers.items()} if e.response else {}
        status_code = e.response.status_code if e.response else 500
        return ResponseFactory.create_standard_intuit_response(status_code, headers, body, request)

    def create_response_for_successful_request(self, guzzle_response, request: RequestInterface):
        status_code = guzzle_response.status_code
        headers = {k: v for k, v in guzzle_response.headers.items()}
        body = guzzle_response.text
        return ResponseFactory.create_standard_intuit_response(status_code, headers, body, request)

    def simplify_array_headers(self, headers):
        return {k: v[0] for k, v in headers.items()}

    def prepare(self, request: RequestInterface):
        options = {}
        if request.get_method().upper() == "POST":
            options['data'] = request.get_body()
        if self.is_verify_ssl:
            options['verify'] = '/path/to/certfile'
        else:
            options['verify'] = False
        options['headers'] = request.get_header()
        options['timeout'] = self.request_time_out
        return options

    def get_last_sent_request(self) -> RequestInterface:
        return self.last_request

    def enable_debug(self) -> None:
        self.enable_debug = True

    def get_debug_info(self):
        return self.information
