import yfinance as yf
import sqlite3
import os
import pandas as pd

def download_etf_data_to_sqlite(
    tickers: list[str],
    db_path: str,
    start_date: str,
    end_date: str
) -> None:
    # Ensure output folder exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # Open connection
    conn = sqlite3.connect(db_path)

    for ticker in tickers:
        print(f"Fetching data for {ticker}...")

        # Download data
        data = yf.Ticker(ticker).history(start=start_date, end=end_date, auto_adjust=False)

        # Check if downloaded data is empty
        if data.empty:
            print(f"No data found for {ticker}. Skipping.")
            continue

        # Clean up
        data.reset_index(inplace=True)
        data['Date'] = data['Date'].dt.tz_convert('UTC').dt.date

        # Optional: ensure consistent column order
        columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
        data = data[[col for col in columns if col in data.columns]]

        # Write to SQLite
        # Define column types
        dtype_map = {
            'Date': 'TEXT',          # ISO datetime as TEXT
            'Open': 'REAL',
            'High': 'REAL',
            'Low': 'REAL',
            'Close': 'REAL',
            'Adj Close': 'REAL',
            'Volume': 'INTEGER'
        }
        
        data.to_sql(ticker, conn, if_exists='replace', index=False, dtype=dtype_map)

        print(f"{ticker}: {len(data)} rows written to SQLite.")

    conn.close()
    print("All data written and connection closed.")
