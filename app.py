import streamlit as st
import yfinance as yf
import json
from streamlit_js_eval import streamlit_js_eval

st.title("📈 Pair Trading with Yahoo Finance + IndexedDB")

# Function to fetch stock price data from Yahoo Finance
def fetch_yahoo_data(stock_symbol):
    stock = yf.Ticker(stock_symbol)
    df = stock.history(period="2y")
    df.reset_index(inplace=True)

    # Convert 'Date' column to string format and 'Close' to float
    df['date'] = df['Date'].dt.strftime('%Y-%m-%d')  # Ensure date is a string
    df['price'] = df['Close'].astype(float)  # Ensure price is a float
    
    df = df[['date', 'price']]
    df['symbol'] = stock_symbol  # Add stock symbol

    return df.to_dict(orient="records")  # Convert DataFrame to a list of dictionaries

# User input for stock symbols
stock1 = st.text_input("Enter Stock 1 (e.g., AAPL)")
stock2 = st.text_input("Enter Stock 2 (e.g., MSFT)")

if st.button("Fetch & Store Data"):
    if stock1 and stock2:
        data1 = fetch_yahoo_data(stock1)
        data2 = fetch_yahoo_data(stock2)

        combined_data = data1 + data2  # Merge stock data

        try:
            json_data = json.dumps(combined_data, indent=2)  # Convert to JSON with debugging
        except TypeError as e:
            st.error(f"⚠️ JSON Serialization Error: {e}")
            st.write(combined_data)  # Show problematic data
            st.stop()

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
                console.log("✅ Stock prices saved in IndexedDB!");
            }};
        }}
        """
        streamlit_js_eval(save_data_js)  # Run JavaScript in browser

        st.success("✅ Stock prices saved in IndexedDB!")
    else:
        st.error("⚠️ Please enter two stock symbols.")
