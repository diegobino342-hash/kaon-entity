import websocket
import json
import threading

class MarketSocket:
    def __init__(self):
        self.url = "wss://ws.derivws.com/websockets/v3?app_id=1089"
        self.ws = None

    def connect(self):
        print("[WS] Criando conexão WebSocket...")

        self.ws = websocket.WebSocketApp(
            self.url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )

        threading.Thread(
            target=self.ws.run_forever,
            daemon=True
        ).start()

    def on_open(self, ws):
        print("[WS] Conectado com sucesso")

        # subscribe em ticks reais (exemplo EUR/USD)
        payload = {
            "ticks": "frxEURUSD",
            "subscribe": 1
        }

        ws.send(json.dumps(payload))

    def on_message(self, ws, message):
        data = json.loads(message)

        if "tick" in data:
            price = data["tick"]["quote"]
            symbol = data["tick"]["symbol"]
            print(f"[TICK] {symbol} → {price}")

    def on_error(self, ws, error):
        print("[WS ERROR]", error)

    def on_close(self, ws, close_status_code, close_msg):
        print("[WS] Conexão encerrada")
