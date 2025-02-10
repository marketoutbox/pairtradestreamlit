import streamlit as st
import yfinance as yf
from streamlit_js_eval import streamlit_js_eval
import pandas as pd
import json

st.title("📈 Pair Trading with Yahoo Finance + IndexedDB")

# Function to fetch Yahoo Finance data
def fetch_yahoo_data(stock_symbol):
    stock = yf.Ticker(stock_symbol)
    df = stock.history(period="2y")  # Get last 2 years of data
    df.reset_index(inplace=True)
    df = df[['Date', 'Close']]  # Keep only Date & Close Price
    df.columns = ['date', 'price']
    df['symbol'] = stock_symbol  # Add symbol column
    return df.to_dict(orient="records")  # Convert to JSON format

# User selects stock symbols
stock1 = st.text_input("Enter Stock 1 (e.g., AAPL)")
stock2 = st.text_input("Enter Stock 2 (e.g., MSFT)")

if st.button("Fetch & Store Data"):
    if stock1 and stock2:
        data1 = fetch_yahoo_data(stock1)
        data2 = fetch_yahoo_data(stock2)
        
        combined_data = data1 + data2  # Merge both stock data
        json_data = json.dumps(combined_data)  # Convert to JSON
        
        # JavaScript function to store in IndexedDB
        save_data_js = f"""
        function() {{
            let request = indexedDB.open("StockDB", 1);
            request.onsuccess = function(event) {{
                let db = event.target.result;
                let transaction = db.transaction(["prices"], "readwrite");
                let store = transaction.objectStore("prices");
                let stockData = {json_data};
                stockData.forEach(data => store.put(data));
            }};
        }}
        """
        streamlit_js_eval(save_data_js)  # Run JavaScript in browser

        st.success("✅ Stock prices saved in IndexedDB!")
    else:
        st.error("⚠️ Please enter two stock symbols.")
