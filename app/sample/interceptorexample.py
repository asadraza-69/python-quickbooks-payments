# Import necessary modules and classes
from app.quickbookspayments.paymentclient import PaymentClient
from app.quickbookspayments.operations.chargeoperations import ChargeOperations
from app.quickbookspayments.operations.cardoperations import  CardOperations
from app.quickbookspayments.interceptors.stacktraceloggerinterceptor import StackTraceLoggerInterceptor
from random import randint


def create_card_body():
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
# Create a PaymentClient instance
client = PaymentClient({
    'access_token': "The accessToken",
    'environment': "sandbox"  # or 'environment': "production"
})

# Add interceptors for logging
client.add_interceptor("FileInterceptor", StackTraceLoggerInterceptor("/Users/hlu2/Desktop/newFolderForLog/logTest/", 'America/Los_Angeles'))

# Create a dictionary for the charge request
charge_data = {
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
}

# Build the charge from the dictionary
charge = ChargeOperations.build_from(charge_data)
response = client.charge(charge)

# Create card and handle response
card = create_card_body()
client_id = randint(1, 1000000)  # Random client ID for testing
response = client.create_card(card, client_id, f"{randint(1, 1000000)}abd")

# Check if the response indicates a failure
if response.failed():
    code = response.get_status_code()
    error_message = response.get_body()
    print(f"code is {code}")
    print(f"body is {error_message}")
else:
    response_charge = response.get_body()
    # Get the Id of the charge request
    charge_id = response_charge.id
    # Get the Status of the charge request
    status = response_charge.status
    print(f"Id is {charge_id}")
    print(f"status is {status}")