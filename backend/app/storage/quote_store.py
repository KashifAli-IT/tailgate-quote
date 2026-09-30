_quotes: dict[str, dict] = {}
_next_quote_number = 1


def generate_quote_id() -> str:
    global _next_quote_number

    quote_id = f"Q-{_next_quote_number:04d}"
    _next_quote_number += 1

    return quote_id


def save_quote(
    quote_id: str,
    quote: dict,
) -> None:
    _quotes[quote_id] = quote


def get_saved_quote(
    quote_id: str,
) -> dict | None:
    return _quotes.get(quote_id)