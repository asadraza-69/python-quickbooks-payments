import os

"""Constants whose values do not change."""


class CoreConstants:
    INTUIT_TID = "intuit_tid"
    CONTENT_TYPE = "Content-Type"

    @staticmethod
    def get_cert_path():
        # Returns the path to the PEM certification key
        return os.path.join(os.path.dirname(__file__), "certs", "cacert.pem")
