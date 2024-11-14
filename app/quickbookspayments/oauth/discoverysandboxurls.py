from .discoveryurls import DiscoveryURLs
class DiscoverySandboxURLs(DiscoveryURLs):
    def __init__(self):
        super().__init__()
        self.set_userinfo_endpoint_url("https://sandbox-accounts.platform.intuit.com/v1/openid_connect/userinfo")
        self.set_migration_endpoint_url("https://developer-sandbox.api.intuit.com/v2/oauth2/tokens/migrate")
