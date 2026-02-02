from core.websocket_client import WebSocketClient
from core.asset_manager import AssetManager
from analysis.decision_engine import DecisionEngine
from notifications.telegram import send_signal
from logger import log
import time

def main():
    log("KAON iniciado")

    assets = AssetManager().get_active_assets()
    ws = WebSocketClient()
    engine = DecisionEngine()

    ws.connect()

    while True:
        for asset in assets:
            log(f"Analisando {asset}")
            ws.subscribe(asset)

            time.sleep(15)  # troca automática de par

            candles = ws.get_candles(asset)
            decision = engine.analyze(asset, candles)

            if decision:
                send_signal(decision)
                ws.unsubscribe(asset)
                time.sleep(300)  # 5 min de operação
                break

            ws.unsubscribe(asset)

if __name__ == "__main__":
    main()
