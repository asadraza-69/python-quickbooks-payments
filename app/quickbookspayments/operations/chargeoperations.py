from app.quickbookspayments.httpclients.request.requestinterface import RequestInterface
from app.quickbookspayments.httpclients.request.requestfactory import RequestFactory
from app.quickbookspayments.httpclients.request.requesttype import RequestType
from app.quickbookspayments.modules.charge import Charge


class ChargeOperations:
    @staticmethod
    def build_from(data):
        return Charge(data)

    @staticmethod
    def create_charge_request(charge: Charge, request_id: str, context) -> 'RequestInterface':
        request = RequestFactory.create_standard_intuit_request(RequestType.CHARGE)
        request.set_method(RequestInterface.POST) \
            .set_url(context.get_base_url() + EndpointUrls.CHARGE_URL) \
            .set_header(context.get_standard_header_with_request_id(request_id)) \
            .set_body(OperationsConverter.get_json_from(charge))
        return request

    @staticmethod
    def create_get_charge_request(charge_id: str, request_id: str, context) -> 'RequestInterface':
        request = RequestFactory.create_standard_intuit_request(RequestType.CHARGE)
        request.set_method(RequestInterface.GET) \
            .set_url(context.get_base_url() + EndpointUrls.CHARGE_URL + "/" + charge_id) \
            .set_header(context.get_standard_header_with_request_id(request_id))
        return request

    @staticmethod
    def create_capture_charge_request(charge: Charge, charge_id: str, request_id: str, context) -> 'RequestInterface':
        request = RequestFactory.create_standard_intuit_request(RequestType.CHARGE)
        request.set_method(RequestInterface.POST) \
            .set_url(context.get_base_url() + EndpointUrls.CHARGE_URL + "/" + charge_id + "/capture") \
            .set_header(context.get_standard_header_with_request_id(request_id)) \
            .set_body(OperationsConverter.get_json_from(charge))
        return request

    @staticmethod
    def create_refund_charge_request(charge: Charge, charge_id: str, request_id: str, context) -> 'RequestInterface':
        request = RequestFactory.create_standard_intuit_request(RequestType.CHARGE)
        request.set_method(RequestInterface.POST) \
            .set_url(context.get_base_url() + EndpointUrls.CHARGE_URL + "/" + charge_id + "/refunds") \
            .set_header(context.get_standard_header_with_request_id(request_id)) \
            .set_body(OperationsConverter.get_json_from(charge))
        return request

    @staticmethod
    def refund_by(charge_id: str, refund_id: str, request_id: str, context) -> 'RequestInterface':
        request = RequestFactory.create_standard_intuit_request(RequestType.CHARGE)
        request.set_method(RequestInterface.GET) \
            .set_url(context.get_base_url() + EndpointUrls.CHARGE_URL + "/" + charge_id + "/refunds/" + refund_id) \
            .set_header(context.get_standard_header_with_request_id(request_id))
        return request

    @staticmethod
    def void_transaction(charge_request_id: str, request_id: str, context) -> 'RequestInterface':
        request = RequestFactory.create_standard_intuit_request(RequestType.CHARGE)
        request.set_method(RequestInterface.POST) \
            .set_url(context.get_base_url() + EndpointUrls.VOID_URL + "/" + charge_request_id + "/void") \
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
# charge_data = {"amount": 100.0, "currency": "USD"}
# charge = ChargeOperations.build_from(charge_data)
# context = Context()
# create_request = ChargeOperations.create_charge_request(charge, "req123", context)
# retrieve_request = ChargeOperations.create_get_charge_request("charge123", "req123", context)
# capture_request = ChargeOperations.create_capture_charge_request(charge, "charge123", "req123", context)

"""
