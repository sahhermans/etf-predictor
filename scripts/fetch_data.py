import sys
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.data_ingestion import download_etf_data_to_sqlite

# Define parameters
tickers = ["SPY", "IVV", "VTI"]
db_path = "data/raw/etf_data.db"
start_date = "2010-01-01"
end_date = "2025-03-26"

# Download data
download_etf_data_to_sqlite(tickers, db_path, start_date, end_date)