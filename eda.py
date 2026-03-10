import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

os.makedirs("outputs", exist_ok=True)

df = pd.read_csv("data/hydropower_data.csv", parse_dates=["datetime"])
print("✅ Data Loaded:", df.shape)
print(df.describe())

# ── Plot 1: River Flow vs Power Output (1 Month) ──────────────────
fig, ax1 = plt.subplots(figsize=(14, 5))
month_data = df.head(720)
ax1.plot(month_data["datetime"], month_data["river_flow"],
         color="#00B4D8", linewidth=2, label="River Flow (m³/s)")
ax1.set_ylabel("River Flow (m³/s)", color="#00B4D8")
ax2 = ax1.twinx()
ax2.plot(month_data["datetime"], month_data["power_output"],
         color="#FFB703", linewidth=2, label="Power Output (MW)")
ax2.set_ylabel("Power Output (MW)", color="#FFB703")
ax1.set_title("River Flow vs Power Output (1 Month)", fontsize=14, fontweight="bold")
fig.legend(loc="upper right")
ax1.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("outputs/flow_vs_power.png", dpi=150)
plt.show()
print("✅ Plot 1 saved")

# ── Plot 2: Monthly Average Power Output ─────────────────────────
monthly = df.groupby("month")[["river_flow", "power_output", "rainfall"]].mean()
fig, ax = plt.subplots(figsize=(10, 5))
x = np.arange(12)
w = 0.35
ax.bar(x - w/2, monthly["river_flow"], width=w, label="River Flow (m³/s)", color="#00B4D8")
ax.bar(x + w/2, monthly["power_output"], width=w, label="Power Output (MW)", color="#FFB703")
ax.set_xticks(x)
ax.set_xticklabels(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])
ax.set_title("Monthly Average River Flow & Power Output", fontsize=14, fontweight="bold")
ax.set_ylabel("Value")
ax.legend()
ax.grid(True, alpha=0.3, axis="y")
plt.tight_layout()
plt.savefig("outputs/monthly_power.png", dpi=150)
plt.show()
print("✅ Plot 2 saved")

# ── Plot 3: Correlation Heatmap ───────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 6))
cols = ["river_flow", "rainfall", "temperature", "reservoir_level", "power_output"]
corr = df[cols].corr()
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax, square=True, linewidths=0.5)
ax.set_title("Feature Correlation Heatmap", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("outputs/correlation_heatmap.png", dpi=150)
plt.show()
print("✅ Plot 3 saved")

# ── Plot 4: Rainfall vs River Flow ────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 5))
ax.scatter(df["rainfall"], df["river_flow"], alpha=0.3, color="#06D6A0", s=10)
ax.set_title("Rainfall vs River Flow", fontsize=14, fontweight="bold")
ax.set_xlabel("Rainfall (mm)")
ax.set_ylabel("River Flow (m³/s)")
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("outputs/rainfall_vs_flow.png", dpi=150)
plt.show()
print("✅ Plot 4 saved")
print("\n✅ EDA Complete! All plots saved in outputs/")
