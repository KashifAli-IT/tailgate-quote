import sqlite3
from pathlib import Path


DATABASE_PATH = (
    Path(__file__).resolve().parents[3]
    / "data"
    / "quotes.db"
)


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database() -> None:
    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS quotes (
                quote_id TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                customer_name TEXT NOT NULL,
                quote_data TEXT NOT NULL
            )
            """
        )

        connection.commit()