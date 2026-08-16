"""
Investmenthypothesen-Alerting.

Prüft die in theses.yml hinterlegten Stop-Loss-, Kursziel- und Review-Schwellen
gegen die aktuellen Kurse (yfinance) und verschickt NUR bei mindestens einem
Treffer eine Telegram-Nachricht – kein täglicher Spam wie bei aktien_bot.py.

Wichtig: Es wird keine automatische Bewertung von News gegen die Kipp-Kriterien
vorgenommen (zu unzuverlässig). Bei einem Alert werden die hinterlegten
Kipp-Kriterien nur als Erinnerungstext mitgeschickt – die Einschätzung bleibt
bei dir.

Verhalten bewusst zustandslos: Solange eine gerissene Schwelle (Stop-Loss,
Kursziel, Review fällig) nicht durch eine Anpassung von theses.yml "quittiert"
wird, meldet sich der Bot bei jedem Lauf erneut. Das ist gewollt (Erinnerung,
bis reagiert wurde), nicht einmalig.

Quelle der Thesen: von Claude aus "investments von claude/<TICKER>_Investmenthypothese.txt"
übernommen. Bei Aktualisierung: theses.yml von Hand anpassen oder Claude Bescheid geben.
"""

import os
from datetime import date, datetime

import requests
import yaml
import yfinance as yf

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

THESES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "theses.yml")


def load_theses():
    with open(THESES_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    resp = requests.post(url, json=payload, timeout=15)
    if resp.status_code != 200:
        print(f"Telegram-Versand fehlgeschlagen: {resp.status_code} {resp.text}")
        resp.raise_for_status()


def get_news(ticker, count=2):
    try:
        stock = yf.Ticker(ticker)
        news = stock.news
        if not news:
            return []
        recent = []
        for item in news[:count]:
            title = item.get("content", {}).get("title", "")
            link = item.get("content", {}).get("canonicalUrl", {}).get("url", "")
            if title:
                recent.append(f"  📰 [{title}]({link})")
        return recent
    except Exception:
        return []


def check_position(ticker, cfg):
    """Prüft eine Position gegen ihre Schwellenwerte. Gibt (triggers, kurs, waehrung) zurück."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.fast_info
        preis = round(info.last_price, 2)
        waehrung = info.currency
    except Exception as e:
        return [f"⚠️ Kurs konnte nicht geladen werden ({e})"], None, None

    triggers = []

    stop_loss = cfg.get("stop_loss")
    if stop_loss is not None and preis <= stop_loss:
        triggers.append(f"🛑 Stop-Loss erreicht/unterschritten: {preis} {waehrung} ≤ {stop_loss} {waehrung}")

    for tp in (cfg.get("take_profit") or []):
        if preis >= tp:
            triggers.append(f"🎯 Kursziel erreicht/überschritten: {preis} {waehrung} ≥ {tp} {waehrung}")

    last_review = cfg.get("last_review")
    review_interval = cfg.get("review_interval_days")
    if last_review and review_interval:
        last_review_date = datetime.strptime(str(last_review), "%Y-%m-%d").date()
        days_since = (date.today() - last_review_date).days
        if days_since >= review_interval:
            triggers.append(
                f"🔁 Review fällig: letzte Prüfung vor {days_since} Tagen (Intervall: {review_interval} Tage)"
            )

    return triggers, preis, waehrung


def format_alert(ticker, cfg, triggers, preis, waehrung):
    name = cfg.get("name", ticker)
    lines = [f"🔔 *{name}* ({ticker})"]
    if preis is not None:
        lines.append(f"  Aktueller Kurs: {preis} {waehrung}")
    for t in triggers:
        lines.append(f"  {t}")

    kill_kriterien = cfg.get("kill_kriterien") or []
    if kill_kriterien:
        lines.append("  ⚠️ Was die These kippen würde (Erinnerung, keine automatische Bewertung):")
        for k in kill_kriterien:
            lines.append(f"    • {k}")

    catalyst_label = cfg.get("next_catalyst_label")
    catalyst_date = cfg.get("next_catalyst")
    if catalyst_label and catalyst_date:
        lines.append(f"  📅 Nächster Katalysator: {catalyst_label} ({catalyst_date})")

    news = get_news(ticker)
    if news:
        lines.append("  📋 Aktuelle Meldungen:")
        lines.extend(news)

    return "\n".join(lines)


def main():
    theses = load_theses()
    if not theses:
        print("Keine Thesen in theses.yml gefunden.")
        return

    heute = date.today().strftime("%d.%m.%Y")
    alerts = []

    for ticker, cfg in theses.items():
        triggers, preis, waehrung = check_position(ticker, cfg)
        if triggers:
            alerts.append(format_alert(ticker, cfg, triggers, preis, waehrung))

    if not alerts:
        print(f"{heute}: Keine Auffälligkeiten – kein Versand.")
        return

    nachricht = f"📊 *Investmenthypothesen-Alert – {heute}*\n\n" + "\n\n".join(alerts)
    send_telegram(nachricht)
    print(f"{heute}: {len(alerts)} Alert(s) gesendet.")


if __name__ == "__main__":
    main()
