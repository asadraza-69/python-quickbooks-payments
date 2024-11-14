from app.quickbookspayments.httpclients.response.intuitresponse import IntuitResponse
from app.quickbookspayments.httpclients.request.requestinterface import RequestInterface


class ResponseFactory:
    """
    Factory class for creating a standard IntuitResponse object.
    """

    @staticmethod
    def create_standard_intuit_response(http_status_code: int, raw_headers: dict, raw_body: str,
                                        request: RequestInterface) -> 'ResponseInterface':
        """
        Creates and returns an IntuitResponse object with the given parameters.

        :param http_status_code: The HTTP status code of the response.
        :param raw_headers: The raw response headers.
        :param raw_body: The raw response body.
        :param request: The associated request object.
        :return: An IntuitResponse object populated with the given data.
        """
        response = IntuitResponse()
        response.set_response_status(http_status_code)
        response.set_header(raw_headers)
        response.set_body(raw_body)
        response.set_associated_request(request)
        return response
