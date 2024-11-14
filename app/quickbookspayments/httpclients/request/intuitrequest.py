from app.quickbookspayments.httpclients.request.requestinterface import RequestInterface
class IntuitRequest(RequestInterface):
    def __init__(self, type):
        self.method = None
        self.url = None
        self.header = None
        self.body = None
        self.requestType = None
        self.requestId = None
        self.setRequestType(type)

    def setMethod(self, method):
        self.method = method
        return self

    def getMethod(self):
        return self.method

    def getUrl(self):
        return self.url

    def setUrl(self, url):
        if not url:
            raise ValueError("invalid URL.")
        else:
            self.url = url
        return self

    def getHeader(self):
        return self.header

    def setHeader(self, header):
        if header and isinstance(header, dict):
            self.header = header
            self.addRequestIdFromHeader(header)
        else:
            raise ValueError("invalid header for request")
        return self

    def addRequestIdFromHeader(self, header):
        if (self.getRequestType() != RequestType.OAUTH and
            self.getRequestType() != RequestType.USERINFO):
            self.setRequestId(header['Request-Id'])

    def getBody(self):
        return self.body

    def setBody(self, body):
        if self.getMethod() != RequestInterface.POST:
            raise ValueError("Cannot Set body for GET request")
        self.body = body
        return self

    def getRequestType(self):
        return self.requestType

    def setRequestType(self, type):
        self.requestType = type

    def setRequestId(self, requestId):
        self.requestId = requestId

    def getRequestId(self):
        return self.requestId

