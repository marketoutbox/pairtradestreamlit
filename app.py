import streamlit as st
import yfinance as yf
import pandas as pd

def get_stock_data(symbol, start, end):
    data = yf.download(symbol, start=start, end=end)
    return data[['Date', 'Close']].reset_index()

# Streamlit UI
st.title("Stock Price Data (2021-2024)")

# User input for stock symbol
symbol = st.text_input("Enter Stock Symbol:", "AAPL")

if st.button("Run"):
    df = get_stock_data(symbol, "2021-01-01", "2024-12-31")
    st.dataframe(df)

    # Convert DataFrame to JSON for IndexedDB storage
    stock_data_json = df.to_json(orient="records")

    # Inject JavaScript to store data in IndexedDB
    st.components.v1.html(f"""
        <script>
        const dbName = "StockDB";
        const storeName = "prices";

        function storeData() {{
            let dbRequest = indexedDB.open(dbName, 1);
            dbRequest.onupgradeneeded = function(event) {{
                let db = event.target.result;
                if (!db.objectStoreNames.contains(storeName)) {{
                    db.createObjectStore(storeName, {{ keyPath: "Date" }});
                }}
            }};

            dbRequest.onsuccess = function(event) {{
                let db = event.target.result;
                let transaction = db.transaction(storeName, "readwrite");
                let store = transaction.objectStore(storeName);
                
                let stockData = {stock_data_json};
                stockData.forEach(item => store.put(item));
            }};
        }}

        storeData();
        </script>
    """, height=0)
