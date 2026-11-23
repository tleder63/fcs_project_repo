"""
Shared constants used across the app (option lists for forms, file paths).

Keeping these in one place means every page shows the same choices and
the values always match what the Spoonacular API accepts.

--- AI-generated (Claude, 23.11.2026), prompt: "skeleton for a flat-share recipe
recommender in Streamlit"; reviewed by the team --- (keep this note, see README)
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# File locations (relative to the repo root, so they work on every laptop)
# ---------------------------------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
MODELS_DIR = ROOT_DIR / "models"
DB_PATH = DATA_DIR / "flatshare.db"

# ---------------------------------------------------------------------------
# Values accepted by the Spoonacular API (complexSearch endpoint).
# Check https://spoonacular.com/food-api/docs if a search returns nothing.
# ---------------------------------------------------------------------------
DIETS = [
    "None",
    "Vegetarian",
    "Vegan",
    "Pescetarian",
    "Gluten Free",
    "Ketogenic",
    "Paleo",
]

INTOLERANCES = [
    "Dairy", "Egg", "Gluten", "Grain", "Peanut", "Seafood",
    "Sesame", "Shellfish", "Soy", "Sulfite", "Tree Nut", "Wheat",
]

CUISINES = [
    "African", "American", "Asian", "British", "Chinese", "French", "German",
    "Greek", "Indian", "Italian", "Japanese", "Korean", "Mediterranean",
    "Mexican", "Middle Eastern", "Spanish", "Thai", "Vietnamese",
]
