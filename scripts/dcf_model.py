import yfinance as yf

def run_dcf(ticker, company_name, beta_override=None, ebitda_override=None,
            ebitda_margin_override=None,
            growth_rate=0.03, fcf_conversion=0.55, exit_multiple=3.5,
            risk_free_rate=0.035, market_risk_premium=0.055,
            cost_of_debt=0.045, tax_rate=0.22, projection_years=5):
    """
    Runs a simplified DCF valuation for a given ticker.
    Returns a dictionary of key results.
    """
    stock = yf.Ticker(ticker)
    info = stock.info

    market_cap = info.get("marketCap")
    total_debt = info.get("totalDebt") or 0
    cash = info.get("totalCash") or 0
    shares_outstanding = info.get("sharesOutstanding")

    # Use manual override if provided, otherwise fall back to Yahoo's figure
    # (documented data-quality issue: Yahoo's beta/EBITDA have proven unreliable
    # for some Oslo Børs stocks - see README for details)
    beta = beta_override if beta_override is not None else info.get("beta")
    if ebitda_override is not None:
        ebitda = ebitda_override
    elif ebitda_margin_override is not None:
        revenue = info.get("totalRevenue")
        ebitda = revenue * ebitda_margin_override
    else:
        ebitda = info.get("ebitda")

    # --- WACC ---
    cost_of_equity = risk_free_rate + beta * market_risk_premium
    total_value = market_cap + total_debt
    equity_weight = market_cap / total_value
    debt_weight = total_debt / total_value
    wacc = (equity_weight * cost_of_equity) + (debt_weight * cost_of_debt * (1 - tax_rate))

    # --- FCF Projections ---
    fcf_projections = []
    current_ebitda = ebitda
    for year in range(1, projection_years + 1):
        current_ebitda = current_ebitda * (1 + growth_rate)
        fcf_projections.append(current_ebitda * fcf_conversion)

    # --- Terminal Value (exit multiple method) ---
    terminal_value = current_ebitda * exit_multiple

    # --- Discount to present value ---
    pv_fcf = [fcf / ((1 + wacc) ** year) for year, fcf in enumerate(fcf_projections, start=1)]
    pv_terminal_value = terminal_value / ((1 + wacc) ** projection_years)
    enterprise_value = sum(pv_fcf) + pv_terminal_value

    # --- Bridge to implied share price ---
    equity_value = enterprise_value - total_debt + cash
    implied_share_price = equity_value / shares_outstanding
    current_price = stock.history(period="1d")["Close"].iloc[-1]
    upside_downside = (implied_share_price / current_price - 1) * 100

    return {
        "Company": company_name,
        "Ticker": ticker,
        "Beta Used": beta,
        "WACC": round(wacc * 100, 2),
        "Enterprise Value (NOK)": round(enterprise_value, 0),
        "Implied Share Price": round(implied_share_price, 2),
        "Current Market Price": round(current_price, 2),
        "Upside/Downside (%)": round(upside_downside, 2)
    }
