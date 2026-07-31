import yfinance as yf

equinor = yf.Ticker("EQNR.OL")
data = equinor.history(period="5d")
print(data)
