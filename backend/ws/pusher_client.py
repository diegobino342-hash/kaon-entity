import json
import websocket
from backend.config.settings import PUSHER_APP_KEY, PUSHER_HOST, ORIGIN

class PusherClient:
    def __init__(self, on_message):
        self.on_message = on_message
        self.ws = None

    def connect(self):
        url = f"{PUSHER_HOST}/app/{PUSHER_APP_KEY}?protocol=7&client=js&version=8.4.0"
        self.ws = websocket.WebSocketApp(
            url,
            header=[f"Origin: {ORIGIN}"],
            on_message=self.on_message
        )
        self.ws.run_forever()

    def send(self, payload):
        self.ws.send(json.dumps(payload))
