import sys
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import matplotlib.pyplot as plt
from src.data_pipeline.load_data import load_raw_data
from src.data_pipeline.clean_data import clean_data

# Load raw data
df_raw = load_raw_data(tickers=["IVV"])  # You can change the ticker here

# Clean it
df_clean = clean_data(df_raw)

# Inspect raw data
print("Raw data overview:")
print(df_raw.info())
print(df_raw.isna().sum())

# Inspect cleaned data
print("\nCleaned data overview:")
print(df_clean.info())
print(df_clean.isna().sum())

# Plotting Close price: raw vs cleaned
plt.figure(figsize=(12, 6))
plt.plot(df_raw["Date"], df_raw["Close"], label="Raw", linestyle="--", alpha=0.6)
plt.plot(df_clean["Date"], df_clean["Close"], label="Cleaned", linewidth=2)
plt.title("SPY - Close Price (Raw vs Cleaned)")
plt.xlabel("Date")
plt.ylabel("Close Price")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
