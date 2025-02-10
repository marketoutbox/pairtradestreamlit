import streamlit as st
import sqlite3
import pandas as pd
import numpy as np

def get_stock_data(symbol):
    conn = sqlite3.connect("price_data.db")
    query = f"""
    SELECT date, close FROM stock_prices WHERE symbol = '{symbol}' ORDER BY date
    """
    df = pd.read_sql(query, conn, parse_dates=['date'])
    conn.close()
    return df

def calculate_zscore(series, window=50):
    rolling_mean = series.rolling(window=window).mean()
    rolling_std = series.rolling(window=window).std()
    return (series - rolling_mean) / rolling_std

st.title("Pair Trading Z-Score Calculator")

# Connect to database to fetch available symbols
conn = sqlite3.connect("price_data.db")
cursor = conn.cursor()
cursor.execute("SELECT DISTINCT symbol FROM stock_prices")
symbols = [row[0] for row in cursor.fetchall()]
conn.close()

# Select stock pairs
col1, col2 = st.columns(2)
with col1:
    stock_1 = st.selectbox("Select First Stock", symbols)
with col2:
    stock_2 = st.selectbox("Select Second Stock", symbols)

if stock_1 and stock_2 and stock_1 != stock_2:
    df1 = get_stock_data(stock_1)
    df2 = get_stock_data(stock_2)
    
    df = pd.merge(df1, df2, on='date', suffixes=('_1', '_2'))
    df['price_ratio'] = df['close_1'] / df['close_2']
    df['z_score'] = calculate_zscore(df['price_ratio'])
    
    st.subheader("Z-Score Chart")
    st.line_chart(df[['date', 'z_score']].set_index('date'))
    
    # Display trading signals
    st.subheader("Trading Signals")
    st.write("Enter Trade when Z-score > 2.5 or < -2.5")
    st.write("Exit Trade when Z-score < 1.5 or > -1.5")
    st.dataframe(df[['date', 'price_ratio', 'z_score']].tail(10))
