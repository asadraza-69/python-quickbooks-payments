from abc import ABC, abstractmethod
from app.quickbookspayments.httpclients.request.requestinterface import RequestInterface
from app.quickbookspayments.httpclients.response.responseinterface import ResponseInterface

class InterceptorInterface(ABC):
    """
    Interface for intercepting and modifying HTTP requests and responses.
    """

    @abstractmethod
    def before(self, request: RequestInterface, client) -> None:
        """
        Change the request before the request is going to be sent.

        :param request: The request to be sent.
        :param client: The payment client that handles the request and response.
        """
        pass

    @abstractmethod
    def after(self, response: ResponseInterface, client) -> None:
        """
        Change the response after the response has been received.

        :param response: The response received.
        :param client: The payment client that handles the request and response.
        """
        pass

    @abstractmethod
    def intercept(self, request: RequestInterface, response: ResponseInterface, client) -> None:
        """
        Intercepting the request sent to QuickBooks Online or response received from QuickBooks Online, or both.
        It does not modify the request or response. In order to alter the request or response, use the before() and after() methods.

        :param request: The request to be intercept.
        :param response: The response to be intercept.
        :param client: The payment client that handles the request and response.
        """
        pass
