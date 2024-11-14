from app.quickbookspayments.httpclients.request.requestinterface import RequestInterface
from app.quickbookspayments.httpclients.request.requestfactory import RequestFactory
from app.quickbookspayments.httpclients.request.requesttype import RequestType
from app.quickbookspayments.modules.card import Card


class CardOperations:
    @staticmethod
    def build_from(data):
        return Card(data)

    @staticmethod
    def create_card(card: Card, customer_id: str, request_id: str, context) -> 'RequestInterface':
        request = RequestFactory.create_standard_intuit_request(RequestType.CARD)
        request.set_method(RequestInterface.POST) \
            .set_url(context.get_base_url() + EndpointUrls.CUSTOMER_URL + "/" + customer_id + "/cards") \
            .set_header(context.get_standard_header_with_request_id(request_id)) \
            .set_body(OperationsConverter.get_json_from(card))
        return request

    @staticmethod
    def delete_card(customer_id: str, card_id: str, request_id: str, context) -> 'RequestInterface':
        request = RequestFactory.create_standard_intuit_request(RequestType.CARD)
        request.set_method(RequestInterface.DELETE) \
            .set_url(context.get_base_url() + EndpointUrls.CUSTOMER_URL + "/" + customer_id + "/cards/" + card_id) \
            .set_header(context.get_standard_header_with_request_id_for_delete(request_id))
        return request

    @staticmethod
    def get_all_cards(customer_id: str, request_id: str, context) -> 'RequestInterface':
        request = RequestFactory.create_standard_intuit_request(RequestType.CARD)
        request.set_method(RequestInterface.GET) \
            .set_url(context.get_base_url() + EndpointUrls.CUSTOMER_URL + "/" + customer_id + "/cards") \
            .set_header(context.get_standard_header_with_request_id(request_id))
        return request

    @staticmethod
    def get_card(customer_id: str, card_id: str, request_id: str, context) -> 'RequestInterface':
        request = RequestFactory.create_standard_intuit_request(RequestType.CARD)
        request.set_method(RequestInterface.GET) \
            .set_url(context.get_base_url() + EndpointUrls.CUSTOMER_URL + "/" + customer_id + "/cards/" + card_id) \
            .set_header(context.get_standard_header_with_request_id(request_id))
        return request

    @staticmethod
    def create_card_from_token(customer_id: str, token_value: str, request_id: str, context) -> 'RequestInterface':
        token = OperationsConverter.create_token_obj_from_value(token_value)
        request = RequestFactory.create_standard_intuit_request(RequestType.CARD)
        request.set_method(RequestInterface.POST) \
            .set_url(context.get_base_url() + EndpointUrls.CUSTOMER_URL + "/" + customer_id + "/cards/createFromToken") \
            .set_header(context.get_standard_header_with_request_id(request_id)) \
            .set_body(OperationsConverter.get_json_from(token))
        return request


"""
# Example context class for demonstration purposes
class Context:
    def get_base_url(self):
        return "https://example.com"

    def get_standard_header_with_request_id(self, request_id):
        return {"Request-ID": request_id}

    def get_standard_header_with_request_id_for_delete(self, request_id):
        return {"Request-ID": request_id}

# Example usage:
# card_data = {"number": "4111111111111111", "exp_month": 12, "exp_year": 2025}
# card = CardOperations.build_from(card_data)
# context = Context()
# create_request = CardOperations.create_card(card, "cust123", "req123", context)
# delete_request = CardOperations.delete_card("cust123", "card123", "req123", context)
# get_all_request = CardOperations.get_all_cards("cust123", "req123", context)
# get_card_request = CardOperations.get_card("cust123", "card123", "req123", context)
# create_token_request = CardOperations.create_card_from_token("cust123", "tokenValue123", "req123", context)
"""
