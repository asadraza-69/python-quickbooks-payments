import time
import hmac
import base64
import hashlib
import urllib.parse
from random import randint


class OAuth1Encrypter:
    """
    OAuth1Encrypter handles the OAuth 1.0 encryption process.
    """

    SIGNATURE_METHOD = 'sha1'
    NONCE_CHARS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

    def __init__(self, ck, cs, ot, ots):
        """
        The Constructor for OAuth 1.

        :param ck: Consumer key
        :param cs: Consumer Secret
        :param ot: OAuth Access Token
        :param ots: OAuth Access Token Secret
        """
        if ck:
            self.consumer_key = ck
        else:
            raise ValueError("Consumer key is not passed.")

        if cs:
            self.consumer_secret = cs
        else:
            raise ValueError("Consumer Secret is not passed.")

        if ot:
            self.oauth_token = ot
        else:
            raise ValueError("OAuth Token is not passed.")

        if ots:
            self.oauth_token_secret = ots
        else:
            raise ValueError("OAuth token Secret is not passed.")

        self.set_nonce()
        self.set_oauth_timestamp()
        self.oauth_parameters = self.append_oauth_parts_to(None)

    def get_oauth_header(self, uri, query_parameters, http_method):
        """
        Return the completed signed Authorization Header.

        :param uri: The complete URL contains everything
        :param query_parameters: The QueryParameters for the request
        :param http_method: The HTTP Method. POST or GET
        :return: Authorization Header
        """
        self.sign(uri, query_parameters, http_method)
        oauth_params = {k: '{}="{}"'.format(k, urllib.parse.quote(v)) for k, v in self.oauth_parameters.items()}
        return 'OAuth ' + ', '.join(oauth_params.values())

    def sign(self, uri, query_parameters, http_method):
        """
        Sign the Request based on the URL, OAuth 1 values, and query parameters.

        :param uri: The Complete URL contains everything
        :param query_parameters: The query parameters for the array
        :param http_method: The HTTP Method. POST or GET
        """
        base_string = self.get_base_string(uri, http_method, query_parameters)
        oauth_signature = self.sign_using_hmac_sha1(base_string)
        self.oauth_parameters['oauth_signature'] = oauth_signature

    def get_base_string(self, uri, method, parameters=None):
        """
        Prepare the base String for OAuth 1 to sign.

        :param uri: The Complete URL contains everything
        :param method: The HTTP Method. POST or GET
        :param parameters: The query parameters for the array
        :return: The baseString for sign
        """
        if parameters is None:
            parameters = {}
        return '&'.join([
            self.prepare_http_method(method),
            self.prepare_url(uri),
            self.prepare_query_params(parameters)
        ])

    def prepare_http_method(self, method):
        """
        Helper method to format the HTTP method.

        :param method: The Post or Get
        :return: The formatted HTTP method
        """
        return urllib.parse.quote(method.strip().upper())

    def prepare_url(self, url):
        """
        Helper method to format the URL.

        :param url: The URL to be formatted
        :return: The formatted URL String
        """
        return urllib.parse.quote(url.strip())

    def prepare_query_params(self, query_parameters):
        """
        A helper method to decide which query parameters to be included.

        :param query_parameters: The QueryParameters Array for format and re-order
        :return: The formatted string
        """
        query_parameters = self.append_oauth_parts_to(query_parameters or {})

        encoded_params = {urllib.parse.quote(k): urllib.parse.quote(v) for k, v in query_parameters.items()}
        sorted_params = sorted(encoded_params.items())
        encoded_string = urllib.parse.quote('&'.join(f"{k}={v}" for k, v in sorted_params))
        return encoded_string

    def sign_using_hmac_sha1(self, base_string):
        """
        Sign the baseString with HMAC-SHA1.

        :param base_string: The baseString to be signed
        :return: Signed String
        """
        key = f"{urllib.parse.quote(self.consumer_secret)}&{urllib.parse.quote(self.oauth_token_secret)}"
        hashed = hmac.new(key.encode(), base_string.encode(), hashlib.sha1)
        return base64.b64encode(hashed.digest()).decode()

    def set_nonce(self, length=6):
        """
        Set a random nonce for the signature.

        :param length: the length of the length
        """
        self.oauth_nonce = ''.join(self.NONCE_CHARS[randint(0, len(self.NONCE_CHARS) - 1)] for _ in range(length))

    def set_oauth_timestamp(self):
        """
        Set a random timestamp for the signature.
        """
        self.oauth_timestamp = str(int(time.time()))

    def append_oauth_parts_to(self, query_parameters=None):
        """
        Add all OAuth query parameters to the signature string.

        :param query_parameters: The queryParameters to be included
        :return: The complete query parameters
        """
        if query_parameters is None:
            query_parameters = {}
        query_parameters.update({
            'oauth_consumer_key': self.consumer_key,
            'oauth_token': self.oauth_token,
            'oauth_signature_method': 'HMAC-SHA1',
            'oauth_timestamp': self.oauth_timestamp,
            'oauth_nonce': self.oauth_nonce,
            'oauth_version': '1.0'
        })
        return query_parameters

    def set_nonce_for_test(self, nonce):
        """
        Set nonce for testing.

        :param nonce: The nonce value to be set
        """
        self.oauth_nonce = nonce

    def set_time_for_test(self, time):
        """
        Set time for testing.

        :param time: The timestamp value to be set
        """
        self.oauth_timestamp = time
