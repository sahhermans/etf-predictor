# src/data/clean_data.py
def clean_data(df):
    df = df.sort_values(["symbol", "date"]).drop_duplicates()
    df = df[df["close"].notna()]
    df["close"] = df.groupby("symbol")["close"].transform(lambda x: x.fillna(method="ffill").fillna(method="bfill"))
    return df

import pandas as pd

def clean_data(df: pd.DataFrame)-> pd.DataFrame:
    """
    Clean raw ETF data:
    - Sorts by symbol and date
    - Removes fully empty rows
    - Forward- and back-fills missing prices within each symbol
    """

    # Sort for safety
    df = df.sort_values(by=["Symbol", "Date"]).reset_index(drop=True)

    # Drop rows where all fields (except Date/Symbol) are NA
    value_cols = [col for col in df.columns if col not in ["Date", "Symbol"]]
    df = df.dropna(subset=value_cols, how="all")

    # Forward/backward fill missing values within each symbol
    df[value_cols] = df.groupby("Symbol")[value_cols].transform(lambda group: group.ffill().bfill())

    return df
