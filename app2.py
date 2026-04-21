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

    # -----------------------------
    # MATRIX FUNCTIONS
    # -----------------------------
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

    # -----------------------------
    # ONE GAME (FIXED!)
    # -----------------------------
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

    # -----------------------------
    # UI
    # -----------------------------
    st.subheader("⚙️ Simulation Settings")

    col1, col2, col3 = st.columns(3)

    with col1:
        n = st.slider("Matrix size", 3, 20, 6)

    with col2:
        prob = st.slider("Probability", 0.0, 0.2, 0.025, 0.001)

    with col3:
        games = st.slider("Number of simulations", 1000, 50000, 10000, step=1000)

    run_btn = st.button("🚀 Run Simulation")

    bet = 20

    # -----------------------------
    # RUN
    # -----------------------------
    if run_btn:

        wins_o = []
        wins_no = []

        zero_o = zero_no = 0
        ge40_o = ge40_no = 0
        sum_o = sum_no = 0

        progress = st.progress(0)

        for i in range(games):

            o, no = play_one_game(prob, n)

            wins_o.append(o)
            wins_no.append(no)

            sum_o += o
            sum_no += no

            zero_o += (o == 0)
            zero_no += (no == 0)

            ge40_o += (o >= 40)
            ge40_no += (no >= 40)

            if i % max(1, games // 100) == 0:
                progress.progress(i / games)

        RTP_o = (sum_o / (games * bet)) * 100
        RTP_no = (sum_no / (games * bet)) * 100

        st.subheader("📊 Results")

        col1, col2 = st.columns(2)

        with col1:
            st.write(f"RTP Overlap: {RTP_o:.2f}%")

        with col2:
            st.write(f"RTP No Overlap: {RTP_no:.2f}%")

        # Histogram
        st.subheader("📊 Histogram")

        fig, ax = plt.subplots()

        ax.hist(wins_o, bins=40, alpha=0.6, label="Overlap")
        ax.hist(wins_no, bins=40, alpha=0.6, label="No Overlap")

        ax.legend()
        st.pyplot(fig)
