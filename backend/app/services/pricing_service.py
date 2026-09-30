import json
import re
from pathlib import Path


CATALOG_PATH = (
    Path(__file__).resolve().parents[3]
    / "data"
    / "seed_catalog.json"
)


def load_catalog() -> list[dict]:
    with CATALOG_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def normalize_query(query: str) -> str:
    query = query.lower().strip()

    replacements = {
        "three quarter": "3/4",
        "three-quarter": "3/4",
        "three fourth": "3/4",
        "three-fourth": "3/4",
        "three fourths": "3/4",
        "three-fourths": "3/4",
        "one quarter": "1/4",
        "one-quarter": "1/4",
        "one half": "1/2",
        "one-half": "1/2",
        "one inch": "1",
        "one-inch": "1",
        "three quarter inch": "3/4",
        "three-quarter-inch": "3/4",
    }

    for source, target in replacements.items():
        query = query.replace(source, target)

    query = query.replace(" inch", "")
    query = query.replace("-inch", "")

    query = re.sub(r"[^\w/.\s-]", " ", query)
    query = re.sub(r"\s+", " ", query)

    return query.strip()


def get_price_list(query: str) -> list[dict]:
    normalized_query = normalize_query(query)

    query_terms = normalized_query.split()

    matches = []

    for item in load_catalog():
        searchable = (
            f"{item['sku']} "
            f"{item['name']} "
            f"{item['category']}"
        ).lower()

        searchable = re.sub(
            r"[^\w/.\s-]",
            " ",
            searchable,
        )

        searchable = re.sub(
            r"\s+",
            " ",
            searchable,
        )

        if all(term in searchable for term in query_terms):
            matches.append(item)

    return matches