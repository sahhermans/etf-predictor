# src/data/load_data.py

import pandas as pd
from sqlalchemy import create_engine, inspect

def load_raw_data(
    db_path: str = "data/raw/etf_data.db",
    tickers: list[str] = None,
    start_date: str = None,
    end_date: str = None,
    table_name: str = "etf_prices"
) -> pd.DataFrame:
    """
    Load raw ETF data from SQLite, optionally filtered by ticker and/or date range.

    Returns a pandas DataFrame.
    """
    engine = create_engine(f"sqlite:///{db_path}")
    inspector = inspect(engine)
    if table_name not in inspector.get_table_names():
        raise ValueError(f"Table '{table_name}' does not exist in {db_path}.")

    # Build WHERE clause
    filters = []
    if tickers:
        tickers_quoted = [f"'{t}'" for t in tickers]
        filters.append(f"Symbol IN ({', '.join(tickers_quoted)})")
    if start_date:
        filters.append(f"Date >= '{start_date}'")
    if end_date:
        filters.append(f"Date <= '{end_date}'")

    where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""
    query = f"SELECT * FROM {table_name} {where_clause}"

    df = pd.read_sql(query, engine, parse_dates=["Date"])
    return df