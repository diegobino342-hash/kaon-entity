const canvas = document.getElementById('live-chart');
const ctx = canvas.getContext('2d');
const beep = document.getElementById('beep-alert');

let priceHistory = [];

function updateDashboard() {
    fetch('/status')
        .then(response => response.json())
        .then(data => {
            document.getElementById('symbol').innerText = data.pair;
            
            // Atualiza Histórico do Gráfico
            if (data.price) {
                priceHistory.push(data.price);
                if (priceHistory.length > 50) priceHistory.shift();
                drawChart();
            }

            // Lógica de Sinal Visual e Sonoro
            const overlay = document.getElementById('signal-overlay');
            if (data.signal && data.signal.active) {
                document.getElementById('signal-dir').innerText = data.signal.direction;
                document.getElementById('signal-dir').className = data.signal.direction.toLowerCase();
                overlay.classList.remove('hidden');
                beep.play(); // Alerta Sonoro de Alta Frequência
            } else {
                overlay.classList.add('hidden');
            }
        });
}

function drawChart() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.beginPath();
    ctx.strokeStyle = '#00ff41'; // Verde Matrix
    ctx.lineWidth = 2;
    
    const step = canvas.width / 50;
    priceHistory.forEach((p, i) => {
        const x = i * step;
        const y = canvas.height - ((p % 1) * 1000); // Escala dinâmica
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
    });
    ctx.stroke();
}

setInterval(updateDashboard, 1000); // Atualização a cada 1 segundo
