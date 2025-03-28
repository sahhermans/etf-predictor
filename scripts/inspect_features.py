import sys
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from src.data_pipeline.load_data import load_raw_data
from src.data_pipeline.clean_data import clean_data
from src.features.feature_engineering import add_features

# --- Settings ---
target_symbol = "SPY"

# --- Load and prepare data ---
df_raw = load_raw_data()
df_clean = clean_data(df_raw)
df_features = add_features(df_clean, target_symbol=target_symbol)

# --- Quick look at data in column chunks ---
print("\nFirst 5 rows of features (in chunks of 10 columns):")
for i in range(0, len(df_features.columns), 10):
    print(df_features.iloc[:, i:i+10].head())
    print("\n---\n")

print("\nLast 5 rows of features (in chunks of 10 columns):")
for i in range(0, len(df_features.columns), 10):
    print(df_features.iloc[:, i:i+10].tail())
    print("\n---\n")

# --- Show available columns ---
print("\nFeature Columns:")
print(df_features.columns.tolist())

# --- Check missing values ---
print("\nMissing values per column:")
print(df_features.isna().sum())

# --- Show full correlation matrix of all numeric features ---
numeric_cols = df_features.select_dtypes(include='number').columns
corr = df_features[numeric_cols].corr()

plt.figure(figsize=(16, 12))
sns.heatmap(corr, annot=False, cmap="coolwarm", center=0)
plt.title(f"Full Correlation Matrix of Numeric Features - {target_symbol}")
plt.tight_layout()
plt.show()

# --- Plot a few features over time ---
# Sample every 10th row to reduce plotting time
plot_sample = df_features.set_index("Date").iloc[::10]

# Plot groups of similar-scale features separately
plot_groups = {
    "Price-related": ["Close", "ma_10", "ma_21"],
    "Return-related": ["return_1d", "return_5d", "target_return_1d", "target_return_5d"],
    "Volatility-related": ["volatility_10", "range_pct", "autocorr_1d_21"],
    "Volume/Other": ["volume_change_1d", "volume_zscore_10"]
}

for title, cols in plot_groups.items():
    valid_cols = [col for col in cols if col in plot_sample.columns]
    if valid_cols:
        plot_sample[valid_cols].plot(figsize=(14, 6), title=f"{title} Features Over Time ({target_symbol})")
        plt.xlabel("Date")
        plt.grid(True)
        plt.tight_layout()
        plt.show()
