import requests
from config import PAPARA_API_KEY, PAPARA_API_URL

def get_account_balance():
    url = f"{PAPARA_API_URL}/v1/Account/balance"
    headers = {
        'ApiKey': PAPARA_API_KEY,
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['data']['balance']
    else:
        return None

def create_payment(reference_code, amount, currency='TRY'):
    url = f"{PAPARA_API_URL}/v1/Payment"
    headers = {
        'ApiKey': PAPARA_API_KEY,
        'Content-Type': 'application/json'
    }
    data = {
        "amount": amount,
        "referenceId": reference_code,
        "currency": currency,
        "description": "Payment Description"
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['data']
    else:
        return None

def check_payment(reference_code):
    url = f"{PAPARA_API_URL}/v1/Payment?referenceId={reference_code}"
    headers = {
        'ApiKey': PAPARA_API_KEY,
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        payment_data = response.json()['data']
        return payment_data['status'] == 1  # 1 status indicates completed payment
    else:
        return False
