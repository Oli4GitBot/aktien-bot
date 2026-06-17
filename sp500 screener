#!/usr/bin/env python3
"""
S&P 500 Fundamentaldaten-Screener mit Telegram-Versand.

Ablauf:
1. Holt aktuelle S&P-500-Ticker-Liste von Wikipedia.
2. Zieht Fundamentaldaten je Ticker via yfinance.
3. Filtert Aktien, die ALLE Kriterien erfuellen.
4. Sendet Ergebnis als Telegram-Nachricht.

Gedacht fuer Ausfuehrung via Cron (z.B. taeglich nach Boersenschluss).

Benoetigte Pakete:
    pip install yfinance requests pandas lxml

Benoetigte Umgebungsvariablen (empfohlen statt Hardcoding):
    TELEGRAM_BOT_TOKEN
    TELEGRAM_CHAT_ID
"""

import os
import sys
import time
import logging
from dataclasses import dataclass, fields
from typing import Optional
from datetime import datetime
from zoneinfo import ZoneInfo

import requests
import pandas as pd
import yfinance as yf

# ---------------------------------------------------------------------------
# Konfiguration
# ---------------------------------------------------------------------------

LOG_LEVEL = os.environ.get("SCREENER_LOG_LEVEL", "INFO")
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("sp500_screener")

# Telegram-Zugangsdaten: bevorzugt aus Umgebungsvariablen lesen.
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

WIKIPEDIA_SP500_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

# Screening-Schwellenwerte (final abgestimmt)
THRESHOLDS = {
    "trailing_pe": {"op": "<", "value": 20},     # KGV
    "price_to_book": {"op": "<", "value": 3},    # KBV
    "roe": {"op": ">", "value": 0.15},           # ROE > 15%
    "net_margin": {"op": ">", "value": 0.10},    # Nettomarge > 10%
    "revenue_growth": {"op": ">", "value": 0.05},# Umsatzwachstum YoY > 5%
    "debt_to_equity": {"op": "<", "value": 1.5}, # Verschuldung (Verhaeltnis, nicht %)
}

# Pause zwischen einzelnen Ticker-Abfragen, um Yahoo-Finance-Rate-Limits zu vermeiden
REQUEST_DELAY_SECONDS = 0.5

# Telegram-Nachrichtenlimit (4096 Zeichen) -> Sicherheitsmarge
TELEGRAM_MAX_LEN = 3500


# ---------------------------------------------------------------------------
# DST-Check: Bei zwei Cron-Triggern (Sommer-/Winterzeit) nur den passenden ausfuehren
# ---------------------------------------------------------------------------

def is_correct_trigger_for_season() -> bool:
    """
    Workflow hat zwei Cron-Trigger (13:30 UTC fuer Sommerzeit, 14:30 UTC fuer
    Winterzeit), da Berlin und US Eastern Time an unterschiedlichen Tagen auf
    Sommerzeit umstellen. Diese Funktion verhindert Doppel-Laeufe, indem sie
    prueft, ob die aktuelle UTC-Stunde zur aktuellen Berlin-Zeitzone passt.

    Manuelle Trigger (workflow_dispatch) ueberspringen diese Pruefung immer,
    damit Tests jederzeit moeglich sind.

    Gibt False zurueck, wenn dies der "falsche" Trigger fuer die aktuelle
    Jahreszeit ist (Script bricht dann ohne Telegram-Versand ab).
    """
    if os.environ.get("GITHUB_EVENT_NAME") == "workflow_dispatch":
        return True

    now_utc = datetime.now(ZoneInfo("UTC"))
    now_berlin = now_utc.astimezone(ZoneInfo("Europe/Berlin"))

    berlin_utc_offset_hours = now_berlin.utcoffset().total_seconds() / 3600
    is_berlin_summer_time = berlin_utc_offset_hours == 2  # MESZ = UTC+2, MEZ = UTC+1

    current_utc_hour = now_utc.hour

    if is_berlin_summer_time:
        return current_utc_hour == 13  # Sommerzeit-Trigger erwartet
    else:
        return current_utc_hour == 14  # Winterzeit-Trigger erwartet



    ticker: str
    name: str
    trailing_pe: Optional[float] = None
    price_to_book: Optional[float] = None
    roe: Optional[float] = None
    net_margin: Optional[float] = None
    revenue_growth: Optional[float] = None
    debt_to_equity: Optional[float] = None  # yfinance liefert dies meist in % (z.B. 120.5 = 1.205)

    def missing_fields(self) -> list[str]:
        return [f.name for f in fields(self) if f.name not in ("ticker", "name") and getattr(self, f.name) is None]


# ---------------------------------------------------------------------------
# Schritt 1: S&P-500-Ticker von Wikipedia laden
# ---------------------------------------------------------------------------

def fetch_sp500_tickers() -> list[tuple[str, str]]:
    """Liefert Liste von (Ticker, Firmenname) Tupeln. Wirft Exception bei Fehler."""
    log.info("Lade S&P-500-Liste von Wikipedia...")
    tables = pd.read_html(WIKIPEDIA_SP500_URL)
    df = tables[0]  # Erste Tabelle enthaelt die Konstituenten

    if "Symbol" not in df.columns:
        raise ValueError("Wikipedia-Tabellenstruktur hat sich geaendert - 'Symbol'-Spalte fehlt.")

    # yfinance erwartet Punkt statt Bindestrich bei Tickern wie BRK.B
    df["Symbol"] = df["Symbol"].str.replace(".", "-", regex=False)

    name_col = "Security" if "Security" in df.columns else df.columns[1]
    tickers = list(zip(df["Symbol"].tolist(), df[name_col].tolist()))
    log.info(f"{len(tickers)} Ticker geladen.")
    return tickers


# ---------------------------------------------------------------------------
# Schritt 2: Fundamentaldaten je Ticker abrufen
# ---------------------------------------------------------------------------

def fetch_metrics(ticker: str, name: str) -> StockMetrics:
    """Holt Fundamentaldaten fuer einen einzelnen Ticker. Fehlende Werte bleiben None."""
    metrics = StockMetrics(ticker=ticker, name=name)
    try:
        info = yf.Ticker(ticker).info
    except Exception as e:
        log.warning(f"{ticker}: Fehler beim Abruf der Info-Daten: {e}")
        return metrics

    metrics.trailing_pe = info.get("trailingPE")
    metrics.price_to_book = info.get("priceToBook")
    metrics.roe = info.get("returnOnEquity")
    metrics.net_margin = info.get("profitMargins")
    metrics.revenue_growth = info.get("revenueGrowth")

    de = info.get("debtToEquity")
    # yfinance liefert debtToEquity meist als Prozentwert (z.B. 145.3 statt 1.453)
    metrics.debt_to_equity = de / 100 if de is not None else None

    return metrics


def fetch_all_metrics(tickers: list[tuple[str, str]]) -> list[StockMetrics]:
    results = []
    total = len(tickers)
    for i, (ticker, name) in enumerate(tickers, start=1):
        log.info(f"[{i}/{total}] Verarbeite {ticker}...")
        results.append(fetch_metrics(ticker, name))
        time.sleep(REQUEST_DELAY_SECONDS)
    return results


# ---------------------------------------------------------------------------
# Schritt 3: Filterlogik
# ---------------------------------------------------------------------------

def passes_all_criteria(m: StockMetrics) -> bool:
    """True nur wenn ALLE Kriterien erfuellt sind UND alle benoetigten Werte vorhanden sind."""
    if m.missing_fields():
        return False  # Unvollstaendige Daten -> konservativ ausschliessen, keine Annahmen

    checks = [
        m.trailing_pe < THRESHOLDS["trailing_pe"]["value"] and m.trailing_pe > 0,
        m.price_to_book < THRESHOLDS["price_to_book"]["value"] and m.price_to_book > 0,
        m.roe > THRESHOLDS["roe"]["value"],
        m.net_margin > THRESHOLDS["net_margin"]["value"],
        m.revenue_growth > THRESHOLDS["revenue_growth"]["value"],
        m.debt_to_equity < THRESHOLDS["debt_to_equity"]["value"],
    ]
    return all(checks)


def run_screening(all_metrics: list[StockMetrics]) -> tuple[list[StockMetrics], int]:
    """Gibt (gefilterte Liste, Anzahl mit unvollstaendigen Daten) zurueck."""
    incomplete_count = sum(1 for m in all_metrics if m.missing_fields())
    passed = [m for m in all_metrics if passes_all_criteria(m)]
    return passed, incomplete_count


# ---------------------------------------------------------------------------
# Schritt 4: Nachricht formatieren
# ---------------------------------------------------------------------------

def format_message(passed: list[StockMetrics], total_checked: int, incomplete_count: int) -> str:
    from datetime import date

    header = (
        f"📊 *S&P 500 Fundamental-Screening* — {date.today().isoformat()}\n"
        f"Geprueft: {total_checked} | Unvollst. Daten: {incomplete_count} | Treffer: {len(passed)}\n"
        f"Kriterien: KGV<20, KBV<3, ROE>15%, NettoM>10%, Wachstum>5%, D/E<1.5\n\n"
    )

    if not passed:
        return header + "Keine Aktie erfuellt heute alle Kriterien."

    lines = []
    for m in passed:
        lines.append(
            f"*{m.ticker}* — {m.name}\n"
            f"  KGV {m.trailing_pe:.1f} | KBV {m.price_to_book:.2f} | "
            f"ROE {m.roe*100:.1f}% | NettoM {m.net_margin*100:.1f}%\n"
            f"  Wachstum {m.revenue_growth*100:.1f}% | D/E {m.debt_to_equity:.2f}"
        )
    body = "\n\n".join(lines)
    return header + body


def split_message(text: str, max_len: int = TELEGRAM_MAX_LEN) -> list[str]:
    """Teilt zu lange Nachrichten an Absatzgrenzen, um Telegrams 4096-Zeichen-Limit einzuhalten."""
    if len(text) <= max_len:
        return [text]

    chunks = []
    current = ""
    for paragraph in text.split("\n\n"):
        if len(current) + len(paragraph) + 2 > max_len:
            if current:
                chunks.append(current)
            current = paragraph
        else:
            current = f"{current}\n\n{paragraph}" if current else paragraph
    if current:
        chunks.append(current)
    return chunks


# ---------------------------------------------------------------------------
# Schritt 5: Telegram-Versand
# ---------------------------------------------------------------------------

def send_telegram_message(text: str) -> None:
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN oder TELEGRAM_CHAT_ID nicht gesetzt. "
            "Bitte als Umgebungsvariablen definieren."
        )

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    for chunk in split_message(text):
        response = requests.post(
            url,
            data={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": chunk,
                "parse_mode": "Markdown",
            },
            timeout=15,
        )
        if response.status_code != 200:
            log.error(f"Telegram-Versand fehlgeschlagen: {response.status_code} {response.text}")
            response.raise_for_status()
        time.sleep(0.3)  # kleine Pause zwischen mehreren Nachrichten-Teilen


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    if not is_correct_trigger_for_season():
        log.info(
            "Falscher Cron-Trigger fuer aktuelle Jahreszeit (Sommer-/Winterzeit-Doppeltrigger). "
            "Ueberspringe Lauf, kein Telegram-Versand."
        )
        return 0

    try:
        tickers = fetch_sp500_tickers()
    except Exception as e:
        log.error(f"Konnte S&P-500-Liste nicht laden: {e}")
        try:
            send_telegram_message(f"⚠️ Screening fehlgeschlagen: Ticker-Liste konnte nicht geladen werden.\n{e}")
        except Exception:
            pass
        return 1

    all_metrics = fetch_all_metrics(tickers)
    passed, incomplete_count = run_screening(all_metrics)

    message = format_message(passed, total_checked=len(all_metrics), incomplete_count=incomplete_count)
    log.info(f"Screening abgeschlossen: {len(passed)} Treffer von {len(all_metrics)} geprueften Aktien.")

    try:
        send_telegram_message(message)
    except Exception as e:
        log.error(f"Telegram-Versand fehlgeschlagen: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
