from app.quickbookspayments.httpclients.request.requestinterface import RequestInterface
from app.quickbookspayments.httpclients.request.requestfactory import RequestFactory
from app.quickbookspayments.httpclients.request.requesttype import RequestType
from app.quickbookspayments.modules.echeck import ECheck


class ECheckOperations:
    def __init__(self):
        pass

    @staticmethod
    def build_from(data):
        return ECheck(data)

    @staticmethod
    def debit(debit_body: ECheck, request_id: str, context) -> 'RequestInterface':
        request = RequestFactory.create_standard_intuit_request(RequestType.ECHECK)
        request.set_method(RequestInterface.POST) \
            .set_url(context.get_base_url() + EndpointUrls.ECHECK_URL) \
            .set_header(context.get_standard_header_with_request_id(request_id)) \
            .set_body(OperationsConverter.get_json_from(debit_body))
        return request

    @staticmethod
    def retrieve_echeck(echeck_id: str, request_id: str, context) -> 'RequestInterface':
        request = RequestFactory.create_standard_intuit_request(RequestType.ECHECK)
        request.set_method(RequestInterface.GET) \
            .set_url(context.get_base_url() + EndpointUrls.ECHECK_URL + "/" + echeck_id) \
            .set_header(context.get_standard_header_with_request_id(request_id))
        return request

    @staticmethod
    def void_or_refund_echeck(echeck: ECheck, echeck_id: str, request_id: str, context) -> 'RequestInterface':
        request = RequestFactory.create_standard_intuit_request(RequestType.ECHECK)
        request.set_method(RequestInterface.POST) \
            .set_url(context.get_base_url() + EndpointUrls.ECHECK_URL + "/" + echeck_id + "/refunds") \
            .set_header(context.get_standard_header_with_request_id(request_id)) \
            .set_body(OperationsConverter.get_json_from(echeck))
        return request

    @staticmethod
    def retrieve_refund(echeck_id: str, refund_id: str, request_id: str, context) -> 'RequestInterface':
        request = RequestFactory.create_standard_intuit_request(RequestType.ECHECK)
        request.set_method(RequestInterface.GET) \
            .set_url(context.get_base_url() + EndpointUrls.ECHECK_URL + "/" + echeck_id + "/refunds/" + refund_id) \
            .set_header(context.get_standard_header_with_request_id(request_id))
        return request


"""
# Example context class for demonstration purposes
class Context:
    def get_base_url(self):
        return "https://example.com"

    def get_standard_header_with_request_id(self, request_id):
        return {"Request-ID": request_id}

# Example usage:
# echeck_data = {"amount": 100.0, "status": "completed"}
# echeck = ECheckOperations.build_from(echeck_data)
# context = Context()
# debit_request = ECheckOperations.debit(echeck, "req123", context)
# retrieve_request = ECheckOperations.retrieve_echeck("echeck123", "req123", context)
# void_request = ECheckOperations.void_or_refund_echeck(echeck, "echeck123", "req123", context)
# refund_request = ECheckOperations.retrieve_refund("echeck123", "refund123", "req123", context)
"""
