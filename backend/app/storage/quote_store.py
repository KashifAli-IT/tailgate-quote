import json
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

def generate_quote_id() -> str:
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT quote_id
            FROM quotes
            WHERE quote_id LIKE 'Q-%'
            ORDER BY CAST(SUBSTR(quote_id, 3) AS INTEGER) DESC
            LIMIT 1
            """
        ).fetchone()

    if row is None:
        next_number = 1
    else:
        last_number = int(row["quote_id"][2:])
        next_number = last_number + 1

    return f"Q-{next_number:04d}"

def save_quote(
    quote_id: str,
    quote: dict,
) -> None:
    with get_connection() as connection:
        connection.execute(
            """
            INSERT OR REPLACE INTO quotes
            (
                quote_id,
                status,
                customer_name,
                quote_data
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                quote_id,
                quote["status"],
                quote["customer_name"],
                json.dumps(quote),
            ),
        )

        connection.commit()


def get_saved_quote(
    quote_id: str,
) -> dict | None:
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT quote_data
            FROM quotes
            WHERE quote_id = ?
            """,
            (quote_id,),
        ).fetchone()

    if row is None:
        return None

    return json.loads(row["quote_data"])