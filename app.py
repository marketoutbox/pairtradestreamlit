import streamlit as st
import yfinance as yf
from streamlit_js_eval import streamlit_js_eval
import json

st.title("📈 Pair Trading with Yahoo Finance + IndexedDB")

# Function to fetch stock price data from Yahoo Finance
def fetch_yahoo_data(stock_symbol):
    stock = yf.Ticker(stock_symbol)
    df = stock.history(period="2y")
    df.reset_index(inplace=True)
    
    # Convert 'Date' column to string format
    df['Date'] = df['Date'].astype(str)
    
    df = df[['Date', 'Close']]
    df.columns = ['date', 'price']
    df['symbol'] = stock_symbol  # Add symbol column
    
    return df.to_dict(orient="records")  # Convert to JSON format

# User input for stock symbols
stock1 = st.text_input("Enter Stock 1 (e.g., AAPL)")
stock2 = st.text_input("Enter Stock 2 (e.g., MSFT)")

if st.button("Fetch & Store Data"):
    if stock1 and stock2:
        data1 = fetch_yahoo_data(stock1)
        data2 = fetch_yahoo_data(stock2)
        
        combined_data = data1 + data2  # Merge stock data
        
        try:
            json_data = json.dumps(combined_data)  # Convert to JSON
        except TypeError as e:
            st.error(f"Error in JSON conversion: {e}")
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

st.subheader("📊 Retrieve Data from IndexedDB")
if st.button("Load Data from IndexedDB"):
    load_data_js = """
    async function() {
        return new Promise((resolve) => {
            let request = indexedDB.open("StockDB", 1);
            request.onsuccess = function(event) {
                let db = event.target.result;
                let transaction = db.transaction(["prices"], "readonly");
                let store = transaction.objectStore("prices");
                let request = store.getAll();
                request.onsuccess = function() {
                    resolve(request.result);
                };
            };
        });
    }
    """
    data = streamlit_js_eval(load_data_js, want_output=True)
    if data:
        st.write("📈 Loaded Data from IndexedDB:")
        st.dataframe(data)
    else:
        st.warning("⚠️ No data found in IndexedDB.")
