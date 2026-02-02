def decide(df):
    last = df.iloc[-1]

    confluences = 0
    direction = None

    if last["rsi"] < 30 and last["close"] < last["bb_low"]:
        confluences += 2
        direction = "CALL"

    if last["rsi"] > 70 and last["close"] > last["bb_high"]:
        confluences += 2
        direction = "PUT"

    probability = confluences / 5

    if probability >= 0.8:
        return {
            "direction": direction,
            "probability": round(probability * 100, 2),
            "reason": "RSI + Bollinger"
        }

    return None
