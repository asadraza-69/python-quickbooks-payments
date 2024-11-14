# Import necessary modules and classes
from app.quickbookspayments.paymentclient import PaymentClient
from app.quickbookspayments.operations.chargeoperations import ChargeOperations

# Create a PaymentClient instance with configuration
client = PaymentClient({
    'access_token': "your access token",
    'environment': "sandbox"  # or 'environment': "production"
})

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
        "expMonth": "12",
        "expYear": "2021",
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
