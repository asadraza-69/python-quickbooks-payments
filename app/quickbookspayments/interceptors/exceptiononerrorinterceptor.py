from app.quickbookspayments.interceptors.interceptorinterface import InterceptorInterface
from app.quickbookspayments.httpclients.request.requestinterface import RequestInterface
from app.quickbookspayments.httpclients.response.responseinterface import ResponseInterface
from app.quickbookspayments.paymentclient import PaymentClient


class ExceptionOnErrorInterceptor(InterceptorInterface):
    def before(self, request: RequestInterface, client: PaymentClient):
        pass

    def after(self, response: ResponseInterface, client: PaymentClient):
        if response.failed():
            request = response.get_associated_request()
            raise RuntimeError(
                f"Request: [{request.get_method()} {request.get_request_type()}] {request.get_url()} failed: {response.get_body()} intuit-tid: {response.get_intuit_tid()}")

    def intercept(self, request: RequestInterface, response: ResponseInterface, client: PaymentClient):
        pass
