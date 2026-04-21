import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# =============================
# PAGE CONFIG
# =============================
st.set_page_config(page_title="Take the Offer Bonus", layout="wide")

# =============================
# TITLE + DESCRIPTION
# =============================
st.title("🎲 Optimal Strategy for Take-the-Offer Bonus")

st.markdown("""
## 🎯 Problem Description
This project analyzes an optimal decision strategy in a weighted bonus game.

At each step, the player can:
- Accept the current offer  
- Reject it (up to 3 times)

The goal is to maximize expected value (EV) using an iterative approximation of optimal stopping.
""")

# =============================
# DATA
# =============================
pays = [
1000, 500, 250, 225, 200, 190, 180, 175, 170, 165,
160, 155, 150, 145, 140, 135, 130, 125, 120, 115,
110, 105, 100, 95, 90, 85, 80, 75, 70, 65,
60, 55, 50, 45, 40, 35, 30, 25, 20, 15,
10, 5
]

weights = [
45, 2, 2, 2, 1, 2, 8, 8, 6, 8,
39, 4, 4, 2, 4, 8, 38, 14, 96, 8,
25, 4, 6, 4, 6, 16, 12, 84, 42, 250,
600, 623, 207, 1500, 1700, 3200, 4000, 4200, 4200, 3000,
1000, 20
]

# =============================
# DATAFRAME
# =============================
data = pd.DataFrame({
    "pays": pays,
    "weights": weights
})

data["prob"] = data["weights"] / data["weights"].sum()

# =============================
# EXPECTED VALUE (ITERATIVE APPROX)
# =============================
EV_0 = (data["pays"] * data["prob"]).sum()

value1 = np.maximum(data["pays"], EV_0)
EV_1 = (value1 * data["prob"]).sum()

value2 = np.maximum(data["pays"], EV_1)
EV_2 = (value2 * data["prob"]).sum()

value3 = np.maximum(data["pays"], EV_2)
EV_3 = (value3 * data["prob"]).sum()

# =============================
# 📊 HISTOGRAM (SORTED + CLEAN)
# =============================
st.subheader("📊 Payout Distribution")

sorted_data = data.sort_values("pays")

fig1, ax1 = plt.subplots()

ax1.bar(sorted_data["pays"], sorted_data["prob"], width=5)

ax1.set_xlabel("Payout")
ax1.set_ylabel("Probability")
ax1.set_title("Distribution of Rewards")

ax1.set_xlim(min(sorted_data["pays"]), max(sorted_data["pays"]))
ax1.grid(axis="y", alpha=0.3)

st.pyplot(fig1)

st.caption("""
This chart shows the probability distribution of all possible rewards.
Higher bars indicate more frequent payouts in the weighted system.
""")

# =============================
# 📈 EV PROGRESSION
# =============================
st.subheader("📈 Expected Value Progression")

EVs = [EV_0, EV_1, EV_2, EV_3]
labels = ["EV0", "EV1", "EV2", "EV3"]

fig2, ax2 = plt.subplots()

ax2.plot(labels, EVs, marker="o")
ax2.set_ylabel("Expected Value")
ax2.set_title("Optimal Decision Improvement")
ax2.grid(True, alpha=0.3)

st.pyplot(fig2)

st.caption("""
Each step represents improved decision-making as more rejection opportunities are allowed.
EV3 represents the best achievable expected value under this model.
""")

# =============================
# NUMERICAL RESULTS
# =============================
st.subheader("📌 Final Expected Values")

st.write(f"**EV0 (no rejection):** {EV_0:.2f}")
st.write(f"**EV1 (1 rejection):** {EV_1:.2f}")
st.write(f"**EV2 (2 rejections):** {EV_2:.2f}")
st.write(f"**EV3 (optimal play):** {EV_3:.2f}")

st.markdown("---")

st.subheader("📊 Interpretation")

st.write("""
The increase from EV0 to EV3 shows the value of optimal decision-making.
Allowing rejection significantly increases expected winnings in this weighted bonus system.
""")