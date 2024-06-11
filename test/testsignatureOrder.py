import requests
import time
import hmac
import hashlib
import base64
import json

# API Credentials
API_KEY = ''
KEY = ''
PASSPHRASE = ''
BASE_URL = 'https://api.bitget.com'

def create_signature(secret_key, timestamp, method, request_path, query_string='', body=''):
    """
    Generates an HMAC SHA256 signature required for Bitget API authentication.
    Adjusted to include query string in signature for GET requests and body for POST requests.
    """
    if method.upper() == 'GET' and query_string:
        message = f'{timestamp}{method.upper()}{request_path}?{query_string}'
    else:
        message = f'{timestamp}{method.upper()}{request_path}{body}'

    secret_key_bytes = bytes(secret_key, 'utf-8')
    message_bytes = bytes(message, 'utf-8')
    hmac_sha256 = hmac.new(secret_key_bytes, msg=message_bytes, digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(hmac_sha256).decode()
    return signature

def place_market_order(symbol, side, size, margin_coin, product_type="USDT-FUTURES", margin_mode="isolated", position_side="long", oneWayMode="true"):
    endpoint = "/api/v2/mix/order/place-order"
    url = f"{BASE_URL}{endpoint}"
    timestamp = str(int(time.time() * 1000))
    method = 'POST'
    body = {
        "symbol": symbol,
        "marginCoin": margin_coin,
        "productType": product_type,
        "oneWayMode": oneWayMode,
        "marginMode": margin_mode,
        "size": size,
        "side": side,
        "positionSide": position_side,
        "orderType": "market",
    }
    body_str = json.dumps(body)
    signature = create_signature(KEY, timestamp, method, endpoint, body=body_str)

    headers = {
        "Content-Type": "application/json",
        "ACCESS-KEY": API_KEY,
        "ACCESS-SIGN": signature,
        "ACCESS-TIMESTAMP": timestamp,
        "ACCESS-PASSPHRASE": PASSPHRASE,
        "locale": "en-US"
    }
    
    response = requests.post(url, headers=headers, data=body_str)
    
    try:
        response.raise_for_status()
        print("Commande placée avec succès :", response.json())
    except requests.exceptions.HTTPError as err:
        print("Échec de placement de la commande :", err.response.text)


if __name__ == "__main__":
    symbol = "SOLUSDT"  # Example symbol
    side = "buy"  # "buy" or "sell"
    size = "0.1"  # The amount to buy/sell
    margin_coin = "USDT"  # The margin coin 
    place_market_order(symbol, side, size, margin_coin)
