import streamlit as st
import yfinance as yf
import pandas as pd

# Function to get stock data
def get_stock_data(symbol, start, end):
    data = yf.download(symbol, start=start, end=end)
    data = data.reset_index()  # Ensure 'Date' is a separate column
    return data[['Date', 'Close']]

# Streamlit UI
st.title("Stock Price Data (2021-2024)")

# Input box for stock symbol
symbol = st.text_input("Enter Stock Symbol:", "AAPL")

if st.button("Run"):
    df = get_stock_data(symbol, "2021-01-01", "2024-12-31")
    
    # Display data as a table
    st.dataframe(df)

    # Convert DataFrame to JSON for IndexedDB storage
    stock_data_json = df.to_json(orient="records")

    # Inject JavaScript to store and retrieve data in IndexedDB
    st.components.v1.html(f"""
        <script>
        const dbName = "StockDB";
        const storeName = "prices";

        function storeData(stockData) {{
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

                stockData.forEach(item => store.put(item));
                console.log("✅ Stock data stored in IndexedDB");
            }};

            dbRequest.onerror = function(event) {{
                console.error("❌ IndexedDB error:", event.target.error);
            }};
        }}

        function getData() {{
            let dbRequest = indexedDB.open(dbName, 1);

            dbRequest.onsuccess = function(event) {{
                let db = event.target.result;
                let transaction = db.transaction(storeName, "readonly");
                let store = transaction.objectStore(storeName);
                let request = store.getAll();

                request.onsuccess = function() {{
                    console.log("📊 Retrieved Stock Data from IndexedDB:", request.result);
                }};
            }};
        }}

        // Store and retrieve data
        storeData({stock_data_json});
        getData();
        </script>
    """, height=0)
