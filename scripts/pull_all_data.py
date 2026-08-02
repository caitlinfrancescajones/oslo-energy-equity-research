import yfinance as yf
import pandas as pd

# Oslo Børs Energy sector - organized by sub-sector
tickers = {
    # E&P (exploration and production)
    "EQNR.OL": "Equinor",
    "AKRBP.OL": "Aker BP",
    "VAR.OL": "Vår Energi",

    # Oilfield services
    "SUBC.OL": "Subsea7",
    "AKSO.OL": "Aker Solutions",
    "ODL.OL": "Odfjell Drilling",

    # Holding company
    "AKER.OL": "Aker ASA"
}

all_data = {}

for ticker, name in tickers.items():
    print(f"Pulling data for {name} ({ticker})...")
    stock = yf.Ticker(ticker)
    history = stock.history(period="1mo")

    if history.empty:
        print(f"  WARNING: No data returned for {ticker} - check the ticker symbol")
        continue

    all_data[name] = history
    history.to_csv(f"data/{ticker.replace('.OL', '')}_prices.csv")

print("Done. Check the data/ folder for CSV files.")
