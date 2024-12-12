import requests

# Zahls payment API endpoint (replace with actual URL)
api_url = "https://api.zahls.ch/v1/payment"

# Your Zahls API key (replace with actual key)
api_key = "uclUsfM1OxlJX2cDTH6iiRcbZVm6Bv"

# Sample payment data (modify with the actual payment details)
payment_data = {
    "amount": 100.0,  # Ensure the amount is a valid number (e.g., 100.0 for $100)
    "currency": "USD",  # Ensure currency is a valid ISO code (e.g., "USD")
    "payment_method": "credit_card",  # Ensure the payment method is valid
    "card_details": {
        "card_number": "4111111111111111",  # Replace with a valid test card number
        "expiration_date": "12/25",  # Use the format MM/YY
        "cvv": "123"  # Use a valid CVV
    },
    "billing_address": {
        "name": "John Doe",
        "address": "1234 Main Street",
        "city": "New York",
        "state": "NY",
        "zip": "10001",
        "country": "US"
    },
    "customer_email": "customer@example.com"
}


# Sending the payment request
response = requests.post(api_url, json=payment_data, headers={"Authorization": f"Bearer {api_key}"},verify=False)

# Check if the payment was successful

if response.status_code == 200:
    print("Payment successful:", response.json())
else:
    print("Payment failed with status code:", response.status_code)
    print("Response:", response.text)
