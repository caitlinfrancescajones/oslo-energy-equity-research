import yfinance as yf
import pandas as pd

tickers = {
    "EQNR.OL": "Equinor",
    "AKRBP.OL": "Aker BP",
    "VAR.OL": "Vår Energi",
    "SUBC.OL": "Subsea7",
    "AKSO.OL": "Aker Solutions",
    "ODL.OL": "Odfjell Drilling",
    "AKER.OL": "Aker ASA"
}

fundamentals_list = []

for ticker, name in tickers.items():
    print(f"Pulling fundamentals for {name} ({ticker})...")
    stock = yf.Ticker(ticker)
    info = stock.info

    fundamentals_list.append({
        "Company": name,
        "Ticker": ticker,
        "Market Cap": info.get("marketCap"),
        "Total Revenue": info.get("totalRevenue"),
        "EBITDA": info.get("ebitda"),
        "Total Debt": info.get("totalDebt"),
        "Total Cash": info.get("totalCash"),
        "Shares Outstanding": info.get("sharesOutstanding"),
        "P/E Ratio": info.get("trailingPE"),
        "Beta": info.get("beta")
    })

fundamentals_df = pd.DataFrame(fundamentals_list)
fundamentals_df.to_csv("data/fundamentals_summary.csv", index=False)

print(fundamentals_df)
print("\nDone. Saved to data/fundamentals_summary.csv")
