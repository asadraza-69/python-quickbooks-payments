import unittest
from random import randint
from app.quickbookspayments.operations.bankaccountoperations import BankAccountOperations


class BankAccountTest(unittest.TestCase):

    def create_instance(self):
        return TestClientCreator.create_instance()

    def create_bank_body(self):
        bank_body = BankAccountOperations.build_from({
            "phone": "6047296480",
            "routingNumber": "322079353",
            "name": "My Checking",
            "accountType": "PERSONAL_CHECKING",
            "accountNumber": "11000000333456781"
        })
        return bank_body

    def test_create_bank_account(self):
        client = self.create_instance()
        bank = self.create_bank_body()
        client_id = randint(0, 10000)
        response = client.create_bank_account(bank, client_id)
        response_bank = response.get_body()
        routing_number = response_bank.routingNumber[-4:]
        passed_number = bank.routingNumber[-4:]
        self.assertEqual(routing_number, passed_number)

    def test_create_token_for_bank(self):
        client = self.create_instance()
        bank = self.create_bank_body()
        client_id = randint(0, 10000)
        response = client.create_token(bank)
        token = response.get_body()
        self.assertIsNotNone(token.value)

    def test_create_bank_account_from_token(self):
        client = self.create_instance()
        bank = self.create_bank_body()
        client_id = randint(0, 10000)
        response = client.create_token(bank)
        token = response.get_body().value
        response = client.create_bank_account_from_token(randint(0, 10000), token)
        routing_number = response.get_body().routingNumber[-4:]
        passed_number = bank.routingNumber[-4:]
        self.assertEqual(routing_number, passed_number)

    def test_delete_bank_account(self):
        client = self.create_instance()
        bank = self.create_bank_body()
        client_id = randint(0, 10000)
        response = client.create_bank_account(bank, client_id)
        response_bank_id = response.get_body().id
        response = client.delete_bank_account(client_id, response_bank_id)
        self.assertEqual(response.get_status_code(), 204)

    def test_get_all_bank_accounts(self):
        client = self.create_instance()
        bank = self.create_bank_body()
        client_id = randint(0, 10000)
        response = client.create_bank_account(bank, client_id)
        response_bank_id = response.get_body().id
        response = client.get_all_bank_account(client_id)
        bank_account = response.get_body()[0]
        routing_number = bank_account.routingNumber[-4:]
        passed_number = bank.routingNumber[-4:]
        self.assertEqual(routing_number, passed_number)

    def test_get_bank_accounts(self):
        client = self.create_instance()
        bank = self.create_bank_body()
        client_id = randint(0, 10000)
        response = client.create_bank_account(bank, client_id)
        response_bank_id = response.get_body().id
        response = client.get_bank_account(client_id, response_bank_id)
        self.assertEqual(response_bank_id, response.get_body().id)

if __name__ == '__main__':
    unittest.main()
