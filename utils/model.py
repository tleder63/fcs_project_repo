"""
Machine learning – OWNER: Person 3

Covers graded requirement 5 (train and use our own model).

Idea
----
1. Each flatmate rates recipes with 👍 / 👎 (table `ratings`).
2. For each flatmate we train a small classifier that predicts
   P(this person likes the recipe) from recipe features.
3. For the group we combine the individual probabilities:
     - "average":       mean of everyone's probability (best for the group overall)
     - "least_misery":  the LOWEST probability (nobody ends up hating dinner)

Features (suggestion – try what works best)
-------------------------------------------
- one-hot cuisines        (Italian=1, Thai=0, ...)
- one-hot diets           (vegetarian=1, ...)
- ready_in_minutes, calories (numbers; scale them)
- maybe: top-N most common ingredients as 0/1 columns

Model (suggestion): sklearn LogisticRegression or KNeighborsClassifier.
Cold start: with fewer than MIN_RATINGS ratings, a model is meaningless – fall
back to a simple score from the stated preferences instead.

--- AI-generated (Claude, 23.11.2026): module structure, docstrings and function
signatures; prompt: "skeleton for a flat-share recipe recommender in Streamlit".
The function bodies are written by the team. ---
"""

import pandas as pd

from utils.constants import MODELS_DIR

MIN_RATINGS = 10   # below this, use the fallback score


def build_features(recipes: list[dict]) -> pd.DataFrame:
    """Turn recipe dicts into a numeric feature table (one row per recipe).

    TODO (Person 3): one-hot encode cuisines/diets (pd.get_dummies or
    sklearn MultiLabelBinarizer), add numeric columns, fill missing values.
    IMPORTANT: training and prediction must produce the same columns –
    store the column list together with the model.
    """
    raise NotImplementedError


def train_model(flatmate_id: int):
    """Train and save a model for one flatmate.

    TODO (Person 3):
      - ratings = db.get_ratings(flatmate_id); return None if < MIN_RATINGS
      - X = build_features(...), y = liked column
      - fit the model, check accuracy (train/test split or cross-validation –
        nice to show in the video!)
      - joblib.dump({"model": model, "columns": X.columns.tolist()},
                    MODELS_DIR / f"flatmate_{flatmate_id}.joblib")
    """
    raise NotImplementedError


def predict_like_probability(flatmate_id: int, recipes: list[dict]) -> list[float]:
    """Return P(like) for each recipe for one flatmate.

    TODO (Person 3): load the saved model (or train it), predict_proba.
    Placeholder: 0.5 for everything (= "no idea yet"), so the app runs.
    """
    return [0.5 for _ in recipes]


def group_score(probabilities: list[float], strategy: str = "least_misery") -> float:
    """Combine the probabilities of all people eating into one group score.

    probabilities: one value per selected flatmate, for ONE recipe.
    TODO (Person 3): implement "average" and "least_misery".
    """
    return 0.5
