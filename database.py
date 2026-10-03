

import sqlite3
import pandas as pd

DB_PATH = "scraped_data.db"
TABLE_NAME = "quotes"


def save_records(records: list[dict], db_path: str = DB_PATH) -> None:
    """Save a list of enriched records to SQLite, replacing prior data."""
    df = pd.DataFrame(records)
    with sqlite3.connect(db_path) as conn:
        df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)


def load_records(db_path: str = DB_PATH) -> pd.DataFrame:
    """Load all stored records back into a DataFrame."""
    with sqlite3.connect(db_path) as conn:
        try:
            return pd.read_sql(f"SELECT * FROM {TABLE_NAME}", conn)
        except pd.errors.DatabaseError:
            return pd.DataFrame(columns=["text", "author", "tags", "polarity",
                                          "subjectivity", "sentiment", "keywords"])


def export_csv(csv_path: str = "scraped_data.csv", db_path: str = DB_PATH) -> None:
    """Export the stored table to a CSV file (handy for the resume/demo)."""
    df = load_records(db_path)
    df.to_csv(csv_path, index=False)
