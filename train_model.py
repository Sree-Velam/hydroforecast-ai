import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from xgboost import XGBRegressor
import joblib
import os

os.makedirs("models", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

# ── Load Data ─────────────────────────────────────────────────────
df = pd.read_csv("data/hydropower_data.csv", parse_dates=["datetime"])
print("✅ Data loaded:", df.shape)

# ── Feature Engineering ───────────────────────────────────────────
df["lag_1"] = df["river_flow"].shift(1)
df["lag_24"] = df["river_flow"].shift(24)
df["lag_168"] = df["river_flow"].shift(168)
df["rolling_mean_24"] = df["river_flow"].rolling(24).mean()
df["rolling_mean_168"] = df["river_flow"].rolling(168).mean()
df.dropna(inplace=True)

features = ["river_flow", "rainfall", "temperature", "reservoir_level",
            "month", "hour", "lag_1", "lag_24", "lag_168",
            "rolling_mean_24", "rolling_mean_168"]
target = "power_output"

X = df[features]
y = df[target]

# ── Scale Data ────────────────────────────────────────────────────
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)
joblib.dump(scaler, "models/scaler.pkl")
print("✅ Scaler saved")

# ── Train Test Split ──────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)
print(f"✅ Train: {X_train.shape}, Test: {X_test.shape}")

# ── Train XGBoost Model ───────────────────────────────────────────
model = XGBRegressor(
    n_estimators=200,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    verbosity=1
)

model.fit(X_train, y_train,
          eval_set=[(X_test, y_test)],
          verbose=50)

joblib.dump(model, "models/xgboost_model.pkl")
print("✅ Model saved")

# ── Evaluate Model ────────────────────────────────────────────────
y_pred = model.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mae  = mean_absolute_error(y_test, y_pred)
r2   = r2_score(y_test, y_pred)

print(f"\n📊 Model Performance:")
print(f"   RMSE : {rmse:.2f} MW")
print(f"   MAE  : {mae:.2f} MW")
print(f"   R²   : {r2:.4f}")

# ── Plot Feature Importance ───────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 6))
importance = pd.Series(model.feature_importances_, index=features).sort_values()
importance.plot(kind="barh", color="#00B4D8", ax=ax)
ax.set_title("Feature Importance", fontsize=14, fontweight="bold")
ax.set_xlabel("Importance Score")
ax.grid(True, alpha=0.3, axis="x")
plt.tight_layout()
plt.savefig("outputs/feature_importance.png", dpi=150)
plt.show()
print("✅ Feature importance plot saved")

# ── Plot Actual vs Predicted ──────────────────────────────────────
fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(y_test.values[:200], label="Actual", color="#00B4D8", linewidth=2)
ax.plot(y_pred[:200], label="Predicted", color="#EF476F", linewidth=2, linestyle="--")
ax.set_title("Actual vs Predicted Power Output (First 200 Hours)", fontsize=14, fontweight="bold")
ax.set_xlabel("Time (Hours)")
ax.set_ylabel("Power Output (MW)")
ax.legend()
ax.grid(True, alpha=0.3)
ax.text(0.02, 0.95, f"R² = {r2:.4f} | RMSE = {rmse:.2f} MW",
        transform=ax.transAxes, fontsize=11,
        bbox=dict(boxstyle="round", facecolor="#065A82", alpha=0.8), color="white")
plt.tight_layout()
plt.savefig("outputs/actual_vs_predicted.png", dpi=150)
plt.show()
print("✅ Prediction plot saved")
print("\n✅ Model Training Complete!")
