import requests

def get_server_time():
    return requests.get(
        "https://configuration-api.homebroker.com/api/get-time/"
    ).json()
