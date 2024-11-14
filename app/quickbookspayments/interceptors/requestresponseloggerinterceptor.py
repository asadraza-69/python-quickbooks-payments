import datetime
import json
import os

from app.quickbookspayments.interceptors.interceptorinterface import InterceptorInterface
from app.quickbookspayments.httpclients.request.requestinterface import RequestInterface
from app.quickbookspayments.httpclients.response.responseinterface import ResponseInterface
from app.quickbookspayments.paymentclient import PaymentClient


class RequestResponseLoggerInterceptor(InterceptorInterface):
    def __init__(self, directory: str, timezone: str):
        self.set_log_directory(directory)
        self.set_time_zone(timezone)

    def before(self, request: RequestInterface, client: PaymentClient) -> None:
        pass

    def after(self, response: ResponseInterface, client: PaymentClient) -> None:
        pass

    def intercept(self, request: RequestInterface, response: ResponseInterface, client: PaymentClient) -> None:
        self.log_request(request)
        self.log_response(response)

    def log_request(self, request: RequestInterface) -> None:
        file_name = self.generate_unique_file_name(request)
        file_path = self.get_file_path(file_name)
        input_data = self.write_type(request) \
                     + self.write_url(request) \
                     + self.write_header(request) \
                     + self.write_body(request)
        self.write_to_file(file_path, input_data)

    def write_to_file(self, file_name: str, content: str) -> None:
        try:
            with open(file_name, 'w') as fp:
                fp.write(content)
        except Exception as e:
            raise RuntimeError(f"Could not open the file: {file_name} to write content: {str(e)}")

    def get_file_path(self, file_name: str) -> str:
        if file_name.endswith('/'):
            return os.path.join(self.log_folder_location, file_name)
        else:
            return os.path.join(self.log_folder_location, file_name)

    def log_response(self, response: ResponseInterface) -> None:
        file_name = self.generate_unique_file_name(response)
        file_path = self.get_file_path(file_name)
        input_data = self.write_type(response) \
                     + self.write_url(response) \
                     + self.write_header(response) \
                     + self.write_body(response)
        self.write_to_file(file_path, input_data)

    def generate_unique_file_name(self, request_or_response: object) -> str:
        type_str = "Request" if isinstance(request_or_response, RequestInterface) else "Response"
        return f"{type_str}_{self.format_current_time()}_U{os.urandom(8).hex()}.txt"

    def format_current_time(self) -> str:
        return self.get_current_time().replace('-', '_').replace(' ', '_').replace(':', '_')

    def get_current_time(self) -> str:
        now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=int(self.timezone))))
        return now.strftime('%Y-%m-%d %H:%M:%S')

    def write_type(self, request_or_response: object) -> str:
        type_str = "Request" if isinstance(request_or_response, RequestInterface) else "Response"
        return f"{type_str} at [{self.get_current_time()}]{self.section_divider()}"

    def write_url(self, request_or_response: object) -> str:
        request = request_or_response if isinstance(request_or_response,
                                                    RequestInterface) else request_or_response.get_associated_request()
        return f"{request.get_method()} {request.get_url()}{self.section_divider()}"

    def write_header(self, request_or_response: object) -> str:
        headers = request_or_response.get_header()
        collapsed_headers = [f"{key}: {val}" for key, val in headers.items() if key != "Authorization"]
        return "\n".join(collapsed_headers) + self.section_divider()

    def write_body(self, request_or_response: object) -> str:
        body = request_or_response.get_body()
        return self.pretty_print(body) + self.section_divider()

    def pretty_print(self, json_str: str) -> str:
        return json.dumps(json.loads(json_str), indent=4)

    def section_divider(self) -> str:
        return "\n\n==================================\n\n"

    def set_log_directory(self, directory: str) -> None:
        self.check_is_directory_writable(directory)
        self.log_folder_location = directory

    def get_log_directory(self) -> str:
        return self.log_folder_location

    def check_is_directory_writable(self, directory: str) -> None:
        if not os.path.isdir(directory) or not os.access(directory, os.W_OK):
            raise RuntimeError(f"{directory} is either not a valid directory or is not writable.")

    def set_time_zone(self, time_zone: str) -> None:
        self.time_zone = time_zone

    def config(self, configuration: dict) -> None:
        pass
