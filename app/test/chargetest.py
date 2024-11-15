import unittest
from random import randint

from app.quickbookspayments.operations.chargeoperations import ChargeOperations
from app.test.testclientcreator import TestClientCreator


class ChargeTest(unittest.TestCase):

    def create_instance(self):
        return TestClientCreator.create_instance()

    def create_charge_body(self):
        charge_body = ChargeOperations.build_from({
            "amount": "10.55",
            "currency": "USD",
            "capture": False,
            "card": {
                "name": "emulate=0",
                "number": "4111111111111111",
                "address": {
                    "streetAddress": "1130 Kifer Rd",
                    "city": "Sunnyvale",
                    "region": "CA",
                    "country": "US",
                    "postalCode": "94086"
                },
                "expMonth": "02",
                "expYear": "2020",
                "cvc": "123"
            },
            "context": {
                "mobile": "false",
                "isEcommerce": "true"
            }
        })
        return charge_body

    def create_charge_body_with_capture(self):
        charge_body = ChargeOperations.build_from({
            "amount": "10.55",
            "currency": "USD",
            "card": {
                "name": "emulate=0",
                "number": "4111111111111111",
                "address": {
                    "streetAddress": "1130 Kifer Rd",
                    "city": "Sunnyvale",
                    "region": "CA",
                    "country": "US",
                    "postalCode": "94086"
                },
                "expMonth": "02",
                "expYear": "2020",
                "cvc": "123"
            },
            "context": {
                "mobile": "false",
                "isEcommerce": "true"
            }
        })
        return charge_body

    def create_refund_body(self):
        refund_body = ChargeOperations.build_from({
            "amount": "10.55",
            "description": "first refund",
            "id": "E5753FS0CL2F"
        })
        return refund_body

    def create_capture_body(self):
        capture_body = ChargeOperations.build_from({
            "amount": "10.55",
            "context": {
                "mobile": "false",
                "isEcommerce": "true"
            }
        })
        return capture_body

    def test_request_id(self):
        client = self.create_instance()
        charge_body = self.create_charge_body()
        request_id = str(randint(0, 10000)) + "abd"
        response = client.charge(charge_body, request_id)
        self.assertEqual(
            response.get_associated_request().get_header()['Request-Id'],
            request_id
        )

        response = client.charge(charge_body)
        self.assertEqual(
            len(response.get_associated_request().get_header()['Request-Id']),
            20
        )

    def test_create_charge_request_on_sandbox(self):
        client = self.create_instance()
        charge_body = self.create_charge_body()
        response = client.charge(charge_body, str(randint(0, 10000)) + "abd")
        charge_response = response.get_body()
        self.assertEqual(charge_response.amount, charge_body.amount)
        self.assertEqual(charge_response.card.address.streetAddress, charge_body.card.address.streetAddress)

    def test_get_charge(self):
        client = self.create_instance()
        charge_body = self.create_charge_body()
        response = client.charge(charge_body, str(randint(0, 10000)) + "abd")
        charge_response = response.get_body()
        charge_id = charge_response.id

        client.get_http_client().enable_debug()
        response = client.retrieve_charge(charge_id, str(randint(0, 10000)) + "abd")
        information = client.get_http_client().get_debug_info()
        self.assertEqual(charge_response.id, charge_id)

    def test_refund_charge(self):
        client = self.create_instance()
        charge_body = self.create_charge_body()
        response = client.charge(charge_body, str(randint(0, 10000)) + "abd")
        charge_response = response.get_body()
        charge_id = charge_response.id
        response = client.refund_charge(self.create_refund_body(), charge_id, str(randint(0, 10000)) + "abd")
        refund_response = response.get_body()
        self.assertEqual(refund_response.status, "ISSUED")
        self.assertEqual(refund_response.amount, charge_body.amount)

    def test_capture_charge(self):
        client = self.create_instance()
        charge_body = self.create_charge_body()
        response = client.charge(charge_body, str(randint(0, 10000)) + "abd")
        charge_response = response.get_body()
        charge_id = charge_response.id
        response = client.capture_charge(self.create_capture_body(), charge_id, str(randint(0, 10000)) + "abd")
        refund_response = response.get_body()
        self.assertEqual(refund_response.status, "CAPTURED")

    def test_refund_by_id(self):
        client = self.create_instance()
        charge_body = self.create_charge_body_with_capture()
        response = client.charge(charge_body, str(randint(0, 10000)) + "abd")
        charge_response = response.get_body()
        charge_id = charge_response.id
        response = client.refund_charge(self.create_refund_body(), charge_id, str(randint(0, 10000)) + "abd")
        refund_response = response.get_body()
        refund_id = refund_response.id
        response = client.get_refund_detail(charge_id, refund_id, str(randint(0, 10000)) + "abd")
        refund_response = response.get_body()
        self.assertEqual(refund_response.id, refund_id)

    def test_void_transaction(self):
        client = self.create_instance()
        charge_body = self.create_charge_body()
        charge_request_id = str(randint(0, 10000)) + "abd"
        client.charge(charge_body, charge_request_id)
        void_response = client.void_charge_transaction(charge_request_id)
        void_body_response = void_response.get_body()
        self.assertEqual(void_body_response.status, 'ISSUED')
        self.assertEqual(void_body_response.type, "VOID")


if __name__ == '__main__':
    unittest.main()
