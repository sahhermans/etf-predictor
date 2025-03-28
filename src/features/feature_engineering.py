import pandas as pd
import numpy as np
from sklearn.decomposition import PCA

def add_features(df: pd.DataFrame, target_symbol: str = None) -> pd.DataFrame:
    """
    Add technical, calendar, correlation, PCA-based features, and target variables to cleaned ETF data.
    Optionally filter the final output to a specific target ETF.
    Assumes one row per (Date, Symbol) and sorted by Symbol and Date.
    """
    df = df.copy()

    # Basic Returns
    df['return_1d'] = df.groupby('Symbol')['Close'].pct_change(1)
    df['return_5d'] = df.groupby('Symbol')['Close'].pct_change(5)
    df['return_21d'] = df.groupby('Symbol')['Close'].pct_change(21)

    # Moving Averages
    df['ma_10'] = df.groupby('Symbol')['Close'].transform(lambda x: x.rolling(10).mean())
    df['ma_21'] = df.groupby('Symbol')['Close'].transform(lambda x: x.rolling(21).mean())
    df['ma_ratio_10_50'] = df['ma_10'] / df.groupby('Symbol')['Close'].transform(lambda x: x.rolling(50).mean())

    # Volatility/Range
    df['volatility_10'] = df.groupby('Symbol')['return_1d'].transform(lambda x: x.rolling(10).std())
    df['range_pct'] = (df['High'] - df['Low']) / df['Open']

    # Volume-based
    df['volume_change_1d'] = df.groupby('Symbol')['Volume'].pct_change()
    df['volume_zscore_10'] = df.groupby('Symbol')['Volume'].transform(
        lambda x: (x - x.rolling(10).mean()) / x.rolling(10).std()
    )

    # Calendar features
    df['day_of_week'] = df['Date'].apply(lambda x: x.weekday())
    df['month'] = df['Date'].apply(lambda x: x.month)
    df['is_month_end'] = df['Date'].apply(lambda x: x.is_month_end)

    # Autocorrelation of returns
    for window in [5, 21]:
        df[f'autocorr_1d_{window}'] = df.groupby('Symbol')['return_1d'].transform(
            lambda x: x.rolling(window).apply(lambda y: y.autocorr(lag=1) if y.notna().sum() > 1 else np.nan, raw=False)
        )

    # Create pivot of Close prices for correlation and PCA
    pivot_close = df.pivot(index='Date', columns='Symbol', values='Close')

    # Pairwise correlation with a single reference ETF
    if target_symbol and target_symbol in pivot_close.columns:
        for col in pivot_close.columns:
            if col != target_symbol:
                corr_name = f'corr_{target_symbol}_{col}_10d'
                rolling_corr = pivot_close[target_symbol].rolling(10).corr(pivot_close[col])
                df = df.merge(
                    rolling_corr.rename(corr_name),
                    left_on='Date', right_index=True, how='left'
                )

    # PCA on close prices
    pca_data = pivot_close.dropna()
    dynamic_pca_components = min(3, pca_data.shape[1])
    if len(pca_data) >= dynamic_pca_components:
        pca = PCA(n_components=dynamic_pca_components)
        pca_components_arr = pca.fit_transform(pca_data)
        for i in range(dynamic_pca_components):
            df = df.merge(
                pd.DataFrame({
                    'Date': pca_data.index,
                    f'pca_component_{i+1}': pca_components_arr[:, i]
                }),
                on='Date', how='left'
            )

    # Target variables
    df['target_return_1d'] = df.groupby('Symbol')['return_1d'].shift(-1)
    df['target_return_5d'] = df.groupby('Symbol')['return_5d'].shift(-5)
    df['target_return_21d'] = df.groupby('Symbol')['return_21d'].shift(-21)

    # Filter to target symbol if specified
    if target_symbol:
        df = df[df['Symbol'] == target_symbol].reset_index(drop=True)

    return df
