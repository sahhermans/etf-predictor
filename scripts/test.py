import sys
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.data.load_data import load_raw_data

df = load_raw_data(
    db_path="data/raw/etf_data.db",
    tickers=["SPY", "VTI"],
    start_date="2021-01-01",
    end_date="2023-12-31"
)

print(df.head())
print(df.tail())
