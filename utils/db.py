"""
Database layer (SQLite) – OWNER: Person 1

Everything that reads or writes the database lives in this file, so the
pages never write SQL themselves. Covers graded requirement 2 (data from a
database) together with utils/api.py.

Tables
------
flatmates     one row per person in the flat and their food preferences
recipes       recipes we already fetched from Spoonacular (acts as a cache)
ratings       which flatmate liked (1) or disliked (0) which recipe
search_cache  which recipe ids a given search returned (saves API quota)

List-like fields (intolerances, dislikes, cuisines, ...) are stored as
comma-separated text, e.g. "Peanut,Dairy". Use to_csv() / from_csv() below.

--- AI-generated (Claude, 23.11.2026): connection, schema and the two example
functions add_flatmate() / get_flatmates(); prompt: "skeleton for a flat-share
recipe recommender in Streamlit". Functions marked TODO are written by the team. ---
"""

import sqlite3
from contextlib import contextmanager

from utils.constants import DATA_DIR, DB_PATH


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def to_csv(items: list[str]) -> str:
    """Turn a list like ["Peanut", "Dairy"] into "Peanut,Dairy" for storage."""
    return ",".join(item.strip() for item in items if item.strip())


def from_csv(text: str | None) -> list[str]:
    """Turn stored text like "Peanut,Dairy" back into ["Peanut", "Dairy"]."""
    if not text:
        return []
    return [item.strip() for item in text.split(",") if item.strip()]


@contextmanager
def get_connection():
    """Open a connection, commit on success, always close.

    Usage:
        with get_connection() as conn:
            conn.execute("SELECT ...")
    """
    DATA_DIR.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row          # rows behave like dicts: row["name"]
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Schema – called once at app start (app.py). Safe to call repeatedly.
# ---------------------------------------------------------------------------
SCHEMA = """
CREATE TABLE IF NOT EXISTS flatmates (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT NOT NULL UNIQUE,
    diet          TEXT,               -- one of constants.DIETS
    intolerances  TEXT,               -- csv, values from constants.INTOLERANCES
    dislikes      TEXT,               -- csv of ingredients, free text
    cuisines      TEXT,               -- csv of favourite cuisines
    created_at    TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS recipes (
    id                INTEGER PRIMARY KEY,   -- Spoonacular recipe id
    title             TEXT NOT NULL,
    image             TEXT,
    ready_in_minutes  INTEGER,
    servings          INTEGER,
    calories          REAL,
    cuisines          TEXT,                  -- csv
    diets             TEXT,                  -- csv
    ingredients       TEXT,                  -- csv of ingredient names
    source_url        TEXT,
    fetched_at        TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ratings (
    flatmate_id  INTEGER NOT NULL REFERENCES flatmates(id) ON DELETE CASCADE,
    recipe_id    INTEGER NOT NULL REFERENCES recipes(id)   ON DELETE CASCADE,
    liked        INTEGER NOT NULL CHECK (liked IN (0, 1)),
    rated_at     TEXT DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (flatmate_id, recipe_id)     -- one rating per person per recipe
);

CREATE TABLE IF NOT EXISTS search_cache (
    query_key    TEXT PRIMARY KEY,           -- e.g. "pasta|Vegetarian|Peanut"
    recipe_ids   TEXT NOT NULL,              -- csv of recipe ids
    fetched_at   TEXT DEFAULT CURRENT_TIMESTAMP
);
"""


def init_db() -> None:
    """Create all tables if they don't exist yet."""
    with get_connection() as conn:
        conn.executescript(SCHEMA)


# ---------------------------------------------------------------------------
# Flatmates – two finished examples to copy the pattern from
# ---------------------------------------------------------------------------
def add_flatmate(name: str, diet: str, intolerances: list[str],
                 dislikes: list[str], cuisines: list[str]) -> None:
    """Insert a new flatmate. Raises sqlite3.IntegrityError if the name exists."""
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO flatmates (name, diet, intolerances, dislikes, cuisines) "
            "VALUES (?, ?, ?, ?, ?)",   # ? placeholders protect against SQL injection
            (name.strip(), diet, to_csv(intolerances), to_csv(dislikes), to_csv(cuisines)),
        )


def get_flatmates() -> list[dict]:
    """Return all flatmates as a list of dicts, list fields already split."""
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM flatmates ORDER BY name").fetchall()
    flatmates = []
    for row in rows:
        mate = dict(row)
        for field in ("intolerances", "dislikes", "cuisines"):
            mate[field] = from_csv(mate[field])
        flatmates.append(mate)
    return flatmates


# ---------------------------------------------------------------------------
# TODO (Person 1): the functions below are placeholders
# ---------------------------------------------------------------------------
def update_flatmate(flatmate_id: int, diet: str, intolerances: list[str],
                    dislikes: list[str], cuisines: list[str]) -> None:
    """TODO: UPDATE the preferences of an existing flatmate."""
    raise NotImplementedError


def delete_flatmate(flatmate_id: int) -> None:
    """TODO: DELETE a flatmate (their ratings disappear too, see ON DELETE CASCADE)."""
    raise NotImplementedError


def save_recipes(recipes: list[dict]) -> None:
    """TODO: INSERT OR REPLACE recipes (dicts from utils.api.parse_recipe) into `recipes`.

    Used by Person 2 to cache API results.
    """
    raise NotImplementedError


def get_recipes(recipe_ids: list[int] | None = None) -> list[dict]:
    """TODO: return recipes from the cache – all of them, or only the given ids."""
    return []


def save_rating(flatmate_id: int, recipe_id: int, liked: bool) -> None:
    """TODO: INSERT OR REPLACE a rating (a person can change their mind)."""
    raise NotImplementedError


def get_ratings(flatmate_id: int | None = None) -> list[dict]:
    """TODO: return ratings joined with recipe data – for one flatmate or everyone.

    Person 3 needs this to train the model, Person 4 for the charts.
    """
    return []


def get_cached_search(query_key: str) -> list[int] | None:
    """TODO: return the recipe ids stored for this search, or None if not cached."""
    return None


def save_cached_search(query_key: str, recipe_ids: list[int]) -> None:
    """TODO: store which recipe ids a search returned."""
    raise NotImplementedError
