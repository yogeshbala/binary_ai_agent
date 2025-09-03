
import streamlit as st
import pandas as pd
from utils.main import run_all_strategies

st.set_page_config(page_title="Trading Strategy Dashboard", layout="wide")

st.title("📈 Strategy Signal Dashboard")

symbol = st.text_input("Enter symbol", value="EURUSD=X")
interval = st.selectbox("Select interval", ["5m", "15m", "1h", "1d"])
run_button = st.button("Run Strategies")

if run_button:
    results = run_all_strategies(symbol=symbol, interval=interval)
    for name, signal in results.items():
        st.metric(label=name, value=signal)
