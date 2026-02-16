"""
Simple script to fetch daily price data using yfinance and save CSVs to data/raw.
Usage:
    python scripts/fetch_stock_data.py --tickers RELIANCE.NS BNS.TO --period 1y

Default tickers include example Indian and Canadian symbols.
"""
import argparse
from pathlib import Path
import yfinance as yf

OUT_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def fetch_and_save(ticker: str, period: str = "1y", interval: str = "1d"):
    print(f"Fetching {ticker} ({period}, {interval})...")
    t = yf.Ticker(ticker)
    df = t.history(period=period, interval=interval)
    if df.empty:
        print(f"Warning: no data for {ticker}")
        return
    path = OUT_DIR / f"{ticker}.csv"
    df.to_csv(path)
    print(f"Saved {path}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--tickers", nargs="+", default=["RELIANCE.NS", "INFY.NS", "BNS.TO"], help="Tickers to fetch")
    p.add_argument("--period", default="1y", help="Period to fetch (e.g., 1y, 6mo)")
    p.add_argument("--interval", default="1d", help="Data interval (e.g., 1d, 1wk)")
    args = p.parse_args()

    for tk in args.tickers:
        try:
            fetch_and_save(tk, period=args.period, interval=args.interval)
        except Exception as e:
            print(f"Error fetching {tk}: {e}")
