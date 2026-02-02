import requests

def get_history(symbol, start, end):
    url = f"https://market-historic-api.homebroker.com/assets/read_values"
    params = {
        "symbol": symbol,
        "start": start,
        "end": end,
        "timespan": "minutes",
        "multiple": 1
    }
    return requests.get(url, params=params).json()
