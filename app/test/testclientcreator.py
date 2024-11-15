import unittest

from app.quickbookspayments.paymentclient import PaymentClient


class TestClientCreator:
    @staticmethod
    def create_instance() -> PaymentClient:
        # Create an instance of PaymentClient
        client = PaymentClient()

        # Set the access token for the client
        client.set_access_token(
            "eyJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwiYWxnIjoiZGlyIn0..rAG5JBcE4RZX5vIRl3PhKA.W65HsM-PU46DOicpJS4anVrKC8OUlbGSwrUV-bktVKong-1suLWnTL-FpjuoowR9xP8vGQ5hN6gYElYz1KEJRsMa0Hb1ieczORo1SGRwOLJA5Ka2MYXRX-P5ZreAMzC_K_9FWXk2vx_9QQJAClNebbLTIDpjbdSOJ5GiKfqs7ixgF8MkRpekGucFcf0a7hJmoHY85adW3C0vL5BUiJ5gvMQCQasqZ-8EGsMr9LJxfHGGTI5CN5mmTyZmQS-KV3y6lfNLVvjvbeDk1qmtzEKw1Z0QAec8YgECylvITlsIL9cV8LPZCEkNavVLc6MHRl5vpF3hTkfk4rTS1dGB2TFEFgGLbWHGEYmdyou_T2JcNGXtv_rhPaishDV7LZG2V3GJ0bGPsH9rc6bqwb1ZRDKYgAB3lNRl_W-GenbvqKiNLsvvnMjYgSBRxKNwP-aVFHQPfY_cCWJP9HiTqvMsxWa2g59krAXobowbaJupCvVlNxfiYaqzXYVFFMlcVtqaYDthYg66pVtwzKIMroE4QfL_kRjdCMM0Xx5HyKh1EXFboY3ZohpJcc7pIZ6_rQea1rnBGXHoFQxxxLsgUim2dF9daxzf7-Gm7VrT4l8wG2pnVcYAFfh4SkB7mi8RYj1IzLv7n1iLI4dHOrSkIjM42wYDOgmiA_bgoY1ZAtLMla6MnQi0cEYrbIZSD_1b6qcuYCMboqJaBgqJg1u3YSaG7nrDsV_szKg6Nr1kRwGKUlgryuw.wBxn4TG7QRthUeudsrNGTA"
        ).set_environment("sandbox")
        return client


if __name__ == "__main__":
    unittest.main()
