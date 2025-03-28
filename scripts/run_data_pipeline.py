# scripts/run_data_pipeline.py

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.data_pipeline.load_data import load_raw_data
from src.data_pipeline.clean_data import clean_data
from src.features.feature_engineering import add_features
from src.features.save import save_features_to_sqlite

target_symbol = "SPY"

df_raw = df = load_raw_data(
    #db_path="data/raw/etf_data.db",
    #tickers=["SPY", "VTI"],
    #start_date="2010-01-01",
    #end_date="2025-01-01"
    )
df_clean = clean_data(df_raw)
df_features = add_features(df_clean, target_symbol=target_symbol)
save_features_to_sqlite(df_features, db_path="data/processed/features.db", table_name="features")
print("Data pipeline completed and saved to database.")