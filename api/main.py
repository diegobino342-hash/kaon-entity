import threading
import asyncio
from flask import Flask, jsonify
from flask_cors import CORS
from engine import KaonEngine

app = Flask(__name__)
CORS(app)

# Instancia o motor
engine = KaonEngine()

def start_engine():
    """Função para rodar o loop assíncrono em uma thread separada"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(engine.scan_market())

# Inicia o motor neural em background
threading.Thread(target=start_engine, daemon=True).start()

@app.route('/')
def home():
    return "KAON NEURAL ENTITY ONLINE - AGENTE ATIVO"

@app.route('/status')
def get_status():
    # Coleta os dados do motor para o Dashboard
    return jsonify({
        "pair": getattr(engine, 'current_pair', "Iniciando..."),
        "price": getattr(engine, 'last_price', 0),
        "signal": getattr(engine, 'active_signal', None),
        "status": "Running"
    })

if __name__ == "__main__":
    # O Render usa a porta 10000 por padrão ou a definida pela variável PORT
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
