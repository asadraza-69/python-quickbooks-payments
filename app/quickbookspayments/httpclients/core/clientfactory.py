from app.quickbookspayments.httpclients.core.guzzleclient import GuzzleClient
from app.quickbookspayments.httpclients.core.httpcurlclient import HttpCurlClient


class ClientFactory:
    @staticmethod
    def build_curl_client(connection_time_out=10, request_time_out=100, is_verify=False):
        client = HttpCurlClient()
        client.set_verify_ssl(is_verify)
        client.set_timeout(connection_time_out, request_time_out)
        return client

    @staticmethod
    def build_guzzle_client(connection_time_out=10, request_time_out=100, is_verify=False):
        client = GuzzleClient()
        client.set_verify_ssl(is_verify)
        client.set_timeout(connection_time_out, request_time_out)
        return client
