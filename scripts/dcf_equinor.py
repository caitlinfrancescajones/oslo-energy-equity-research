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

# --- Step 5: Free Cash Flow Projections ---

# NOTE: Yahoo's EBITDA figure (NOK 41.9B) was inconsistent with Equinor's
# reported 2025 adjusted operating income of USD 27.6B (~NOK 350B at
# ~10.3 NOK/USD, plus D&A). Using a manually sourced figure from Equinor's
# 2025 annual report instead.
ebitda = 350_000_000_000  # NOK 350B, based on 2025 annual report
print(f"\nCurrent EBITDA: {ebitda:,.0f} NOK")

# Assumptions (documented, defensible judgement calls)
revenue_growth_rate = 0.03   # 3% annual growth - conservative, mature E&P major
fcf_conversion = 0.55        # ~55% of EBITDA converts to FCF after capex/tax/D&A
                              # (typical range for capital-intensive E&P is 40-60%)
projection_years = 5

fcf_projections = []
current_ebitda = ebitda

print("\n--- FCF Projections ---")
for year in range(1, projection_years + 1):
    current_ebitda = current_ebitda * (1 + revenue_growth_rate)
    projected_fcf = current_ebitda * fcf_conversion
    fcf_projections.append(projected_fcf)
    print(f"Year {year}: EBITDA = {current_ebitda:,.0f} NOK | FCF = {projected_fcf:,.0f} NOK")

    # --- Step 6: Terminal Value (Exit Multiple Method) ---
# NOTE: Using exit multiple rather than Gordon Growth perpetuity. Oil & gas
# companies extract finite reserves, so assuming perpetual growth overstates
# terminal value. Equinor's actual observed EV/EBITDA is ~3x - using a
# slightly conservative-to-market 3.5x as the exit assumption.

exit_ev_ebitda_multiple = 3.5

terminal_ebitda = current_ebitda  # Year 5 EBITDA, already calculated above
terminal_value = terminal_ebitda * exit_ev_ebitda_multiple
print(f"\nTerminal Value (Exit Multiple Method): {terminal_value:,.0f} NOK")

# --- Step 7: Discount everything back to present value ---

pv_fcf = []
for year, fcf in enumerate(fcf_projections, start=1):
    discounted = fcf / ((1 + wacc) ** year)
    pv_fcf.append(discounted)

pv_terminal_value = terminal_value / ((1 + wacc) ** projection_years)

enterprise_value = sum(pv_fcf) + pv_terminal_value

print(f"\nSum of PV of FCF (Years 1-5): {sum(pv_fcf):,.0f} NOK")
print(f"PV of Terminal Value: {pv_terminal_value:,.0f} NOK")
print(f"\n--- Enterprise Value: {enterprise_value:,.0f} NOK ---")

# --- Step 8: Bridge to implied share price ---

total_debt_value = total_debt
cash = info.get("totalCash")
shares_outstanding = info.get("sharesOutstanding")

equity_value = enterprise_value - total_debt_value + cash
implied_share_price = equity_value / shares_outstanding

current_price = stock.history(period="1d")["Close"].iloc[-1]

print(f"\nEquity Value: {equity_value:,.0f} NOK")
print(f"Shares Outstanding: {shares_outstanding:,.0f}")
print(f"\n--- Implied Share Price: {implied_share_price:,.2f} NOK ---")
print(f"--- Current Market Price: {current_price:,.2f} NOK ---")

upside_downside = (implied_share_price / current_price - 1) * 100
print(f"--- Implied Upside/Downside: {upside_downside:+.2f}% ---")
