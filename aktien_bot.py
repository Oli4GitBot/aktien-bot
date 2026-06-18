import requests
import yfinance as yf
from datetime import datetime
import os

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

AKTIEN = {
    "Apple": "AAPL",
    "ASML": "ASML",
    "Zalando": "ZAL.DE",
    "Lanxess": "LXS.DE",
    "Microsoft": "MSFT",
    "Bayer": "BAYN.DE"
}

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

def get_news(ticker):
    try:
        stock = yf.Ticker(ticker)
        news = stock.news
        if not news:
            return []
        recent = []
        for item in news[:3]:
            title = item.get("content", {}).get("title", "")
            link = item.get("content", {}).get("canonicalUrl", {}).get("url", "")
            if title:
                recent.append(f"  📰 [{title}]({link})")
        return recent
    except:
        return []

def get_kurs(name, ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.fast_info
        preis = round(info.last_price, 2)
        prev_close = round(info.previous_close, 2)
        change = round(preis - prev_close, 2)
        change_pct = round((change / prev_close) * 100, 2)
        waehrung = info.currency
        pfeil = "📈" if change >= 0 else "📉"
        vorzeichen = "+" if change >= 0 else ""
        nachricht = (
            f"{pfeil} *{name}* ({ticker})\n"
            f"  Kurs: {preis} {waehrung}\n"
            f"  Änderung: {vorzeichen}{change} ({vorzeichen}{change_pct}%)\n"
        )
        news = get_news(ticker)
        if news:
            nachricht += "  📋 Meldungen:\n" + "\n".join(news) + "\n"
        return nachricht
    except Exception as e:
        return f"⚠️ *{name}* ({ticker}): Fehler ({e})\n"

def main():
    heute = datetime.now().strftime("%d.%m.%Y")
    nachricht = f"📊 *Tägliche Aktien-Info – {heute}*\n\n"
    for name, ticker in AKTIEN.items():
        nachricht += get_kurs(name, ticker) + "\n"
    send_telegram(nachricht)
    print("Nachricht gesendet.")

if __name__ == "__main__":
    main()
