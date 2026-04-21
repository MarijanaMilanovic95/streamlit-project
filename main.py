import streamlit as st
import app1
import app2

st.set_page_config(page_title="📊 Simulation Dashboard", layout="wide")

st.title("📊 Simulation Dashboard")

page = st.sidebar.selectbox(
    "Choose project",
    ["Home", "Monte Carlo Simulation", "Take the Offer Bonus"]
)

if page == "Home":
    st.write("📊 Welcome!")
    st.write("👈 Please choose a project from the menu on the left.")

elif page == "Monte Carlo Simulation":
    app2.run()

elif page == "Take the Offer Bonus":
    app1.run()
