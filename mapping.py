import requests
import json

def fetch_top_altcoins(limit=200): ## max 500
    url = f"https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': limit,
        'page': 1,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

def calc(price):
    return round(500 / price, 8) # for change price 

def extract_name_symbol_price(data):
    name_symbol_price = {}
    for coin in data:
        name = coin['symbol'].upper()
        symbol = coin['symbol'].upper() + "USDT"
        price = calc(coin['current_price'])
        name_symbol_price[name] = {"symbol": symbol, "size": price}
    return name_symbol_price


def export_mapping_to_json(mapping, filename):
    with open(filename, "w") as file:
        file.write("{\n")
        for key, value in mapping.items():
            file.write(f'    "{key}": {json.dumps(value, separators=(",", ":"))},\n')
        file.write("}\n")
    print(f"Mapping exported to {filename}")


if __name__ == "__main__":
    top_altcoins_data = fetch_top_altcoins()
    if top_altcoins_data:
        name_symbol_price_mapping = extract_name_symbol_price(top_altcoins_data)
        export_mapping_to_json(name_symbol_price_mapping, "mapping.yaml")
