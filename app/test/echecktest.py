import unittest
from random import randint
from app.quickbookspayments.operations.echeckoperations import ECheckOperations
from app.quickbookspayments.paymentclient import PaymentClient

class ECheckTest(unittest.TestCase):

    def create_instance(self):
        return TestClientCreator.create_instance()

    def create_echeck_body(self):
        echeck_body = ECheckOperations.build_from({
            "bankAccount": {
                "phone": "1234567890",
                "routingNumber": "490000018",
                "name": "Fname LName",
                "accountType": "PERSONAL_CHECKING",
                "accountNumber": "1100000033345678"
            },
            "description": "Check Auth test call",
            "checkNumber": str(randint(1, 99999999)).zfill(8),
            "paymentMode": "WEB",
            "amount": "5.55",
            "context": {
                "deviceInfo": {
                    "macAddress": "macaddress",
                    "ipAddress": "34",
                    "longitude": "longitude",
                    "phoneNumber": "phonenu",
                    "latitude": "",
                    "type": "type",
                    "id": "1"
                }
            }
        })
        return echeck_body

    def test_retrieve_echeck(self):
        client = self.create_instance()
        echeck_body = self.create_echeck_body()
        response = client.debit(echeck_body)
        echeck_id = response.get_body().id
        response = client.retrieve_echeck(echeck_id)
        self.assertEqual(response.get_body().id, echeck_id)

    def test_create_debit(self):
        client = self.create_instance()
        echeck_body = self.create_echeck_body()
        response = client.debit(echeck_body)
        self.assertEqual(response.get_body().checkNumber, echeck_body.checkNumber)
        self.assertEqual(response.get_body().amount, echeck_body.amount)

    def test_void_or_refund_echecks(self):
        client = self.create_instance()
        echeck_body = self.create_echeck_body()
        response = client.debit(echeck_body)
        echeck_id = response.get_body().id
        body = ECheckOperations.build_from({
            "amount": 5.55
        })
        response = client.void_or_refund_echeck(body, echeck_id)
        self.assertEqual(response.get_body().amount, echeck_body.amount)

if __name__ == '__main__':
    unittest.main()
