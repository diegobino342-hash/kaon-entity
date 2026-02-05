from flask import Flask, jsonify
from flask_cors import CORS
from agent import Agent
import threading
import os

app = Flask(__name__)
CORS(app)

agent = Agent()

@app.route("/")
def index():
    return jsonify({
        "status": "online",
        "agent": "running"
    })

@app.route("/health")
def health():
    return jsonify({"ok": True})

def start_agent():
    agent.start()

if __name__ == "__main__":
    # inicia o agente em thread separada
    threading.Thread(target=start_agent, daemon=True).start()

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
