from flask import Flask, jsonify
from candle_builder import CandleBuilder
from indicators import apply
from decision_engine import decide

app = Flask(__name__)
last_signal = {}

@app.route("/signal")
def signal():
    return jsonify(last_signal)

@app.route("/")
def health():
    return {"status": "KAON ONLINE"}

app.run(host="0.0.0.0", port=10000)
