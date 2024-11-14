from abc import ABC, abstractmethod
from typing import Dict, Optional
from app.quickbookspayments.httpclients.request.requestinterface import RequestInterface

class ResponseInterface(ABC):
    """
    Interface defining the methods for handling responses from HTTP requests.
    """

    @abstractmethod
    def set_response_status(self, status_code: int) -> 'ResponseInterface':
        """
        Set the response status code and check if the request failed.
        Updates the failure status if the status code is not 2xx.
        """
        pass

    @abstractmethod
    def set_header(self, response_header: dict):
        """
        Set the response headers.
        """
        pass

    @abstractmethod
    def set_body(self, response_body: str):
        """
        Set the response body.
        """
        pass

    @abstractmethod
    def set_associated_request(self, associated_request: RequestInterface) -> 'ResponseInterface':
        """
        Set the associated request for the response.
        """
        pass

    @abstractmethod
    def get_status_code(self) -> int:
        """
        Return the status code of the response.
        """
        pass

    @abstractmethod
    def get_url(self) -> str:
        """
        Return the URL of the request.
        """
        pass

    @abstractmethod
    def get_header(self) -> Dict[str, str]:
        """
        Return the response headers.
        """
        pass

    @abstractmethod
    def get_body(self) -> Optional[str]:
        """
        Return the response body.
        """
        pass

    @abstractmethod
    def failed(self) -> bool:
        """
        Return True if the request failed based on the status code.
        """
        pass

    @abstractmethod
    def get_intuit_tid(self) -> str:
        """
        Return the Intuit Transaction ID (intuit_tid).
        """
        pass

    @abstractmethod
    def get_content_type(self) -> str:
        """
        Return the content type of the response.
        """
        pass

    @abstractmethod
    def get_associated_request(self) -> RequestInterface:
        """
        Return the associated request.
        """
        pass

    @abstractmethod
    def get_request_id(self) -> str:
        """
        Return the request ID.
        """
        pass
