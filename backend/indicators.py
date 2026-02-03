import pandas as pd
import ta

def apply(candles):
    df = pd.DataFrame(candles)
    df["rsi"] = ta.momentum.RSIIndicator(df["close"]).rsi()
    bb = ta.volatility.BollingerBands(df["close"])
    df["bb_low"] = bb.bollinger_lband()
    df["bb_high"] = bb.bollinger_hband()
    return df
