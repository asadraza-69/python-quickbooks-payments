from app.quickbookspayments.modules.charge import Charge
from app.quickbookspayments.modules.card import Card
from app.quickbookspayments.clientcontext import ClientContext
from app.quickbookspayments.httpclients.request.requestinterface import RequestInterface
from app.quickbookspayments.httpclients.response.responseinterface import ResponseInterface
from app.quickbookspayments.httpclients.core.clientfactory import ClientFactory
from app.quickbookspayments.operations.operationsconverter import OperationsConverter
from app.quickbookspayments.operations.chargeoperations import ChargeOperations
from app.quickbookspayments.operations.cardoperations import  CardOperations
from app.quickbookspayments.operations.bankaccountoperations import   BankAccountOperations
from app.quickbookspayments.resolver import InterceptorInterface
from typing import  Optional

class PaymentClient:
    def __init__(self, context: Optional[dict] = None):
        if context:
            self.context = ClientContext(context)
        else:
            self.context = ClientContext()
        self.http_client = ClientFactory.build_curl_client()
        self.interceptors: dict[InterceptorInterface] = {}

    """
    /**
     * A generic function to send any request that implements RequestInterface
     * @param RequestInterface $request The request to be sent
     * @param InterceptorInterface $interceptor for this request/response. Optional.
     */
    """

    def send(self, request: RequestInterface, interceptor: Optional[InterceptorInterface] = None) -> ResponseInterface:
        if interceptor:
            interceptor.before(request, self)
            response = self.http_client.send(request)
            interceptor.after(response, self)
            interceptor.intercept(request, response, self)
            OperationsConverter.update_response_body_to_obj(response)
            return response
        else:
            response = self.http_client.send(request)
            OperationsConverter.update_response_body_to_obj(response)
            return response

    def charge(self, charge: Charge, request_id: str = "") -> ResponseInterface:
        if not request_id:
            request_id = ClientContext.generate_request_id()
        request = ChargeOperations.create_charge_request(charge, request_id, self.get_context())
        response = self.http_client.send(request)
        self.before(request)
        response = self.http_client.send(request)
        self.after(response)
        OperationsConverter.update_response_body_to_obj(response)
        return response

    def void_charge_transaction(self, charge_request_id: str, request_id: str = "") -> ResponseInterface:
        if not request_id:
            request_id = ClientContext.generate_request_id()
        request = ChargeOperations.void_transaction(charge_request_id, request_id, self.get_context())
        self.http_client.send(request)
        self.before(request)
        response = self.http_client.send(request)
        self.after(response)
        OperationsConverter.update_response_body_to_obj(response)
        return response

    def retrieve_charge(self, charge_id: str, request_id: str = "") -> ResponseInterface:
        if not request_id:
            request_id = ClientContext.generate_request_id()
        request = ChargeOperations.create_get_charge_request(charge_id, request_id, self.get_context())
        self.before(request)
        response = self.http_client.send(request)
        self.after(response)
        self.intercept(request, response)
        OperationsConverter.update_response_body_to_obj(response)
        return response

    def capture_charge(self, charge: Charge, charge_id: str, request_id: str = "") -> ResponseInterface:
        if not request_id:
            request_id = ClientContext.generate_request_id()
        request = ChargeOperations.create_capture_charge_request(charge, charge_id, request_id, self.get_context())
        self.before(request)
        response = self.http_client.send(request)
        self.after(response)
        self.intercept(request, response)
        OperationsConverter.update_response_body_to_obj(response)
        return response

    def refund_charge(self, charge: Charge, charge_id: str, request_id: str = "") -> ResponseInterface:
        if not request_id:
            request_id = ClientContext.generate_request_id()
        request = ChargeOperations.create_refund_charge_request(charge, charge_id, request_id, self.get_context())
        self.before(request)
        response = self.http_client.send(request)
        self.after(response)
        self.intercept(request, response)
        OperationsConverter.update_response_body_to_obj(response)
        return response

    def get_refund_detail(self, charge_id: str, refund_id: str, request_id: str = "") -> ResponseInterface:
        if not request_id:
            request_id = ClientContext.generate_request_id()
        request = ChargeOperations.refund_by(charge_id, refund_id, request_id, self.get_context())
        self.before(request)
        response = self.http_client.send(request)
        self.after(response)
        self.intercept(request, response)
        OperationsConverter.update_response_body_to_obj(response)
        return response

    def create_card(self, card: Card, customer_id: str, request_id: str = "") -> ResponseInterface:
        if not request_id:
            request_id = ClientContext.generate_request_id()
        request = CardOperations.create_card(card, customer_id, request_id, self.get_context())
        self.before(request)
        response = self.http_client.send(request)
        self.after(response)
        self.intercept(request, response)
        OperationsConverter.update_response_body_to_obj(response)
        return response

    def get_card(self, customer_id: str, card_id: str, request_id: str = "") -> ResponseInterface:
        if not request_id:
            request_id = ClientContext.generate_request_id()
        request = CardOperations.get_card(customer_id, card_id, request_id, self.get_context())
        self.before(request)
        response = self.http_client.send(request)
        self.after(response)
        self.intercept(request, response)
        OperationsConverter.update_response_body_to_obj(response)
        return response

    def delete_card(self, customer_id: str, card_id: str, request_id: str = "") -> ResponseInterface:
        if not request_id:
            request_id = ClientContext.generate_request_id()
        request = CardOperations.delete_card(customer_id, card_id, request_id, self.get_context())
        self.before(request)
        response = self.http_client.send(request)
        self.after(response)
        self.intercept(request, response)
        OperationsConverter.update_response_body_to_obj(response)
        return response

    def get_all_cards_for(self, customer_id: str, request_id: str = "") -> ResponseInterface:
        if not request_id:
            request_id = ClientContext.generate_request_id()
        request = CardOperations.get_all_cards(customer_id, request_id, self.get_context())
        self.before(request)
        response = self.http_client.send(request)
        self.after(response)
        self.intercept(request, response)
        OperationsConverter.update_response_body_to_obj(response)
        return response

    def create_card_from_token(self, customer_id: str, token_value: str, request_id: str = "") -> ResponseInterface:
        if not request_id:
            request_id = ClientContext.generate_request_id()
        request = CardOperations.create_card_from_token(customer_id, token_value, request_id, self.get_context())
        self.before(request)
        response = self.http_client.send(request)
        self.after(response)
        self.intercept(request, response)
        OperationsConverter.update_response_body_to_obj(response)
        return response

    def before(self, request):
        pass

    def after(self, response):
        pass

    def intercept(self, request, response):
        pass

    def get_context(self):
        return self.context

    def delete_bank_account(self, customer_id: str, bank_account_id: str, request_id: str = "") -> ResponseInterface:
        if not request_id:
            request_id = ClientContext.generate_request_id()
        request = BankAccountOperations.delete_bank_account(customer_id, bank_account_id, request_id,
                                                            self.get_context())
        self.before(request, self)
        response = self.http_client.send(request)
        self.after(response, self)
        self.intercept(request, response)
        OperationsConverter.update_response_body_to_obj(response)
        return response

    def get_all_bank_account(self, customer_id: str, request_id: str = "") -> ResponseInterface:
        if not request_id:
            request_id = ClientContext.generate_request_id()
        request = BankAccountOperations.get_all_bank_accounts_for(customer_id, request_id, self.get_context())
        self.before(request, self)
        response = self.http_client.send(request)
        self.after(response, self)
        self.intercept(request, response)
        OperationsConverter.update_response_body_to_obj(response)
        return response

    def get_bank_account(self, customer_id: str, bank_account_id: str, request_id: str = "") -> ResponseInterface:
        if not request_id:
            request_id = ClientContext.generate_request_id()
        request = BankAccountOperations.get_bank_account_for(customer_id, bank_account_id, request_id,
                                                             self.get_context())
        self.before(request, self)
        response = self.http_client.send(request)
        self.after(response, self)
        self.intercept(request, response)
        OperationsConverter.update_response_body_to_obj(response)
        return response

    def intercept(self, request: RequestInterface, response: ResponseInterface) -> None:
        for interceptor in self.interceptors:
            interceptor.intercept(request, response, self)

    def before(self, request: RequestInterface, client: 'PaymentClient') -> None:
        for interceptor in self.interceptors:
            interceptor.before(request, client)

    def after(self, response: ResponseInterface, client: 'PaymentClient') -> None:
        for interceptor in self.interceptors:
            interceptor.after(response, client)

    def get_url(self) -> str:
        return self.context.get_base_url()

    def set_url(self, url: str) -> 'PaymentClient':
        if not url:
            raise RuntimeError("Set empty base url for Payments API.")
        self.context.set_base_url(url)
        return self

    def get_access_token(self):
        return self.context.get_access_token()

    def set_access_token(self, access_token) -> 'PaymentClient':
        self.context.set_access_token(access_token)
        return self

    def get_refresh_token(self):
        return self.context.get_refresh_token()

    def set_refresh_token(self, refresh_token) -> 'PaymentClient':
        self.context.set_refresh_token(refresh_token)
        return self

    def set_environment(self, environment) -> None:
        self.context.set_environment(environment)

    def get_all_interceptors(self) -> list:
        return self.interceptors

    def get_interceptor(self, interceptor_name: str):
        return self.interceptors.get(interceptor_name)

    def add_interceptor(self, name: str, interceptor: InterceptorInterface) -> 'PaymentClient':
        if name in self.interceptors:
            raise RuntimeError(f"Interceptor with name: {name} already exists.")
        self.interceptors[name] = interceptor
        return self

    def remove_interceptor(self, name: str) -> None:
        if name in self.interceptors:
            del self.interceptors[name]
        else:
            raise RuntimeError(f"Interceptor with name: {name} cannot be deleted. It does not exist.")

    def get_oauth2_authenticator(self):
        return self.oauth2_authenticator

    def set_oauth2_authenticator(self, oauth2_authenticator):
        self.oauth2_authenticator = oauth2_authenticator
        return self

    def get_http_client(self):
        return self.http_client

    def set_http_client(self, http_client):
        self.http_client = http_client
        return self

    def get_context(self):
        return self.context

    def set_context(self, context: ClientContext):
        self.context = context
        return self
