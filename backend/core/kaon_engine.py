from backend.market.candle_builder import CandleBuilder
from backend.market.indicators import rsi

class KaonEngine:
    def __init__(self):
        self.candles = []
        self.builder = CandleBuilder()

    def process_tick(self, timestamp, price):
        candle = self.builder.add_tick(timestamp, price)
        if candle:
            self.candles.append(candle)
            self.analyze()

    def analyze(self):
        closes = [c["close"] for c in self.candles]
        value = rsi(closes)
        if value and value < 30:
            print("📈 POSSÍVEL COMPRA")
        elif value and value > 70:
            print("📉 POSSÍVEL VENDA")
