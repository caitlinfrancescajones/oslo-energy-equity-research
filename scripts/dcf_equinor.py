import yfinance as yf

# --- Step 1: Pull the data we need ---
ticker = "EQNR.OL"
stock = yf.Ticker(ticker)
info = stock.info

market_cap = info.get("marketCap")
total_debt = info.get("totalDebt")

# NOTE: Yahoo's beta figure for EQNR was unreliable (varied from -0.67 to 1.89
# across data providers). Using a manually researched, sector-standard beta
# for an integrated energy major instead.
beta = 1.05

print(f"Market Cap: {market_cap:,.0f} NOK")
print(f"Total Debt: {total_debt:,.0f} NOK")
print(f"Beta (manual assumption): {beta}")

# --- Step 2: Assumptions (you set these based on research/judgement) ---
risk_free_rate = 0.035      # ~3.5%, roughly Norwegian 10-year govt bond yield
market_risk_premium = 0.055  # ~5.5%, standard equity risk premium assumption
cost_of_debt = 0.045        # ~4.5%, approximate borrowing rate
tax_rate = 0.22             # Norway standard corporate tax rate

# --- Step 3: Cost of equity (CAPM) ---
cost_of_equity = risk_free_rate + beta * market_risk_premium
print(f"\nCost of Equity (CAPM): {cost_of_equity:.4f} ({cost_of_equity*100:.2f}%)")

# --- Step 4: WACC ---
total_value = market_cap + total_debt
equity_weight = market_cap / total_value
debt_weight = total_debt / total_value

wacc = (equity_weight * cost_of_equity) + (debt_weight * cost_of_debt * (1 - tax_rate))
print(f"\nEquity Weight: {equity_weight:.2%}")
print(f"Debt Weight: {debt_weight:.2%}")
print(f"WACC: {wacc:.4f} ({wacc*100:.2f}%)")
