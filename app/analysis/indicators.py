import pandas as pd
import ta

def apply_indicators(candles):
    df = pd.DataFrame(candles)
    df["rsi"] = ta.momentum.RSIIndicator(df["close"]).rsi()
    bb = ta.volatility.BollingerBands(df["close"])
    df["bb_high"] = bb.bollinger_hband()
    df["bb_low"] = bb.bollinger_lband()
    return df
