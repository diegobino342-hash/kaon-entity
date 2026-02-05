import threading
import os
from flask import Flask
from agent import TradingAgent

app = Flask(__name__)

@app.route("/")
def health():
    return {"status": "KAON backend online"}

def start_agent():
    agent = TradingAgent()
    agent.start()

if __name__ == "__main__":
    # inicia o agente em background
    threading.Thread(
        target=start_agent,
        daemon=True
    ).start()

    # Render exige porta aberta
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
