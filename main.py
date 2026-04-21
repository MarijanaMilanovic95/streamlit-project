import streamlit as st

st.set_page_config(page_title="My Projects", layout="wide")

st.title("📊 My Data Science Projects")

page = st.sidebar.selectbox(
    "Choose project",
    [
        "Home",
        "Monte Carlo Simulation",
        "Optimal Strategy for Take-the-Offer Bonus"
    ]
)

if page == "Home":
    st.markdown("""
    ## 👋 Welcome

    This is a portfolio of data science projects.

    Use the sidebar to select a project:
    - 🎲 Monte Carlo Simulation
    - 🎯 Optimal Strategy for Take-the-Offer Bonus
    """)

elif page == "Monte Carlo Simulation":
    with open("app2.py", encoding="utf-8") as f:
        exec(f.read())

elif page == "Optimal Strategy for Take-the-Offer Bonus":
    with open("app1.py", encoding="utf-8") as f:
        exec(f.read())