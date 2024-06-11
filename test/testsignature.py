import requests
import time
import hmac
import hashlib
import base64
import json
import urllib.parse

# API Credentials BIGET !!!
API_KEY = ''
KEY = ''
PASSPHRASE = ''
BASE_URL = 'https://api.bitget.com'

def create_signature(secret_key, timestamp, method, request_path, query_string='', body=''):
    """
    Generates an HMAC SHA256 signature required for Bitget API authentication.
    Adjusted to include query string in signature for GET requests.
    """
    if method.upper() == 'GET' and query_string:
        # For GET requests, include the encoded query string in the message
        message = f'{timestamp}{method.upper()}{request_path}?{query_string}'
    else:
        message = f'{timestamp}{method.upper()}{request_path}{body}'

    secret_key_bytes = bytes(secret_key, 'utf-8')
    message_bytes = bytes(message, 'utf-8')
    hmac_sha256 = hmac.new(secret_key_bytes, msg=message_bytes, digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(hmac_sha256).decode()
    return signature

def get_all_positions(product_type, margin_coin):
    """
    Fetches all positions for a specified product type and margin coin.
    Adjusted to properly include query parameters in the signature.
    """
    endpoint = "/api/v2/mix/position/all-position"
    query_params = {
        "productType": product_type,
        "marginCoin": margin_coin,
    }
    query_string = urllib.parse.urlencode(sorted(query_params.items()))
    url = f"{BASE_URL}{endpoint}?{query_string}"
    timestamp = str(int(time.time() * 1000))
    method = 'GET'
    signature = create_signature(KEY, timestamp, method, endpoint, query_string=query_string)

    headers = {
        "Content-Type": "application/json",
        "ACCESS-KEY": API_KEY,
        "ACCESS-SIGN": signature, 
        "ACCESS-TIMESTAMP": timestamp,
        "ACCESS-PASSPHRASE": PASSPHRASE,
        "locale": "en-US"
    }
    
    response = requests.get(url, headers=headers)
    
    try:
        response.raise_for_status()
        print("Positions retrieved successfully:", response.json())
    except requests.exceptions.HTTPError as err:
        print("Failed to retrieve positions:", err.response.text)

if __name__ == "__main__":
    product_type = "USDT-FUTURES"
    margin_coin = "USDT"
    get_all_positions(product_type, margin_coin)
