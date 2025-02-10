import streamlit as st
import yfinance as yf
import json
import streamlit.components.v1 as components

# Streamlit page setup
st.set_page_config(page_title="Pair Trading App", layout="wide")
st.title("📈 Pair Trading with IndexedDB")

# ✅ Custom JS for IndexedDB communication
indexeddb_js = """
<script>
function saveStockPrice(symbol, priceData) {
    let request = indexedDB.open("StockDB", 1);

    request.onupgradeneeded = function(event) {
        let db = event.target.result;
        if (!db.objectStoreNames.contains("prices")) {
            db.createObjectStore("prices", { keyPath: "symbol" });
            console.log("✅ Created object store: prices");
        }
    };

    request.onsuccess = function(event) {
        let db = event.target.result;

        if (!db.objectStoreNames.contains("prices")) {
            console.error("❌ Object store 'prices' not found.");
            return;
        }

        let transaction = db.transaction(["prices"], "readwrite");
        let store = transaction.objectStore("prices");

        let stockEntry = {
            symbol: symbol,
            prices: priceData,
            timestamp: new Date().toISOString()
        };

        let putRequest = store.put(stockEntry);

        putRequest.onsuccess = function() {
            console.log("✅ Data saved successfully:", stockEntry);
            alert("✅ Data saved successfully for " + symbol);
        };
