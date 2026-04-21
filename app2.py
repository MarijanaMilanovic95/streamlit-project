import streamlit as st
import random
import numpy as np
import matplotlib.pyplot as plt


def run():

    st.title("🎲 Monte Carlo Simulation")

    st.markdown("""
    This simulation compares two reward models:
    - 🔵 Overlap model (patterns can overlap)
    - 🟢 No Overlap model (strict pattern separation)

    The goal is to analyze distribution, risk, and long-term expected value in credits.
    """)

    # =============================
    # MATRIX
    # =============================
    def create_matrix(n, k):
        return [[k for _ in range(n)] for _ in range(n)]

    def apply_probability(mat, prob):
        n = len(mat)
        for i in range(n):
            for j in range(n):
                if random.random() < prob:
                    mat[i][j] = 1

    def count_ones(mat):
        return sum(sum(row) for row in mat)

    # =============================
    # PATTERNS
    # =============================
    def count_2x2(mat):
        n = len(mat)
        count = 0
        for i in range(n - 1):
            for j in range(n - 1):
                if (mat[i][j] == 1 and mat[i+1][j] == 1 and
                    mat[i][j+1] == 1 and mat[i+1][j+1] == 1):
                    count += 1
        return count

    def count_3x3(mat):
        n = len(mat)
        count = 0
        for i in range(n - 2):
            for j in range(n - 2):
                ok = True
                for x in range(3):
                    for y in range(3):
                        if mat[i+x][j+y] != 1:
                            ok = False
                            break
                    if not ok:
                        break
                if ok:
                    count += 1
        return count

    def count_3x3_and_mark(mat):
        n = len(mat)
        covered = [[False]*n for _ in range(n)]
        count = 0

        for i in range(n - 2):
            for j in range(n - 2):
                ok = True
                for x in range(3):
                    for y in range(3):
                        if mat[i+x][j+y] != 1:
                            ok = False
                            break
                    if not ok:
                        break

                if ok:
                    count += 1
                    for x in range(3):
                        for y in range(3):
                            covered[i+x][j+y] = True

        return count, covered

    def count_2x2_not_in_3x3(mat, covered):
        n = len(mat)
        count = 0

        for i in range(n - 1):
            for j in range(n - 1):
                cells = [(i,j), (i+1,j), (i,j+1), (i+1,j+1)]

                if all(mat[x][y] == 1 for x, y in cells):
                    if all(not covered[x][y] for x, y in cells):
                        count += 1

        return count

    # =============================
    # ONE GAME
    # =============================
    def play_one_game(prob, n):

        life = 3
        mat = create_matrix(n, 0)

        while life > 0:
            prev = count_ones(mat)
            apply_probability(mat, prob)
            new = count_ones(mat)

            if new == prev:
                life -= 1
            else:
                life = 3

        price2_o = count_2x2(mat) * 40
        price3_o = count_3x3(mat) * 110
        total_o = price2_o + price3_o

        c3, covered = count_3x3_and_mark(mat)
        c2 = count_2x2_not_in_3x3(mat, covered)
        total_no = c3 * 110 + c2 * 40

        return total_o, total_no

    # =============================
    # UI
    # =============================
    st.subheader("⚙️ Settings")

    col1, col2, col3 = st.columns(3)

    with col1:
        n = st.slider("Matrix size", 3, 20, 6)

    with col2:
        prob = st.slider("Probability", 0.0, 0.2, 0.025, 0.001)

    with col3:
        games = st.slider("Number of simulations", 1000, 50000, 10000, step=1000)

    run_btn = st.button("🚀 Run Simulation")

    bet = 20

    # =============================
    # SIMULATION
    # =============================
    if run_btn:

        wins_o = []
        wins_no = []

        zero_o = 0
        zero_no = 0

        ge40_o = 0
        ge40_no = 0

        sum_o = 0
        sum_no = 0

        progress = st.progress(0)

        for i in range(games):

            o, no = play_one_game(prob, n)

            wins_o.append(o)
            wins_no.append(no)

            sum_o += o
            sum_no += no

            if o == 0:
                zero_o += 1
            if no == 0:
                zero_no += 1

            if o >= 40:
                ge40_o += 1
            if no >= 40:
                ge40_no += 1

            if i % (games // 100 + 1) == 0:
                progress.progress(i / games)

        # =============================
        # RESULTS
        # =============================
        RTP_o = (sum_o / (games * bet)) * 100
        RTP_no = (sum_no / (games * bet)) * 100

        p_win40_o = (ge40_o / games) * 100
        p_win40_no = (ge40_no / games) * 100

        p_zero_o = (zero_o / games) * 100
        p_zero_no = (zero_no / games) * 100

        st.subheader("📊 Results")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🔵 Overlap Model")
            st.write(f"Return to Player (RTP): {RTP_o:.2f}%")
            st.caption("Return to Player represents the percentage of total bet returned to the player over time, measured in credits.")

            st.write(f"Probability of profit ≥ 40 credits: {p_win40_o:.2f}%")
            st.caption("This shows how often the player achieves at least 40 credits profit.")

            st.write(f"Probability of zero win: {p_zero_o:.2f}%")
            st.caption("This shows how often the player ends with no winnings at all.")

        with col2:
            st.markdown("### 🟢 No Overlap Model")
            st.write(f"Return to Player (RTP): {RTP_no:.2f}%")
            st.write(f"Probability of profit ≥ 40 credits: {p_win40_no:.2f}%")
            st.write(f"Probability of zero win: {p_zero_no:.2f}%")
            
        # =============================
        # STATISTICS
        # =============================
        st.subheader("📈 Distribution Analysis")

        wins_o = np.array(wins_o)
        wins_no = np.array(wins_no)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🔵 Overlap Model Statistics")

            st.write(f"Expected value: {wins_o.mean():.2f} credits")
            st.caption("Expected value represents the average reward per game over many simulations.")

            st.write(f"Standard deviation: {wins_o.std():.2f} credits")
            st.caption("Standard deviation measures how much results vary from the average value (risk/volatility).")

            st.write(f"Minimum reward: {wins_o.min():.0f} credits")
           
            st.write(f"Maximum reward: {wins_o.max():.0f} credits")

        with col2:
            st.markdown("### 🟢 No Overlap Model Statistics")

            st.write(f"Expected value: {wins_no.mean():.2f} credits")
            st.write(f"Standard deviation: {wins_no.std():.2f} credits")
            st.write(f"Minimum reward: {wins_no.min():.0f} credits")
            st.write(f"Maximum reward: {wins_no.max():.0f} credits")

        # =============================
        # HISTOGRAM
        # =============================
        st.subheader("📊 Histogram of Rewards")

        fig, ax = plt.subplots()

        ax.hist(wins_o, bins=40, alpha=0.6, label="Overlap Model")
        ax.hist(wins_no, bins=40, alpha=0.6, label="No Overlap Model")

        ax.set_xlabel("Reward (credits)")
        ax.set_ylabel("Frequency")
        ax.legend()
        ax.grid(alpha=0.3)

        st.pyplot(fig)
