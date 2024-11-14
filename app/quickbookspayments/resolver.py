from app.quickbookspayments.modules.token import Token
from app.quickbookspayments.interceptors.interceptorinterface import InterceptorInterface


def get_payment_client():
    from app.quickbookspayments.paymentclient import PaymentClient
    return PaymentClient