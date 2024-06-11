import requests
import time
import hmac
import hashlib
import json
from loguru import logger
import base64
import colorama
from auto.config_controller import BITGET_API_KEY, BITGET_SECRET_KEY, BITGET_PASSPHRASE, BITGET_BASE_URL

def create_signature(timestamp, method, endpoint, body, secret_key):
    body_str = json.dumps(body) if body else ''
    message = f'{timestamp}{method.upper()}{endpoint}{body_str}'
    hmac_sha256 = hmac.new(bytes(secret_key, 'utf-8'), msg=bytes(message, 'utf-8'), digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(hmac_sha256).decode()
    return signature

def open_market_order(symbol, side, size, order_type="market", local="en-US", product_type="usdt-futures", margin_mode="isolated", oneWayMode="true", margin_coin="USDT"):
    endpoint = "/api/v2/mix/order/place-order"
    url = BITGET_BASE_URL + endpoint
    timestamp = str(int(time.time() * 1000))
    method = "POST"

    body = {
        "symbol": symbol,
        "productType": product_type,
        "marginMode": margin_mode,
        "oneWayMode": oneWayMode,
        "marginCoin": margin_coin, 
        "size": size,
        "side": side, 
        "orderType": order_type,
    }

    body_str = json.dumps(body)
    
    headers = {
        "ACCESS-KEY": BITGET_API_KEY,
        "ACCESS-SIGN": create_signature(timestamp, method, endpoint, body, BITGET_SECRET_KEY),  
        "ACCESS-PASSPHRASE": BITGET_PASSPHRASE,
        "ACCESS-TIMESTAMP": timestamp,
        "Content-Type": "application/json",
        "locale": local  
    }

    logger.debug(colorama.Fore.LIGHTWHITE_EX + f"Sending request to {url} with headers {headers} and body {body_str}")
    
    response = requests.post(url, headers=headers, data=body_str)
    try:
        response.raise_for_status()
        logger.info(f"Order response: {response.json()}")
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error placing order on Bitget: {e.response.text}")
        return None

def close_position(symbol, productType, holdSide):
    endpoint = "/api/v2/mix/order/close-positions"
    url = BITGET_BASE_URL + endpoint
    timestamp = str(int(time.time() * 1000))
    method = "POST"

    body = {
        "symbol": symbol,
        "productType": productType,
        "holdSide": holdSide
    }

    headers = {
        "ACCESS-KEY": BITGET_API_KEY,
        "ACCESS-SIGN": create_signature(timestamp, method, endpoint, body, BITGET_SECRET_KEY),
        "ACCESS-PASSPHRASE": BITGET_PASSPHRASE,
        "ACCESS-TIMESTAMP": timestamp,
        "Content-Type": "application/json",
        "locale": "en-US"
    }

    response = requests.post(url, headers=headers, json=body)
    try:
        response.raise_for_status()
        logger.info(f"Close position response: {response.json()}")
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error closing position on Bitget: {e.response.text}")
        return None
