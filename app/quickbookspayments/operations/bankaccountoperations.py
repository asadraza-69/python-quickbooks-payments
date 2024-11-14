from app.quickbookspayments.httpclients.request.requestinterface import RequestInterface
from app.quickbookspayments.httpclients.request.requestfactory import RequestFactory
from app.quickbookspayments.httpclients.request.requesttype import RequestType
from app.quickbookspayments.modules.bankaccount import BankAccount
from app.quickbookspayments.modules.token import  Token



class BankAccountOperations:
    @staticmethod
    def build_from(data):
        return BankAccount(data)

    @staticmethod
    def create_bank_account(bankaccount:BankAccount, customer_id:str, request_id:str, context) -> 'RequestInterface':
        request = RequestFactory.create_standard_intuit_request(RequestType.BANKACCOUNT)
        request.set_method(RequestInterface.POST) \
            .set_url(context.get_base_url() + EndpointUrls.CUSTOMER_URL + "/" + customer_id + "/bank-accounts") \
            .set_header(context.get_standard_header_with_request_id(request_id)) \
            .set_body(OperationsConverter.get_json_from(bankaccount))
        return request

    @staticmethod
    def create_bank_account_from_token(customer_id:str, token_value:str, request_id:str, context) -> 'RequestInterface':
        token = OperationsConverter.create_token_obj_from_value(token_value)
        request = RequestFactory.create_standard_intuit_request(RequestType.BANKACCOUNT)
        request.set_method(RequestInterface.POST) \
            .set_url(
            context.get_base_url() + EndpointUrls.CUSTOMER_URL + "/" + customer_id + "/bank-accounts/createFromToken") \
            .set_header(context.get_standard_header_with_request_id(request_id)) \
            .set_body(OperationsConverter.get_json_from(token))
        return request

    @staticmethod
    def delete_bank_account(customer_id:str, bank_account_id:str, request_id:str, context) -> 'RequestInterface':
        request = RequestFactory.create_standard_intuit_request(RequestType.BANKACCOUNT)
        request.set_method(RequestInterface.DELETE) \
            .set_url(
            context.get_base_url() + EndpointUrls.CUSTOMER_URL + "/" + customer_id + "/bank-accounts/" + bank_account_id) \
            .set_header(context.get_standard_header_with_request_id_for_delete(request_id))
        return request

    @staticmethod
    def get_all_bank_accounts_for(customer_id:str, request_id:str, context) -> 'RequestInterface':
        request = RequestFactory.create_standard_intuit_request(RequestType.BANKACCOUNT)
        request.set_method(RequestInterface.GET) \
            .set_url(context.get_base_url() + EndpointUrls.CUSTOMER_URL + "/" + customer_id + "/bank-accounts") \
            .set_header(context.get_standard_header_with_request_id(request_id))
        return request

    @staticmethod
    def get_bank_account_for(customer_id:str, bank_account_id:str, request_id, context) -> 'RequestInterface':
        request = RequestFactory.create_standard_intuit_request(RequestType.BANKACCOUNT)
        request.set_method(RequestInterface.GET) \
            .set_url(
            context.get_base_url() + EndpointUrls.CUSTOMER_URL + "/" + customer_id + "/bank-accounts/" + bank_account_id) \
            .set_header(context.get_standard_header_with_request_id(request_id))
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
# bankaccount_data = {"account_number": "123456789", "routing_number": "987654321"}
# bankaccount = BankAccountOperations.build_from(bankaccount_data)
# context = Context()
# create_request = BankAccountOperations.create_bank_account(bankaccount, "cust123", "req123", context)
# delete_request = BankAccountOperations.delete_bank_account("cust123", "bank123", "req123", context)
# get_all_request = BankAccountOperations.get_all_bank_accounts_for("cust123", "req123", context)
# get_bank_request = BankAccountOperations.get_bank_account_for("cust123", "bank123", "req123", context)
# create_token_request = BankAccountOperations.create_bank_account_from_token("cust123", "tokenValue123", "req123", context)
"""