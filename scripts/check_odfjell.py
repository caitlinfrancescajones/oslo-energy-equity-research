import yfinance as yf

stock = yf.Ticker("ODL.OL")
info = stock.info

market_cap = info.get("marketCap")
total_debt = info.get("totalDebt")
cash = info.get("totalCash")
revenue = info.get("totalRevenue")

print(f"Market Cap: {market_cap:,.0f} NOK")
print(f"Total Debt: {total_debt:,.0f} NOK")
print(f"Total Cash: {cash:,.0f} NOK")
print(f"Revenue: {revenue:,.0f} NOK")

estimated_ebitda = revenue * 0.20  # the margin we assumed
print(f"\nEstimated EBITDA (20% margin assumption): {estimated_ebitda:,.0f} NOK")

print(f"\nDebt-to-Revenue ratio: {total_debt/revenue:.2f}x")
print(f"Debt-to-EBITDA ratio (estimated): {total_debt/estimated_ebitda:.2f}x")
