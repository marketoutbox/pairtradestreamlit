import streamlit as st
import yfinance as yf
import json
from streamlit_js_eval import streamlit_js_eval

st.title("📈 Yahoo Finance Price Storage in IndexedDB")

# Function to fetch stock price data from Yahoo Finance
def fetch_yahoo_data(stock_symbol):
    stock = yf.Ticker(stock_symbol)
    df = stock.history(period="2y")  # Get last 2 years of data
    df.reset_index(inplace=True)

    df['date'] = df['Date'].dt.strftime('%Y-%m-%d')  # Convert date to string
    df['price'] = df['Close'].astype(float)  # Ensure price is a float
    
    df = df[['date', 'price']]
    df['symbol'] = stock_symbol  # Add stock symbol

    return df.to_dict(orient="records")  # Convert DataFrame to list of dicts

# Input box for stock symbol
stock_symbol = st.text_input("Enter Stock Symbol (e.g., AAPL)")

if st.button("Fetch & Store in IndexedDB"):
    if stock_symbol:
        data = fetch_yahoo_data(stock_symbol)

        # Convert data to JSON
        try:
            json_data = json.dumps(data, indent=2)
        except TypeError as e:
            st.error(f"JSON Error: {e}")
            st.write(data)  # Debugging
            st.stop()

        # FIX: Use a valid label as the first argument
        streamlit_js_eval(js_expressions="1+1", key="validate_js")  # Dummy JS check

        # JavaScript to store in IndexedDB
        save_data_js = f"""
        (async function() {{
            let request = indexedDB.open("StockDB", 1);
            request.onupgradeneeded = function(event) {{
                let db = event.target.result;
                if (!db.objectStoreNames.contains("prices")) {{
                    db.createObjectStore("prices", {{ keyPath: "date" }});
                }}
            }};
            request.onsuccess = function(event) {{
                let db = event.target.result;
                let transaction = db.transaction(["prices"], "readwrite");
                let store = transaction.objectStore("prices");
                let stockData = {json_data};
                stockData.forEach(data => store.put(data));
                console.log("✅ Stock prices saved in IndexedDB!");
            }};
        }})();        
        """

        # FIX: Pass JS as second argument with a label
        streamlit_js_eval(js_expressions=save_data_js, key="store_prices")

        st.success(f"✅ {stock_symbol} stock prices stored in IndexedDB!")
    else:
        st.error("⚠️ Please enter a stock symbol.")
