import os
import unittest
from random import randint

from app.quickbookspayments.interceptors.requestresponseloggerinterceptor import RequestResponseLoggerInterceptor
from app.quickbookspayments.interceptors.stacktraceloggerinterceptor import StackTraceLoggerInterceptor
from app.quickbookspayments.operations.cardoperations import CardOperations
from app.test.testclientcreator import TestClientCreator


class LoggingInterceptorTest(unittest.TestCase):
    test_dir = "/tmp/logTest"

    def create_instance(self):
        return TestClientCreator.create_instance()

    def create_card_body(self):
        card_body = CardOperations.build_from({
            "expMonth": "12",
            "address": {
                "postalCode": "44112",
                "city": "Richmond",
                "streetAddress": "1245 Hana Rd",
                "region": "VA",
                "country": "US"
            },
            "number": "4131979708684369",
            "name": "Test User",
            "expYear": "2026"
        })
        return card_body

    def setUp(self):
        self.test_dir = self.test_dir + '_' + str(randint(1, 99999999)).zfill(8)
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir, 0o755)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            for file in os.listdir(self.test_dir):
                file_path = os.path.join(self.test_dir, file)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            os.rmdir(self.test_dir)

    def test_logging_to_disk_works_or_not(self):
        client = self.create_instance()
        client.add_interceptor("FileInterceptor",
                               RequestResponseLoggerInterceptor(self.test_dir + '/', 'America/Los_Angeles'))
        # client.add_interceptor("LoggerInterceptor", StackTraceLoggerInterceptor(self.test_dir + '/errorLog.txt'))
        card = self.create_card_body()
        client_id = randint(0, 10000)
        response = client.create_card(card, client_id, str(randint(0, 10000)) + "abd")
        exist = os.path.exists(self.test_dir + '/errorLog.txt')
        self.assertTrue(exist)

    # def test_can_change_request_and_response(self):
    #     charge_body = ChargeOperations.build_from({
    #         "amount": "10.55",
    #         "currency": "USD",
    #         "capture": False,
    #         "card": {
    #             "name": "emulate=0",
    #             "number": "4111111111111111",
    #             "address": {
    #                 "streetAddress": "1130 Kifer Rd",
    #                 "city": "Sunnyvale",
    #                 "region": "CA",
    #                 "country": "US",
    #                 "postalCode": "94086"
    #             },
    #             "expMonth": "02",
    #             "expYear": "2020",
    #             "cvc": "123"
    #         },
    #         "context": {
    #             "mobile": "false",
    #             "isEcommerce": "true"
    #         }
    #     })
    #
    #     client = self.create_instance()
    #     request = ChargeOperations.create_charge_request(charge_body, "sfas" + str(randint(0, 10000)), client.get_context())
    #     exception_on_error_interceptor = ExceptionOnErrorInterceptor()
    #     client.send(request, exception_on_error_interceptor)
    #     self.assertTrue(exist)


if __name__ == '__main__':
    unittest.main()
