# scripts/run_data_pipeline.py

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.data.load_data import load_raw_data
from src.data.clean_data import clean_data
from src.data.feature_engineering import add_features
from src.data.utils import save_to_sqlite

def main():
    df_raw = df = load_raw_data(
        db_path="data/raw/etf_data.db",
        tickers=["SPY", "VTI"],
        start_date="2021-01-01",
        end_date="2023-12-31"
        )
    df_clean = clean_data(df_raw)
    df_features = add_features(df_clean)
    save_to_sqlite(df_features)
    print("✅ Data pipeline completed and saved to database.")

if __name__ == "__main__":
    main()

