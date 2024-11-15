import unittest
from random import randint

from app.quickbookspayments.operations.cardoperations import CardOperations
from app.test.testclientcreator import TestClientCreator


class CardTest(unittest.TestCase):

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

    def create_card_body2(self):
        card_body = CardOperations.build_from({
            "expMonth": "11",
            "address": {
                "postalCode": "44112",
                "city": "Richmond",
                "streetAddress": "White Street 132",
                "region": "VA",
                "country": "US"
            },
            "number": "4948759199127257",
            "name": "Sophia Perez",
            "expYear": "2022"
        })
        return card_body

    def test_create_card_request_on_sandbox(self):
        client = self.create_instance()
        card = self.create_card_body()
        client_id = randint(0, 10000)
        response = client.create_card(card, client_id, str(randint(0, 10000)) + "abd")
        card_response = response.get_body()
        self.assertEqual(card_response.name, card.name)
        self.assertEqual(card_response.expYear, card.expYear)

    def test_delete_card_request_on_sandbox(self):
        client = self.create_instance()
        card = self.create_card_body()
        customer_id = randint(0, 10000)
        response = client.create_card(card, customer_id, str(randint(0, 10000)) + "abd")
        card_response = response.get_body()
        response = client.delete_card(customer_id, card_response.id, str(randint(0, 10000)) + "abd")
        self.assertEqual(response.get_status_code(), 204)
        self.assertIsNone(response.get_body())

    def test_all_cards_on_sandbox(self):
        client = self.create_instance()
        card = self.create_card_body()
        card2 = self.create_card_body2()
        customer_id = randint(0, 10000)
        response = client.create_card(card, customer_id)
        id1 = response.get_body().id
        response = client.create_card(card2, customer_id)
        id2 = response.get_body().id

        response = client.get_all_cards_for(customer_id)
        body = response.get_body()
        card1 = body[0]
        card2 = body[1]

        self.assertEqual(card1.id, id2)
        self.assertEqual(card2.id, id1)

        client.delete_card(customer_id, id1)
        client.delete_card(customer_id, id2)

    def test_find_a_customer_card_on_sandbox(self):
        client = self.create_instance()
        card = self.create_card_body()
        customer_id = randint(0, 10000)

        # Add a test card
        response = client.create_card(card, customer_id)
        id1 = response.get_body().id
        secure_card_number1 = response.get_body().number

        # Retrieve the test card
        response2 = client.get_card(customer_id, id1)
        id2 = response2.get_body().id
        secure_card_number2 = response.get_body().number

        # Make sure the retrieved secure card matches the originally added card
        self.assertEqual(id1, id2)
        self.assertEqual(secure_card_number1, secure_card_number2)

        client.delete_card(customer_id, id1)

    def test_create_card_token(self):
        client = self.create_instance()
        card = self.create_card_body()
        response = client.create_token(card)
        value = response.get_body().value
        customer_id = randint(0, 10000)
        response = client.create_card_from_token(customer_id, value)
        self.assertEqual(card.expMonth, response.get_body().expMonth)
        self.assertEqual(card.name, response.get_body().name)


if __name__ == '__main__':
    unittest.main()
