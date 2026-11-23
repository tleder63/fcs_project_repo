"""
Spoonacular API wrapper – OWNER: Person 2

All calls to the Spoonacular API go through this file. Covers graded
requirement 2 (data loaded via an API).

The free Spoonacular plan has a small daily quota, so every result should be
cached in the database (utils/db.py) and reused – see the TODO in
search_recipes_cached().

API key: put it in .streamlit/secrets.toml (never in the code):
    SPOONACULAR_API_KEY = "your-key"

--- AI-generated (Claude, 23.11.2026): get_api_key(), search_recipes() and
parse_recipe(); prompt: "skeleton for a flat-share recipe recommender in
Streamlit". Functions marked TODO are written by the team. ---
"""

import requests
import streamlit as st

BASE_URL = "https://api.spoonacular.com"
TIMEOUT_SECONDS = 15


def get_api_key() -> str:
    """Read the API key from .streamlit/secrets.toml and stop the app with a hint if missing."""
    try:
        return st.secrets["SPOONACULAR_API_KEY"]
    except (KeyError, FileNotFoundError):
        st.error(
            "No Spoonacular API key found. Create `.streamlit/secrets.toml` "
            "with `SPOONACULAR_API_KEY = \"...\"` (see README)."
        )
        st.stop()


def search_recipes(query: str = "", diet: str | None = None,
                   intolerances: list[str] | None = None,
                   exclude_ingredients: list[str] | None = None,
                   cuisines: list[str] | None = None,
                   number: int = 10) -> list[dict]:
    """Call Spoonacular's complexSearch endpoint and return parsed recipes.

    Every argument maps onto one API filter, so the combined flat
    preferences (utils/preferences.py) can be passed straight in.
    Returns a list of dicts in the format of parse_recipe().
    """
    params = {
        "apiKey": get_api_key(),
        "query": query,
        "number": number,
        "addRecipeInformation": True,   # adds time, servings, cuisines, diets
        "addRecipeNutrition": True,     # adds calories and ingredient list
    }
    if diet and diet != "None":
        params["diet"] = diet
    if intolerances:
        params["intolerances"] = ",".join(intolerances)
    if exclude_ingredients:
        params["excludeIngredients"] = ",".join(exclude_ingredients)
    if cuisines:
        params["cuisine"] = ",".join(cuisines)   # comma = OR for cuisines

    response = requests.get(f"{BASE_URL}/recipes/complexSearch",
                            params=params, timeout=TIMEOUT_SECONDS)
    if response.status_code == 402:
        st.error("Daily Spoonacular quota used up – try again tomorrow or use cached recipes.")
        return []
    response.raise_for_status()
    return [parse_recipe(item) for item in response.json().get("results", [])]


def parse_recipe(raw: dict) -> dict:
    """Reduce Spoonacular's large recipe JSON to the fields our `recipes` table stores."""
    nutrition = raw.get("nutrition") or {}
    calories = next(
        (n.get("amount") for n in nutrition.get("nutrients", []) if n.get("name") == "Calories"),
        None,
    )
    ingredients = [i.get("name", "") for i in nutrition.get("ingredients", [])] or \
                  [i.get("name", "") for i in raw.get("extendedIngredients", [])]
    return {
        "id": raw["id"],
        "title": raw.get("title", "Untitled"),
        "image": raw.get("image"),
        "ready_in_minutes": raw.get("readyInMinutes"),
        "servings": raw.get("servings"),
        "calories": calories,
        "cuisines": raw.get("cuisines", []),
        "diets": raw.get("diets", []),
        "ingredients": [name for name in ingredients if name],
        "source_url": raw.get("sourceUrl"),
    }


# ---------------------------------------------------------------------------
# TODO (Person 2)
# ---------------------------------------------------------------------------
def search_recipes_cached(**filters) -> list[dict]:
    """TODO: same as search_recipes(), but check the database first.

    Suggested steps:
      1. Build a query_key string from the filters (e.g. "pasta|Vegetarian|Peanut").
      2. db.get_cached_search(query_key) -> if ids found, return db.get_recipes(ids).
      3. Otherwise call search_recipes(**filters), then db.save_recipes(...)
         and db.save_cached_search(query_key, [r["id"] for r in recipes]).
    Until this is done, it simply calls the API directly.
    """
    return search_recipes(**filters)
