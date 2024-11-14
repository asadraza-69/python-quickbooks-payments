from app.quickbookspayments.httpclients.request.intuitrequest import IntuitRequest
class RequestFactory:
    @staticmethod
    def create_standard_intuit_request(request_type):
        return IntuitRequest(request_type)
