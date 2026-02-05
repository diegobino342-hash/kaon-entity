from market_socket import MarketSocket
import time

class Agent:
    def __init__(self):
        self.socket = MarketSocket()

    def start(self):
        print("[AGENT] Iniciando agente em tempo real...")
        self.socket.connect()

        # loop vivo apenas para manter o processo ativo
        while True:
            time.sleep(1)
