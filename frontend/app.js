async function updateSignal() {
  const res = await fetch("/signal");
  const data = await res.json();

  if (data.direction) {
    const text = `${data.symbol} | ${data.direction} | ${data.probability}%`;
    document.getElementById("signal").innerText = text;

    speechSynthesis.speak(
      new SpeechSynthesisUtterance(
        `Sinal de ${data.direction} com probabilidade ${data.probability} por cento`
      )
    );
  }
}

setInterval(updateSignal, 3000);
