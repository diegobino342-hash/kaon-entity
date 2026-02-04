import websocket
import json
import threading
import time
from config import WS_URL, ORIGIN

class MarketSocket:
    def __init__(self, on_tick):
        self.on_tick = on_tick
        self.ws = None

    def _on_message(self, ws, message):
        try:
            data = json.loads(message)
            if "event" in data and "-OTC" in data["event"]:
                tick = json.loads(data["data"])
                self.on_tick(tick)
        except Exception as e:
            print("WS parse error:", e)

    def _on_open(self, ws, symbol):
        ws.send(json.dumps({
            "event": "pusher:subscribe",
            "data": {"auth": "", "channel": symbol}
        }))
        print(f"WS SUBSCRIBED: {symbol}")

    def start(self, symbol):
        def run():
            while True:
                try:
                    self.ws = websocket.WebSocketApp(
                        WS_URL,
                        header=[f"Origin: {ORIGIN}"],
                        on_message=self._on_message,
                        on_open=lambda ws: self._on_open(ws, symbol)
                    )
                    self.ws.run_forever(ping_interval=60, ping_timeout=10)
                except Exception as e:
                    print("WS error, reconnecting:", e)
                time.sleep(5)

        threading.Thread(target=run, daemon=True).start()
