from app.quickbookspayments.httpclients.core.basecurl import BaseCurl
from app.quickbookspayments.httpclients.core.httpclientinterface import HttpClientInterface
from app.quickbookspayments.httpclients.request.requestinterface import RequestInterface
from app.quickbookspayments.httpclients.response.responsefactory import ResponseFactory
from app.quickbookspayments.httpclients.response.responseinterface import ResponseInterface


class HttpCurlClient(HttpClientInterface):
    def __init__(self):
        self.base_curl = BaseCurl()
        self.connection_time_out = 10
        self.request_time_out = 100
        self.is_verify_ssl = True
        self.enable_debug = False
        self.information = None
        self.last_request = None

    def set_timeout(self, connection_timeout: int, request_timeout: int) -> None:
        self.connection_time_out = connection_timeout
        self.request_time_out = request_timeout

    def set_verify_ssl(self, is_built_in_ssl_verifier_used: bool) -> None:
        self.is_verify_ssl = is_built_in_ssl_verifier_used

    def send(self, request: RequestInterface) -> ResponseInterface:
        if not request:
            raise RuntimeError("Cannot send an empty request.")

        self.last_request = request
        self.prepare(request)
        curl_response = self.base_curl.execute(request)
        self.handle_curl_errors()
        response = self.parse_curl_response(curl_response, request)

        if self.enable_debug:
            self.information = self.base_curl.getCurl()

        self.close_connection()
        return response

    def execute(self):
        return self.base_curl.execute()

    def handle_curl_errors(self):
        if self.base_curl.errno() or self.base_curl.error():
            error_msg = self.base_curl.error()
            error_number = self.base_curl.getInfo('http_code')
            raise RuntimeError(
                f"cURL error during making API call. cURL Error Number:[{error_number}] with error:[{error_msg}]")

    def parse_curl_response(self, curl_response, request) -> ResponseInterface:
        header_size = self.base_curl.getInfo('header_size')
        raw_headers = curl_response.headers
        raw_body = curl_response.text
        http_status_code = self.base_curl.getInfo('http_code')

        return ResponseFactory.create_standard_intuit_response(http_status_code, raw_headers, raw_body, request)

    def close_connection(self):
        self.base_curl.close()

    def get_last_sent_request(self) -> RequestInterface:
        return self.last_request

    def prepare(self, request: RequestInterface) -> None:
        self.intialize_curl()
        if self.enable_debug:
            self.enable_header_out()
        self.base_curl.session.headers.update(request.get_header())
        self.base_curl.session.url = request.get_url()
        if request.get_method().upper() == "POST":
            self.set_post_body_and_method(request)
        else:
            self.base_curl.session.method = request.get_method().upper()

        self.base_curl.session.verify = self.is_verify_ssl
        if self.is_verify_ssl:
            self.set_ssl_config()
        else:
            self.accept_all()
        self.update_curl_settings()

    def enable_header_out(self):
        # Placeholder for setting CURLINFO_HEADER_OUT to true in requests
        pass

    def intialize_curl(self):
        if not self.base_curl.session:
            self.base_curl = BaseCurl()

    def set_post_body_and_method(self, request: RequestInterface):
        self.base_curl.session.method = "POST"
        self.base_curl.session.data = request.get_body()

    def set_ssl_config(self):
        self.base_curl.session.verify = '/path/to/certfile'

    def accept_all(self):
        self.base_curl.session.verify = False

    def update_curl_settings(self):
        self.base_curl.session.timeout = (self.connection_time_out, self.request_time_out)
        self.base_curl.session.return_response = True
        self.base_curl.session.headers = True

    def enable_debug(self) -> None:
        self.enable_debug = True

    def get_debug_info(self):
        return self.information
