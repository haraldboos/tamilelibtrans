# import requests
# api_key = 'YOUR_API_KEY_HERE'
# amount = 10
#     # Add other necessary parameters
    
# api_url = 'https://tamilpubliclibrary.zahls.ch/de/vpos'
# headers = {'Authorization': f'Bearer {api_key}'}
# payload = {
#         'amount': amount,
#         # Add other parameters here
#     }
    
# response = requests.post(api_url, headers=headers, data=payload)
# print(response)
# import urllib.request
# import hmac
# import hashlib
import base64

# post_data = {}

# # http query string for signature calculation
# try:
#     httpQueryString = urllib.parse.urlencode(post_data).encode('UTF-8')
#     apiSignature = hmac.new(b'XxCskNVxWCSkUFPfJDNo57j9UdEXst', msg=httpQueryString, digestmod=hashlib.sha256).digest()

#     # http query string for payload
#     payload = urllib.parse.urlencode(post_data, quote_via=urllib.parse.quote, safe='[|]').encode('UTF-8')
# except:
#     print('somre except')
# import urllib.request
# import hmac
# import hashlib
# import base64
# import sys

# post_data = {}

# data = urllib.parse.urlencode(post_data).encode('UTF-8')

# dig = hmac.new(b'XxCskNVxWCSkUFPfJDNo57j9UdEXst', msg=data, digestmod=hashlib.sha256).digest()
# post_data['ApiSignature'] = base64.b64encode(dig).decode()
# post_data['instance'] = 'tamilpubliclibrary'

# data = urllib.parse.urlencode(post_data, quote_via=urllib.parse.quote).encode('UTF-8')

# try:
#     result = urllib.request.urlopen(' https://api.zahls.ch/v1/SignatureCheck/?' + data.decode())
#     print(result)
#     sys.exit("Signature correct")
# except Exception as exc:
#     print(exc, file=sys.stderr)
#     sys.exit("Signature wrong")
# import requests

# url = "https://api.zahls.ch/v1/Transaction/"

# headers = {
#     "accept": "application/json",
#     "content-type": "application/x-www-form-urlencoded"
# }

# response = requests.post(url, headers=headers)

# print(response.text)
import requests

api_key = "XxCskNVxWCSkUFPfJDNo57j9UdEXst"
api_secret = "XxCskNVxWCSkUFPfJDNo57j9UdEXst"
url = "https://api.zahls.ch/v1/gateways"  # Replace with specific endpoint

payload = {
    "amount": 1000,  # Example amount in cents
    "currency": "EUR",
    # Add other product and customer details as needed
}

headers = {
    "Authorization": f"Basic {base64.b64encode(f'{api_key}:{api_secret}'.encode()).decode()}"
}

response = requests.post(url, json=payload, headers=headers)
print(response)