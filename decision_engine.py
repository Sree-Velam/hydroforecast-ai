import pandas as pd
import numpy as np

def get_recommendation(predicted_power, demand, reservoir_level,
                        reservoir_max=70, reservoir_min=20):
    """
    Decision engine: gives recommendations based on
    predicted power output, demand and reservoir level.
    """
    surplus = predicted_power - demand
    recommendations = []
    action = ""
    status = ""

    # ── Scenario 1: High Power Surplus ───────────────────────────
    if surplus > 50:
        if reservoir_level < reservoir_max * 0.9:
            action = "STORE WATER"
            status = "🟢 STABLE"
            recommendations = [
                f"✅ Surplus of {surplus:.1f} MW detected",
                f"💧 Maintain reservoir level — current: {reservoir_level:.1f}m",
                "⚡ Reduce turbine load slightly",
                "📉 Consider reducing energy tariff rates",
            ]
        else:
            action = "INCREASE GENERATION"
            status = "🟢 STABLE"
            recommendations = [
                f"✅ Surplus of {surplus:.1f} MW detected",
                "💧 Reservoir is full — increase turbine output",
                "💰 Export surplus energy to main grid",
            ]

    # ── Scenario 2: Balanced ─────────────────────────────────────
    elif -20 <= surplus <= 50:
        action = "MAINTAIN BALANCE"
        status = "🟡 BALANCED"
        recommendations = [
            "✅ Power generation matches demand",
            "💧 Maintain current water flow rate",
            "👁️ Monitor reservoir level closely",
        ]

    # ── Scenario 3: Mild Deficit ──────────────────────────────────
    elif -100 <= surplus < -20:
        if reservoir_level > reservoir_min:
            action = "INCREASE WATER FLOW"
            status = "🟡 CAUTION"
            recommendations = [
                f"⚠️ Deficit of {abs(surplus):.1f} MW detected",
                f"💧 Increase water flow — reservoir at {reservoir_level:.1f}m",
                "⚡ Activate additional turbines",
            ]
        else:
            action = "DRAW FROM GRID"
            status = "🔴 WARNING"
            recommendations = [
                f"⚠️ Deficit of {abs(surplus):.1f} MW — low reservoir",
                "🔌 Draw additional power from main grid",
                "📢 Alert consumers to reduce usage",
            ]

    # ── Scenario 4: Severe Deficit ────────────────────────────────
    else:
        action = "EMERGENCY MODE"
        status = "🔴 CRITICAL"
        recommendations = [
            f"🚨 Severe deficit of {abs(surplus):.1f} MW",
            "🔌 Maximum grid draw activated",
            "💧 All available water reserves being used",
            "📢 URGENT: Implement load shedding",
            "📱 Alert grid operators immediately",
        ]

    return {
        "action": action,
        "status": status,
        "surplus": round(surplus, 2),
        "recommendations": recommendations,
    }


if __name__ == "__main__":
    test_cases = [
        (300, 200, 60),   # Surplus
        (250, 260, 45),   # Balanced
        (150, 300, 40),   # Mild Deficit
        (100, 400, 15),   # Severe Deficit
    ]

    print("🧠 Decision Engine Test\n" + "="*50)
    for power, demand, reservoir in test_cases:
        result = get_recommendation(power, demand, reservoir)
        print(f"\nPower: {power}MW | Demand: {demand}MW | Reservoir: {reservoir}m")
        print(f"Status : {result['status']}")
        print(f"Action : {result['action']}")
        for r in result["recommendations"]:
            print(f"  {r}")
    print("\n✅ Decision Engine Working!")
