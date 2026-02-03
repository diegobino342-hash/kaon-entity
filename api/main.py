from flask import Flask, jsonify
from flask_cors import CORS
from engine import KaonEngine
import threading

app = Flask(__name__)
CORS(app)

# Inicia o motor neural em uma thread separada para rodar 24h
engine = KaonEngine()
threading.Thread(target=engine.run_sync, daemon=True).start()

@app.route('/status')
def get_status():
    # Retorna o par atual, o gráfico e se há sinal
    return jsonify({
        "pair": engine.current_pair,
        "price": engine.last_price,
        "signal": engine.active_signal,
        "learning_stats": engine.memory.get_stats()
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
