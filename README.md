# 💧 HydroForecast AI — Hydropower Generation Forecasting Platform
## SDG 7 — Affordable and Clean Energy

---

## 📁 Project Structure

```
hydropower_project/
│
├── data/                   ← Dataset folder (auto created)
├── models/                 ← Saved ML models (auto created)
├── outputs/                ← Saved graphs (auto created)
│
├── generate_data.py        ← Step 1: Generate dataset
├── eda.py                  ← Step 2: Exploratory data analysis
├── train_model.py          ← Step 3: Train XGBoost model
├── decision_engine.py      ← Step 4: Decision support logic
├── dashboard.py            ← Step 5: Streamlit dashboard
│
├── requirements.txt        ← All dependencies
└── README.md               ← This file
```

---

## 🚀 How to Run (Step by Step)

### Step 1 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2 — Generate Dataset
```bash
python generate_data.py
```

### Step 3 — Run EDA
```bash
python eda.py
```

### Step 4 — Train XGBoost Model
```bash
python train_model.py
```

### Step 5 — Test Decision Engine
```bash
python decision_engine.py
```

### Step 6 — Launch Dashboard
```bash
streamlit run dashboard.py
```

---

## 🛠️ Tech Stack

| Component     | Technology         |
|---------------|--------------------|
| Language      | Python 3.x         |
| ML Model      | XGBoost            |
| Data          | Pandas, NumPy      |
| Visualization | Plotly, Matplotlib |
| Dashboard     | Streamlit          |
| Dataset       | NASA POWER / USGS  |

---

## 🎯 Features

- ✅ River flow & rainfall data analysis
- ✅ XGBoost model for power generation forecasting
- ✅ 7-day power generation forecast
- ✅ AI-powered decision engine
- ✅ Real-time alert notification system
- ✅ Interactive Streamlit dashboard

---

## 🌱 SDG 7 — Affordable and Clean Energy
