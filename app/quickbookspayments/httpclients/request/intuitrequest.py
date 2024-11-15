from app.quickbookspayments.httpclients.request.requestinterface import RequestInterface

class IntuitRequest(RequestInterface):
    def __init__(self, type):
        self._method = None
        self._url = None
        self._header = None
        self._body = None
        self._request_type = None
        self._request_id = None
        self.set_request_type(type)

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, method):
        self._method = method

    def set_method(self, method):  # Converted to PEP8
        self.method = method
        return self

    def get_method(self):  # Converted to PEP8
        return self.method

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        if not url:
            raise ValueError("invalid URL.")
        self._url = url

    def get_url(self):  # Converted to PEP8
        return self.url

    def set_url(self, url):  # Converted to PEP8
        if not url:
            raise ValueError("invalid URL.")
        self.url = url
        return self

    @property
    def header(self):
        return self._header

    @header.setter
    def header(self, header):
        if header and isinstance(header, dict):
            self._header = header
            self.add_request_id_from_header(header)
        else:
            raise ValueError("invalid header for request")

    def get_header(self):  # Converted to PEP8
        return self.header

    def set_header(self, header):  # Converted to PEP8
        if header and isinstance(header, dict):
            self.header = header
            self.add_request_id_from_header(header)
        else:
            raise ValueError("invalid header for request")
        return self

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, body):
        if self.method != RequestInterface.POST:
            raise ValueError("Cannot set body for GET request")
        self._body = body

    def get_body(self):  # Converted to PEP8
        return self.body

    def set_body(self, body):  # Converted to PEP8
        if self.get_method() != RequestInterface.POST:
            raise ValueError("Cannot Set body for GET request")
        self.body = body
        return self

    @property
    def request_type(self):
        return self._request_type

    @request_type.setter
    def request_type(self, request_type):
        self._request_type = request_type

    def get_request_type(self):  # Converted to PEP8
        return self.request_type

    def set_request_type(self, type):  # Converted to PEP8
        self.request_type = type

    @property
    def request_id(self):
        return self._request_id

    @request_id.setter
    def request_id(self, request_id):
        self._request_id = request_id

    def get_request_id(self):  # Converted to PEP8
        return self.request_id

    def set_request_id(self, request_id):  # Converted to PEP8
        self.request_id = request_id

    def add_request_id_from_header(self, header):  # Converted to PEP8
        if (self.request_type != "OAUTH" and self.request_type != "USERINFO"):
            self.request_id = header['Request-Id']

