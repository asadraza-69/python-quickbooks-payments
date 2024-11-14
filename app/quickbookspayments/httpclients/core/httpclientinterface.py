from abc import ABC, abstractmethod
from app.quickbookspayments.httpclients.request.requestinterface import RequestInterface
from app.quickbookspayments.httpclients.response.responsefactory import ResponseFactory
from app.quickbookspayments.httpclients.response.responseinterface import ResponseInterface

class HttpClientInterface(ABC):
    """
    A Parent Interface for all the Http Clients

    @package QuickBooksOnline
    """

    @abstractmethod
    def send(self, request: RequestInterface) -> ResponseInterface:
        pass

    @abstractmethod
    def get_last_sent_request(self) -> RequestInterface:
        pass

    @abstractmethod
    def set_verify_ssl(self, is_built_in_ssl_verifier_used: bool) -> None:
        """
        Depends on the Framework you are using, you want to either let the SDK
        do SSL verification for you, or let the framework do it.

        By default, the HttpClient will check the SSL config for you to make sure everything is
        working as expected. You will need to use set_verify_ssl(False) to disable it.
        """
        pass

    @abstractmethod
    def set_timeout(self, connection_timeout: int, request_timeout: int) -> None:
        pass

    @abstractmethod
    def enable_debug(self) -> None:
        """
        Allow User to enable this for debugging purpose.
        """
        pass

    @abstractmethod
    def get_debug_info(self):
        pass
