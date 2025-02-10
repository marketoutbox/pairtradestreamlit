import streamlit as st
import yfinance as yf
import json
from streamlit_js_eval import streamlit_js_eval

st.title("📊 View Stored Stock Prices from IndexedDB")

# JavaScript to retrieve data from IndexedDB
retrieve_data_js = """
(async function() {
    return new Promise((resolve, reject) => {
        let request = indexedDB.open("StockDB", 1);
        request.onsuccess = function(event) {
            let db = event.target.result;
            let transaction = db.transaction(["prices"], "readonly");
            let store = transaction.objectStore("prices");
            let getAllRequest = store.getAll();
            
            getAllRequest.onsuccess = function() {
                resolve(getAllRequest.result);
            };
            getAllRequest.onerror = function() {
                reject("Failed to fetch data from IndexedDB");
            };
        };
    });
})();
"""

# Button to fetch data
if st.button("Fetch Stored Prices"):
    stored_data = streamlit_js_eval(js_expressions=retrieve_data_js, key="fetch_prices")

    if stored_data:
        st.write("✅ Retrieved Data:")
        st.dataframe(stored_data)  # Show in a table
    else:
        st.warning("⚠️ No data found in IndexedDB.")
