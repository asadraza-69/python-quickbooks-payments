from abc import ABC, abstractmethod

class RequestInterface(ABC):
    GET = "GET"
    POST = "POST"
    DELETE = "DELETE"

    @property
    @abstractmethod
    def method(self):
        pass

    @method.setter
    @abstractmethod
    def method(self, method):
        pass

    @property
    @abstractmethod
    def url(self):
        pass

    @url.setter
    @abstractmethod
    def url(self, url):
        pass

    @property
    @abstractmethod
    def header(self):
        pass

    @header.setter
    @abstractmethod
    def header(self, header):
        pass

    @property
    @abstractmethod
    def body(self):
        pass

    @body.setter
    @abstractmethod
    def body(self, body):
        pass

    @property
    @abstractmethod
    def request_type(self):
        pass

    @request_type.setter
    @abstractmethod
    def request_type(self, request_type):
        pass

    @property
    @abstractmethod
    def request_id(self):
        pass

    @request_id.setter
    @abstractmethod
    def request_id(self, request_id):
        pass
