# pylint: disable=C0114, C0116, W0718, W0401, W0614
from urllib.parse import urljoin
import requests
from endpoints import *  # NOSONAR

def get_avg_price(symbol):
    url = urljoin(BASE_ENDPOINT, AVG_PRICE_ENDPOINT)
    params = {"symbol": symbol}
    return fetch(url, params)

def get_price_history(symbol, interval, start_time, end_time):
    url = urljoin(BASE_ENDPOINT, KLINES_ENDPOINT)
    params = {"symbol": symbol, "interval": interval, "startTime": start_time, "endTime": end_time}
    return fetch(url, params)

def get_current_price(symbol):
    url = urljoin(BASE_ENDPOINT, TICKER_ENDPOINT)
    params = {"symbol": symbol}
    return fetch(url, params)

def get_symbols(currency):
    url = urljoin(BASE_ENDPOINT, INFO_ENDPOINT)
    info = fetch(url)
    symbols = []
    for symbol in info["symbols"]:
        if symbol["symbol"].endswith(currency):
            symbols.append(symbol["symbol"])
    return symbols

def fetch(url, params=None):
    try:
        res = requests.get(url=url, params=params, timeout=5)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"Error fetching.\nURL -> {url}\nPARAMS -> {params}\nERROR -> {e}")
        return None
