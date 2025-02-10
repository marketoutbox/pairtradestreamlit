// Initialize IndexedDB for Stock Prices
function initIndexedDB() {
    let request = indexedDB.open("StockDB", 1);
    request.onupgradeneeded = function(event) {
        let db = event.target.result;
        if (!db.objectStoreNames.contains("prices")) {
            db.createObjectStore("prices", { keyPath: "date" });
        }
    };
}

// Fetch stock prices from IndexedDB
function fetchStockData() {
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

// Initialize the database
initIndexedDB();
