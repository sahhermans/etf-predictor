import sqlite3
import pandas as pd 

def save_features_to_sqlite(df: pd.DataFrame, db_path: str, table_name: str = "features") -> None:
    """
    Save the feature-enhanced DataFrame to an SQLite database.

    Args:
        df (pd.DataFrame): DataFrame to save
        db_path (str): Path to the SQLite .db file
        table_name (str): Name of the table to write to
    """
    with sqlite3.connect(db_path) as conn:
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Features written to table '{table_name}' in database '{db_path}'.")
