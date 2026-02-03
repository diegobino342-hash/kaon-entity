import threading
import asyncio
import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from engine import KaonEngine

app = Flask(__name__, static_folder='../frontend')
CORS(app)

# Inicializa o motor neural
engine = KaonEngine()

def start_engine_loop():
    """Gerenciador do ciclo de vida do motor assíncrono em background"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # Roda o scanner de mercado indefinidamente
    loop.run_until_complete(engine.scan_market())

# Inicia a thread do motor antes do Flask para garantir a captura de dados
engine_thread = threading.Thread(target=start_engine_loop, daemon=True)
engine_thread.start()

# --- ROTAS DO WEB APP ---

@app.route('/')
def serve_index():
    """Serve a interface visual do agente"""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve arquivos CSS, JS e imagens"""
    return send_from_directory(app.static_folder, path)

@app.route('/status')
def get_status():
    """Endpoint que o frontend consulta para atualizar o gráfico e sinais"""
    return jsonify({
        "pair": getattr(engine, 'current_pair', "Iniciando Varredura..."),
        "price": getattr(engine, 'last_price', 0),
        "signal": getattr(engine, 'active_signal', None),
        "neural_stats": {
            "payout_active": "80%+",
            "scanning": True,
            "time_sync": "UTC"
        }
    })

if __name__ == "__main__":
    # A Render define automaticamente a porta na variável de ambiente PORT
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
