from websocket_client import MarketSocket
from candle_builder import CandleBuilder
from indicators import apply
from decision_engine import decide
from config import SYMBOL
from market_feed import MarketFeed
from pair_rotation import PairRotationManager
from clock import CandleClock
import time

PAIRS = [
    "AAPL-OTC",
    "EURUSD-OTC",
    "GBPUSD-OTC"
]

builder = CandleBuilder()
feed = MarketFeed()
clock = CandleClock()
rotation = PairRotationManager(PAIRS, interval_seconds=10)

latest_signal = {}
current_pair = None

def on_tick(tick):
    global latest_signal

    symbol = tick["sym"]
    price = tick["price"]
    ts = tick["timestamp"]

    feed.update(symbol, price, ts)

    if symbol != current_pair:
        return

    builder.add_tick(price, ts)

    if not feed.is_live(symbol):
        return

    # só analisa quando perto de fechar a vela
    if clock.seconds_to_close() > 40:
        return

    if len(builder.candles) < 20:
        return

    df = apply(builder.candles)
    decision = decide(df)

    if decision:
        direction, prob = decision
        latest_signal = {
            "symbol": symbol,
            "direction": direction,
            "probability": prob,
            "time": clock.current_bucket()
        }
        print("SINAL:", latest_signal)

def start():
    global current_pair

    ws = MarketSocket(on_tick)
    ws.connect(None)  # conexão base sem subscribe

    while True:
        if rotation.should_switch():
            next_pair = rotation.next_pair()
            print("ROTATION →", next_pair)

            ws.unsubscribe(current_pair)
            ws.subscribe(next_pair)

            current_pair = next_pair

        time.sleep(0.2)

def get_signal():
    return latest_signal

def get_candles():
    return builder.get_candles()
