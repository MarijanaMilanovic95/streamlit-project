import streamlit as st

st.set_page_config(page_title="My Projects", layout="wide")

st.title("📊 My Projects")

import app1
import app2

page = st.sidebar.selectbox(
    "Choose project",
    [
        "Home",
        "Monte Carlo Simulation",
        "Optimal Strategy for Take-the-Offer Bonus"
    ]
)

if page == "Home":
    st.write("Welcome! Choose a project from the sidebar.")
