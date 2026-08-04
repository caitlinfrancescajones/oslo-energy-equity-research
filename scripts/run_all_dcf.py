from dcf_model import run_dcf
import pandas as pd

# Companies to value, with any manually-verified overrides
# (Equinor's beta and EBITDA were verified against real sources - see README)
companies = [
    {"ticker": "EQNR.OL", "name": "Equinor", "beta_override": 1.05, "ebitda_override": 350_000_000_000},
    {"ticker": "AKRBP.OL", "name": "Aker BP", "beta_override": 1.05, "ebitda_margin_override": 0.55},
    {"ticker": "VAR.OL", "name": "Vår Energi", "beta_override": 1.00, "ebitda_margin_override": 0.55},
    {"ticker": "SUBC.OL", "name": "Subsea7", "beta_override": 1.25, "ebitda_margin_override": 0.18},
    {"ticker": "AKSO.OL", "name": "Aker Solutions", "beta_override": 1.20, "ebitda_margin_override": 0.18},
    {"ticker": "ODL.OL", "name": "Odfjell Drilling", "beta_override": 1.30, "ebitda_override": 3_900_000_000},
    {"ticker": "AKER.OL", "name": "Aker ASA", "beta_override": 0.95, "ebitda_margin_override": 0.25},
]

results = []

for company in companies:
    print(f"Running DCF for {company['name']}...")
    try:
        result = run_dcf(
    ticker=company["ticker"],
    company_name=company["name"],
    beta_override=company.get("beta_override"),
    ebitda_override=company.get("ebitda_override"),
    ebitda_margin_override=company.get("ebitda_margin_override")
)
        results.append(result)
    except Exception as e:
        print(f"  ERROR valuing {company['name']}: {e}")

results_df = pd.DataFrame(results)
print("\n--- DCF Summary: All Companies ---")
print(results_df.to_string(index=False))

results_df.to_csv("outputs/dcf_summary_all_companies.csv", index=False)
print("\nSaved to outputs/dcf_summary_all_companies.csv")
