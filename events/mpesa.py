# events/mpesa.py
import requests
from requests.auth import HTTPBasicAuth
import datetime
import base64

# Replace with your own credentials
consumer_key = 'gWOyc7plaasiCxc3GINInkUYzQeagmPf6JAD0RjFpuxgjjcZ'
consumer_secret = 'XG8FGKNT5qQUGT3pGSTbORZGs9HQYUEcwmRTuaHbwwvwdGEAtoNujnYhTRX2fqSA'
business_shortcode = '174379'  # Test Paybill
lipa_na_mpesa_passkey = 'YOUR_PASSKEY'
callback_url = 'https://yourdomain.com/payment/callback/'

def get_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    return response.json()['access_token']

def lipa_na_mpesa(phone_number, amount):
    access_token = get_access_token()
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    password = base64.b64encode((business_shortcode + lipa_na_mpesa_passkey + timestamp).encode()).decode('utf-8')

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "BusinessShortCode": business_shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": business_shortcode,
        "PhoneNumber": phone_number,
        "CallBackURL": callback_url,
        "AccountReference": "EVENTS",
        "TransactionDesc": "Payment for event"
    }

    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()
