from dcf_model import run_dcf
from datetime import date
today = date.today().strftime("%B %d, %Y")

# Run the DCF for Equinor (our most rigorously verified company)
result = run_dcf(
    ticker="EQNR.OL",
    company_name="Equinor",
    beta_override=1.05,
    ebitda_override=350_000_000_000
)

# Determine direction language for the write-up
direction = "undervalued" if result["Upside/Downside (%)"] > 0 else "overvalued"

html_content = f"""
<!DOCTYPE html>
<html>
<head>
<style>
    body {{ font-family: Georgia, serif; max-width: 700px; margin: 40px auto; color: #1a1a1a; }}
    h1 {{ font-size: 24px; border-bottom: 3px solid #1a1a1a; padding-bottom: 8px; }}
    h2 {{ font-size: 16px; margin-top: 30px; color: #333; }}
    .meta {{ color: #666; font-size: 13px; margin-bottom: 20px; }}
    .metric-table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
    .metric-table td {{ padding: 8px; border-bottom: 1px solid #ddd; }}
    .metric-table td:first-child {{ font-weight: bold; width: 60%; }}
    .risk-list {{ line-height: 1.8; }}
    .disclaimer {{ font-size: 11px; color: #999; margin-top: 40px; border-top: 1px solid #ddd; padding-top: 15px; }}
</style>
</head>
<body>

<h1>{result['Company']} ({result['Ticker']})</h1>
<div class="meta">Equity Research Note | Oslo Børs Energy Sector | Author: Caitlin Francesca Jones | Generated: {today}</div>

<h2>Investment Thesis</h2>
<p>
Equinor is Norway's largest integrated energy company, with a mature and cash-generative
North Sea production base alongside a growing renewables portfolio. Our DCF model, using
a WACC of {result['WACC']}% and conservative long-term production growth assumptions,
implies a valuation range meaningfully different from the current market price, suggesting the market may be pricing in risks (commodity volatility, energy transition exposure) not fully captured by this simplified model.
</p>

<h2>Valuation Summary</h2>
<table class="metric-table">
<tr><td>WACC</td><td>{result['WACC']}%</td></tr>
<tr><td>Enterprise Value</td><td>{result['Enterprise Value (NOK)']:,.0f} NOK</td></tr>
<tr><td>Implied Share Price</td><td>{result['Implied Share Price']:,.2f} NOK</td></tr>
<tr><td>Current Market Price</td><td>{result['Current Market Price']:,.2f} NOK</td></tr>
<tr><td>Implied Upside/Downside</td><td>{result['Upside/Downside (%)']:+.2f}%</td></tr>
</table>

<h2>Key Risks</h2>
<ul class="risk-list">
<li><strong>Commodity price exposure:</strong> Cash flows are highly sensitive to oil and gas prices, which are volatile and largely outside company control.</li>
<li><strong>Energy transition risk:</strong> Long-term demand for fossil fuels faces structural pressure from decarbonization policy and renewable adoption.</li>
<li><strong>Norwegian tax regime:</strong> The special petroleum tax (marginal rate ~78%) materially affects after-tax cash flow relative to standard corporate tax assumptions.</li>
<li><strong>Model limitations:</strong> Beta and EBITDA inputs required manual correction due to unreliable third-party data (see Methodology).</li>
</ul>

<h2>Methodology Notes</h2>
<p>
This valuation uses a simplified unlevered DCF: WACC via CAPM, five-year FCF projections
using a conservative 3% growth assumption, and an exit-multiple terminal value (3.5x EBITDA,
reflecting Equinor's observed market multiple) rather than a perpetuity growth model, given
the finite-reserve nature of oil and gas extraction. Beta and EBITDA figures required manual
verification against Equinor's 2025 annual report, as Yahoo Finance's automated data proved
unreliable for both metrics. This is a personal, educational valuation exercise using simplified assumptions and a small
number of manually-verified inputs. It should not be read as a professional research
recommendation or a claim about fair value — it is intended to demonstrate methodology and
judgement, not to predict the "correct" price.
</p>

<div class="disclaimer">
This research note was produced as part of a personal equity research project and does not
constitute investment advice. Figures are based on a simplified model with stated assumptions
and publicly available data as of the date of analysis.
</div>

</body>
</html>
"""

with open("outputs/equinor_research_note.html", "w") as f:
    f.write(html_content)

print("Research note saved to outputs/equinor_research_note.html")
