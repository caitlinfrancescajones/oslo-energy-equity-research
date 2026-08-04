import pandas as pd
import matplotlib.pyplot as plt

# Load the results we already calculated
df = pd.read_csv("outputs/dcf_summary_all_companies.csv")

# Sort by upside/downside for a cleaner visual story
df = df.sort_values("Upside/Downside (%)")

fig, ax = plt.subplots(figsize=(10, 6))

colors = ["#d62728" if x < 0 else "#2ca02c" for x in df["Upside/Downside (%)"]]
bars = ax.barh(df["Company"], df["Upside/Downside (%)"], color=colors)

ax.axvline(0, color="black", linewidth=0.8)
ax.set_xlabel("Implied Upside / Downside vs. Market Price (%)")
ax.set_title("DCF-Implied Valuation vs. Market Price\nOslo Børs Energy Sector")

# Add value labels on each bar
for bar, value in zip(bars, df["Upside/Downside (%)"]):
    label_x = value + (2 if value >= 0 else -2)
    ha = "left" if value >= 0 else "right"
    ax.text(label_x, bar.get_y() + bar.get_height()/2, f"{value:.1f}%",
            va="center", ha=ha, fontsize=9)

plt.tight_layout()
plt.savefig("outputs/dcf_upside_downside_chart.png", dpi=150)
print("Chart saved to outputs/dcf_upside_downside_chart.png")

plt.show()
