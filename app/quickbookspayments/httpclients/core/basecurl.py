import requests


class BaseCurl:
    def __init__(self):
        self.session = requests.Session()
        self.response = None

    def execute(self, request):
        method = request.get_method().upper()
        if method == "POST":
            self.response = self.session.post(request.get_url(), headers=request.get_header(), data=request.get_body())
        else:
            self.response = self.session.request(method, request.get_url(), headers=request.get_header())

        return self.response

    def getInfo(self, info_type):
        if info_type == 'header_size':
            return len(self.response.headers)
        elif info_type == 'http_code':
            return self.response.status_code
        return None

    def close(self):
        self.session.close()

    def errno(self):
        return self.response.status_code >= 400

    def error(self):
        return self.response.reason if self.response.status_code >= 400 else ""

    def getCurl(self):
        return self.session
