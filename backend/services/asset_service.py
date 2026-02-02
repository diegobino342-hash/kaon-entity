import requests
from backend.auth.token_handler import get_bearer_token

URL = "https://user-api.homebroker.com/config/assets"

def get_assets():
    headers = {"Authorization": f"Bearer {get_bearer_token()}"}
    return requests.get(URL, headers=headers).json()
