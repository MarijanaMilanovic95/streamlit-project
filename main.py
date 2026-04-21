import streamlit as st
import app1
import app2

st.set_page_config(page_title="My Projects", layout="wide")

st.title("📊 My Projects")

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
