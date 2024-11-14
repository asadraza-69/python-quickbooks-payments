from app.quickbookspayments.operations.endpointurls import EndpointUrls
from app.quickbookspayments.operations.operationsconverter import OperationsConverter
from app.quickbookspayments.httpclients.request.requestinterface import RequestInterface
from app.quickbookspayments.httpclients.request.requestfactory import RequestFactory
from app.quickbookspayments.httpclients.request.requesttype import RequestType
from app.quickbookspayments.modules.card import Card
from app.quickbookspayments.modules.bankaccount import BankAccount


class TokenOperations:
    @staticmethod
    def create_token(token_body, is_ie:bool, request_id:str, context) -> 'RequestInterface':
        request = RequestFactory.create_standard_intuit_request(RequestType.TOKEN)
        request_body = {}
        if isinstance(token_body, Card):
            request_body['card'] = token_body
        elif isinstance(token_body, BankAccount):
            request_body['bankAccount'] = token_body
        url = context.get_base_url() + (EndpointUrls.TOKEN_URL_IE if is_ie else EndpointUrls.TOKEN_URL)
        request.set_method(RequestInterface.POST) \
            .set_url(url) \
            .set_header(context.get_non_auth_header_with_request_id(request_id)) \
            .set_body(OperationsConverter.get_json_from(request_body))
        return request


"""
# Example context class for demonstration purposes
class Context:
    def get_base_url(self):
        return "https://example.com"

    def get_non_auth_header_with_request_id(self, request_id):
        return {"Request-ID": request_id}

# Example usage:
# card = Card()
# context = Context()
# request = TokenOperations.create_token(card, is_ie=True, request_id="12345", context=context)

"""