import pandas as pd
import numpy as np
import os

os.makedirs("data", exist_ok=True)

np.random.seed(42)
n = 8760  # 1 year hourly data

dates = pd.date_range(start="2023-01-01", periods=n, freq="h")
month = dates.month
hour = dates.hour

# Simulate river flow (m³/s) — higher in monsoon season
river_flow = np.abs(
    200 + 150 * np.sin(2 * np.pi * (month - 6) / 12)
    + np.random.normal(0, 20, n)
)

# Simulate rainfall (mm)
rainfall = np.abs(
    50 * np.sin(2 * np.pi * (month - 6) / 12)
    + np.random.normal(0, 10, n)
)

# Simulate temperature
temperature = 25 + 8 * np.sin(2 * np.pi * (month - 3) / 12) + np.random.normal(0, 2, n)

# Simulate reservoir water level (m)
reservoir_level = np.abs(
    50 + 20 * np.sin(2 * np.pi * (month - 6) / 12)
    + np.random.normal(0, 5, n)
)

# Hydropower formula: P = η × ρ × g × Q × H
# η=0.85, ρ=1000, g=9.81
eta = 0.85
rho = 1000
g = 9.81
power_output = np.clip(
    (eta * rho * g * river_flow * reservoir_level) / 1e6
    + np.random.normal(0, 5, n),
    0, None
)

df = pd.DataFrame({
    "datetime": dates,
    "month": month,
    "hour": hour,
    "river_flow": river_flow.round(2),
    "rainfall": rainfall.round(2),
    "temperature": temperature.round(2),
    "reservoir_level": reservoir_level.round(2),
    "power_output": power_output.round(2),
})

df.to_csv("data/hydropower_data.csv", index=False)
print(f"✅ Dataset created: {df.shape[0]} rows, {df.shape[1]} columns")
print(df.head())
