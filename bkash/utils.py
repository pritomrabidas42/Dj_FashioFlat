import requests
from django.conf import settings

def get_bkash_token():
    url = settings.BKASH_BASE_URL + 'token/grant'
    headers = {
        'Content-Type': 'application/json',
        'username': settings.BKASH_USERNAME,
        'password': settings.BKASH_PASSWORD,
        'Accept': 'application/json',
    }
    body = {
        "app_key": settings.BKASH_APP_KEY,
        "app_secret": settings.BKASH_APP_SECRET
    }
    response = requests.post(url, json=body, headers=headers)
    return response.json()

def create_payment(id_token, payment_request):
    url = settings.BKASH_BASE_URL + 'create'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + id_token,
        'X-APP-Key': settings.BKASH_APP_KEY,
    }
    response = requests.post(url, json=payment_request, headers=headers)
    return response.json()

def execute_payment(id_token, payment_id):
    url = settings.BKASH_BASE_URL + 'execute'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + id_token,
        'X-APP-Key': settings.BKASH_APP_KEY,
    }
    body = {"paymentID": payment_id}
    response = requests.post(url, json=body, headers=headers)
    return response.json()
