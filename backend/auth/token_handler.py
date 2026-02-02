import os

def get_bearer_token():
    return os.getenv("BEARER_TOKEN")
