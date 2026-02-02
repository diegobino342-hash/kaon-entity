import requests
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

def send_signal(signal):
    text = (
        f"📡 KAON SIGNAL\n"
        f"Par: {signal['asset']}\n"
        f"Ação: {signal['action']}\n"
        f"Probabilidade: {int(signal['prob']*100)}%"
    )
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": text})
