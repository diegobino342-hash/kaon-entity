const chart = LightweightCharts.createChart(
  document.getElementById("chart"),
  {
    layout: {
      background: { color: '#0b0b0b' },
      textColor: '#00ffcc',
    },
    grid: {
      vertLines: { color: '#1f1f1f' },
      horzLines: { color: '#1f1f1f' },
    },
    timeScale: {
      timeVisible: true,
      secondsVisible: false,
    },
  }
);

const candleSeries = chart.addCandlestickSeries({
  upColor: '#00ff00',
  downColor: '#ff0040',
  borderUpColor: '#00ff00',
  borderDownColor: '#ff0040',
  wickUpColor: '#00ff00',
  wickDownColor: '#ff0040',
});

async function update() {
  const candlesRes = await fetch("/candles");
  const candles = await candlesRes.json();

  const formatted = candles.map(c => ({
    time: c.bucket,
    open: c.open,
    high: c.high,
    low: c.low,
    close: c.close
  }));

  candleSeries.setData(formatted);

  const signalRes = await fetch("/signal");
  const signal = await signalRes.json();

  if (signal.direction) {
    const text = `${signal.symbol} | ${signal.direction} | ${signal.probability}%`;
    document.getElementById("signal").innerText = text;

    speechSynthesis.cancel();
    speechSynthesis.speak(
      new SpeechSynthesisUtterance(
        `Sinal de ${signal.direction} com probabilidade ${signal.probability} por cento`
      )
    );
  }
}

setInterval(update, 2000);
