import requests
from config import ASSETS_URL, HOME_BROKER_BEARER

class AssetManager:
    def get_active_assets(self):
        headers = {"Authorization": f"Bearer {HOME_BROKER_BEARER}"}
        r = requests.get(ASSETS_URL, headers=headers).json()
        return [
            a["symbol"]
            for a in r
            if a["is_active"] and a["profit_payout"] >= 80
        ]
