async function update() {
  const r = await fetch("/signal");
  const d = await r.json();
  if (d.direction) {
    document.getElementById("signal").innerText =
      `${d.direction} ${d.probability*100}%`;

    speechSynthesis.speak(
      new SpeechSynthesisUtterance(
        `Sinal de ${d.direction}`
      )
    );
  }
}
setInterval(update, 3000);
