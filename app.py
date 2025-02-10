import streamlit as st
import yfinance as yf
import pandas as pd

def get_stock_data(symbol, start, end):
    data = yf.download(symbol, start=start, end=end)
    return data[['Close']].reset_index()

# Streamlit UI
st.title("Stock Price Data (2021-202d4)")

# User input for stock symbol
symbol = st.text_input("Enter Stock Symbol:", "AAPL")
if st.button("Run"):
    df = get_stock_data(symbol, "2021-01-01", "2024-12-31")
    st.dataframe(df)
