import streamlit as st
import app1
import app2

st.set_page_config(page_title="My Projects", layout="wide")

st.title("📊 My Projects")

page = st.sidebar.selectbox(
    "Choose project",
    ["Home", "Monte Carlo Simulation", "Take the Offer Bonus"]
)

if page == "Home":
    st.title("📊 Simulation Dashboard")

elif page == "Monte Carlo Simulation":
    app2.run()

elif page == "Take the Offer Bonus":
    app1.run()
