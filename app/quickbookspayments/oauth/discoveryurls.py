class DiscoveryURLs:
    __issuer_url = None
    __authorization_endpoint_url = None
    __token_endpoint_url = None
    __userinfo_endpoint_url = None
    __revocation_endpoint_url = None
    __migration_endpoint_url = None
    def __init__(self):
        self.set_issuer_url("https://oauth.platform.intuit.com/op/v1")
        self.set_authorization_endpoint_url("https://appcenter.intuit.com/connect/oauth2")
        self.set_token_endpoint_url("https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer")
        self.set_userinfo_endpoint_url("https://accounts.platform.intuit.com/v1/openid_connect/userinfo")
        self.set_revocation_endpoint_url("https://developer.api.intuit.com/v2/oauth2/tokens/revoke")
        self.set_migration_endpoint_url("https://developer.api.intuit.com/v2/oauth2/tokens/migrate")

    def get_issuer_url(self):
        return self.__issuer_url

    def set_issuer_url(self, issuer_url):
        self.__issuer_url = issuer_url
        return self

    def get_authorization_endpoint_url(self):
        return self.__authorization_endpoint_url

    def set_authorization_endpoint_url(self, authorization_endpoint_url):
        self.__authorization_endpoint_url = authorization_endpoint_url
        return self

    def get_token_endpoint_url(self):
        return self.__token_endpoint_url

    def set_token_endpoint_url(self, token_endpoint_url):
        self.__token_endpoint_url = token_endpoint_url
        return self

    def get_userinfo_endpoint_url(self):
        return self.__userinfo_endpoint_url

    def set_userinfo_endpoint_url(self, userinfo_endpoint_url):
        self.__userinfo_endpoint_url = userinfo_endpoint_url
        return self

    def get_revocation_endpoint_url(self):
        return self.__revocation_endpoint_url

    def set_revocation_endpoint_url(self, revocation_endpoint_url):
        self.__revocation_endpoint_url = revocation_endpoint_url
        return self

    def get_migration_endpoint_url(self):
        return self.__migration_endpoint_url

    def set_migration_endpoint_url(self, migration_endpoint_url):
        self.__migration_endpoint_url = migration_endpoint_url
        return self
