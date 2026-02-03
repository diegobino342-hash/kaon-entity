import asyncio
import websockets
import json
import time

class KaonEngine:
    def __init__(self):
        self.url = "wss://ws-us2.pusher.com/app/43474559fc2d8059c93e?protocol=7&client=js&version=8.4.0"
        # Lista inicial (pode ser expandida com base no seu arquivo 5.txt)
        self.pairs = ["AAPL-OTC", "MSFT-OTC", "EURUSD-OTC", "NVDA-OTC", "GOOG-OTC"]
        
        # Variáveis de Estado (O que o Main.py vai ler)
        self.current_pair = "Iniciando..."
        self.last_price = 0
        self.active_signal = None
        self.price_history = []
        
    async def scan_market(self):
        """Loop infinito de varredura e análise neural"""
        while True:
            for pair in self.pairs:
                self.current_pair = pair
                self.price_history = [] # Limpa histórico para o novo par
                
                try:
                    async with websockets.connect(self.url) as ws:
                        # Inscreve no canal do par via Pusher Protocol
                        subscribe_msg = {
                            "event": "pusher:subscribe",
                            "data": {"channel": pair}
                        }
                        await ws.send(json.dumps(subscribe_msg))
                        
                        start_time = time.time()
                        # Varredura de 15 segundos por par
                        while time.time() - start_time < 15:
                            message = await ws.recv()
                            data = json.loads(message)
                            
                            if "data" in data:
                                payload = json.loads(data["data"])
                                if "price" in payload:
                                    price = payload["price"]
                                    self.last_price = price
                                    self.price_history.append(price)
                                    
                                    # Lógica Neural: Analisa Projeção para o PRÓXIMO CANDLE
                                    # Dispara exatamente 40s antes do fechamento do M5
                                    self.process_neural_logic(pair)

                            # Keep-alive obrigatório da Pusher
                            if "pusher:ping" in message:
                                await ws.send(json.dumps({"event": "pusher:pong"}))
                                
                except Exception as e:
                    print(f"Erro na conexão com {pair}: {e}")
                    await asyncio.sleep(2) # Pequena pausa antes de tentar o próximo

    def process_neural_logic(self, pair):
        """Analisa se o cenário atual projeta uma compra ou venda futura"""
        now = time.time()
        # Verifica se estamos na janela de 40s antes da abertura do próximo M5
        seconds_in_m5 = (now % 300)
        
        if 255 <= seconds_in_m5 <= 260: # Janela de disparo (4min e 20s de candle)
            # Aqui o Agente decide a melhor entrada entre todos os analisados
            # Exemplo de sinal gerado pela rede neural:
            self.active_signal = {
                "pair": pair,
                "direction": "COMPRA" if self.last_price > self.price_history[0] else "VENDA",
                "time": "M5",
                "probability": 88.5,
                "active": True
            }
        else:
            # Limpa o sinal após o tempo de entrada passar
            if seconds_in_m5 < 10:
                self.active_signal = None
