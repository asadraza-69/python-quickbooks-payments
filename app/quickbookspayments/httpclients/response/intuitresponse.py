from typing import Dict, Any
from app.quickbookspayments.httpclients.request.requestinterface import RequestInterface
from app.quickbookspayments.httpclients.core.coreconstants import CoreConstants

class IntuitResponse:
    def __init__(self):
        self.code: int = 0
        self.url: str = ""
        self.header: Dict[str, str] = {}
        self.body: Any = None
        self.failure: bool = False
        self.intuit_tid: str = ""
        self.content_type: str = ""
        self.request: RequestInterface = None
        self.request_id: str = ""

    def set_response_status(self, status_code: int) -> "IntuitResponse":
        self.code = status_code
        self.check_if_request_is_failed(status_code)
        return self

    def check_if_request_is_failed(self, status_code: int):
        if status_code < 200 or status_code >= 300:
            self.failure = True
        else:
            self.failure = False

    def get_status_code(self) -> int:
        return self.code

    def get_url(self) -> str:
        return self.url

    def set_header(self, response_header: Dict[str, str] or str) -> "IntuitResponse":
        if isinstance(response_header, str):
            self.header = self.convert_string_header_to_dict(response_header)
        else:
            self.header = response_header
            self.intuit_tid = response_header.get('intuit_tid', '')
            self.content_type = response_header.get('Content-Type', '')
        return self

    def convert_string_header_to_dict(self, raw_headers: str) -> Dict[str, str]:
        headers = {}
        raw_headers = raw_headers.replace("\r\n", "\n")
        response_headers_rows = raw_headers.strip().split("\n")
        for line in response_headers_rows:
            if ": " not in line:
                continue
            key, value = line.split(": ", 1)
            headers[key] = value
            self.set_content_type(key, value)
            self.set_intuit_tid(key, value)
        return headers

    def get_header(self) -> Dict[str, str]:
        return self.header

    def set_body(self, response_body: Any) -> "IntuitResponse":
        self.body = response_body
        return self

    def get_body(self) -> Any:
        return self.body

    def failed(self) -> bool:
        return self.failure

    def set_intuit_tid(self, key: str, val: str):
        if key.strip().lower() == CoreConstants.INTUIT_TID.lower():
            self.intuit_tid = val.strip()

    def get_intuit_tid(self) -> str:
        return self.intuit_tid

    def set_content_type(self, key: str, val: str):
        if key.strip().lower() == CoreConstants.CONTENT_TYPE.lower():
            self.content_type = val.strip()

    def get_content_type(self) -> str:
        return self.content_type

    def set_associated_request(self, associated_request: RequestInterface) -> "IntuitResponse":
        self.request = associated_request
        self.request_id = associated_request.get_request_id()
        self.url = associated_request.get_url()
        return self

    def get_associated_request(self) -> RequestInterface:
        return self.request

    def set_request_id(self, request_id: str):
        self.request_id = request_id

    def get_request_id(self) -> str:
        return self.request_id
