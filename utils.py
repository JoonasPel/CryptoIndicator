# pylint: disable=C0114, C0116, W0718
from urllib.parse import urljoin
from datetime import datetime, timedelta
import requests
from endpoints import BASE_ENDPOINT, PING_ENDPOINT

def get_error_description(error_code: int) -> str:
    description = ""
    match error_code:
        case 403:
            description = "WAF violated"
        case 409:
            description = "cancelReplace order partially succeed"
        case 418:
            description = "IP auto-banned. (Continued requesting after 429 too much)."
        case 429:
            description = "Request rate limit"
        case error_code if 400 <= error_code <= 499:
            description = "Malformed request. Sender's issue."
        case error_code if 500 <= error_code <= 599:
            description = "Internal server error. Execution status UNKNOWN! Might have succeeded."
        case _:
            description = f"Unknown error code: {error_code}."
    return description

def test_connection(timeout=3) -> bool:
    """Ping Binance to test connection.

    Args:
        timeout (int, optional): Timeout as seconds. Defaults to 3.

    Returns:
        bool: Binance returned succesfull response before timeout exceeded.
    """
    try:
        res = requests.get(urljoin(BASE_ENDPOINT, PING_ENDPOINT), timeout=timeout)
        return res.ok
    except Exception:
        return False

def unix_n_hours_ago_ms(hours):
    now = datetime.now()
    x_hours_ago = now - timedelta(hours=hours)
    return int(x_hours_ago.timestamp() * 1000)

def unix_now_ms():
    return int(datetime.now().timestamp() * 1000)

def is_non_descending(list):
    previous = list[0]
    for number in list:
        if number < previous:
            return False
        previous = number
    return True

def is_almost_non_descending(list, dips_allowed):
    """Checks if list is non descending but allows n dips."""
    dips = 0
    for i in range(1, len(list)):
        if list[i] < list[i - 1]:
            dips += 1
            if dips > dips_allowed:
                return False
    return True
