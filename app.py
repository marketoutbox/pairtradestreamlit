import streamlit as st
import yfinance as yf
import pandas as pd

def get_stock_data(symbol, start, end):
    data = yf.download(symbol, start=start, end=end)
    return data[['Close']].reset_index()

# Streamlit UI
st.title("AAPL Stock Price Data (2021-2024)")

# Fetch data
df = get_stock_data("AAPL", "2021-01-01", "2024-12-31")

# Display table
st.dataframe(df)
