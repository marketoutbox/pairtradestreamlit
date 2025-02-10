import streamlit as st
import yfinance as yf
import json
import streamlit.components.v1 as components

st.set_page_config(page_title="Pair Trading App", layout="wide")
st.title("📈 Pair Trading with IndexedDB")

# ✅ JavaScript for IndexedDB storage & retrieval
indexeddb_js = """
<script>
function initDB() {
    let request = indexedDB.open("StockDB", 1);
    request.onupgradeneeded = function(event) {
        let db = event.target.result;
        if (!db.objectStoreNames.contains("prices")) {
            db.createObjectStore("prices", { keyPath: "symbol" });
            console.log("✅ Created object store: prices");
        }
    };
    request.onerror = function(event) {
        console.error("❌ Failed to open IndexedDB:", event.target.error);
    };
}

function saveStockPrice(symbol, priceData) {
    let request = indexedDB.open("StockDB", 1);
    request.onsuccess = function(event) {
        let db = event.target.result;
        let transaction = db.transaction(["prices"], "readwrite");
        let store = transaction.objectStore("prices");

        let stockEntry = {
            symbol: symbol,
            prices: priceData,
            timestamp: new Date().toISOString()
        };

        let putRequest = store.put(stockEntry);
        putRequest.onsuccess = function() {
            console.log("✅ Data saved:", stockEntry);
            alert("✅ Data saved for " + symbol);
        };
        putRequest.onerror = function() {
            console.error("❌ Failed to save data:", putRequest.error);
        };
    };
}

function fetchStockPrice(symbol) {
    let request = indexedDB.open("StockDB", 1);
    request.onsuccess = function(event) {
        let db = event.target.result;
        let transaction = db.transaction(["prices"], "readonly");
        let store = transaction.objectStore("prices");

        let getRequest = store.get(symbol);
        getRequest.onsuccess = function() {
            if (getRequest.result) {
                console.log("📊 Data fetched:", getRequest.result);
                alert("📊 Data for " + symbol + ":\n" + JSON.stringify(getRequest.result.prices, null, 2));
            } else {
                alert("⚠️ No data found for " + symbol);
            }
        };
    };
}

initDB(); // Ensure DB is initialized on page load
</script>
"""

# ✅ Render JavaScript for IndexedDB
components.html(indexeddb_js, height=0)

# ✅ Step 1: Fetch & Store Stock Prices
st.subheader("📥 Fetch & Store Stock Prices")
symbol = st.text_input("Enter stock symbol (e.g., AAPL)", key="fetch_symbol")
if st.button("Fetch & Store Prices"):
    if symbol:
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period="2y")[["Close"]]
            hist.reset_index(inplace=True)
            hist["Date"] = hist["Date"].astype(str)

            price_data = hist.values.tolist()  # Convert DataFrame to List
            json_data = json.dumps(price_data)

            # ✅ Run JavaScript to store in IndexedDB
            js_code = f"<script>saveStockPrice('{symbol}', {json_data})</script>"
            components.html(js_code, height=0)
        except Exception as e:
            st.error(f"❌ Error fetching data: {e}")

# ✅ Step 2: Retrieve Stock Prices
st.subheader("📤 Fetch Stored Stock Prices")
symbol_fetch = st.text_input("Enter symbol to fetch data", key="retrieve_symbol")
if st.button("Retrieve Prices"):
    if symbol_fetch:
        js_code = f"<script>fetchStockPrice('{symbol_fetch}')</script>"
        components.html(js_code, height=0)
