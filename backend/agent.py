import time
from market_socket import MarketSocket

class TradingAgent:
    def __init__(self):
        self.ws = MarketSocket()

    def start(self):
        self.ws.connect()

        # mantém o agente vivo
        while True:
            time.sleep(1)
