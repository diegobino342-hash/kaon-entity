import websocket
import json
from config import WS_URL, ORIGIN

class MarketSocket:
    def __init__(self, on_tick):
        self.on_tick = on_tick

    def on_message(self, ws, msg):
        data = json.loads(msg)
        if "event" in data and "-OTC" in data["event"]:
            tick = json.loads(data["data"])
            self.on_tick(tick)

    def connect(self, symbol):
        self.ws = websocket.WebSocketApp(
            WS_URL,
            header=[f"Origin: {ORIGIN}"],
            on_message=self.on_message
        )

        def on_open(ws):
            ws.send(json.dumps({
                "event": "pusher:subscribe",
                "data": {"auth": "", "channel": symbol}
            }))

        self.ws.on_open = on_open
        self.ws.run_forever()
