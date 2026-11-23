"""
Page: flatmates rate recipes with 👍 / 👎 – OWNER: Person 3

The ratings are the training data for the ML model (utils/model.py).
Covers graded requirements 4 (interaction) and 5 (machine learning).

--- AI-generated (Claude, 23.11.2026): page outline only; prompt: "skeleton
for a flat-share recipe recommender in Streamlit". TODO parts are written by
the team. ---
"""

import streamlit as st

from utils.db import get_flatmates, get_recipes, init_db

init_db()
st.title("👍 Rate recipes")

flatmates = get_flatmates()
if not flatmates:
    st.info("Add flatmates first (page 'Flatmates').")
    st.stop()

who = st.selectbox("Who is rating?", [m["name"] for m in flatmates])
recipes = get_recipes()

if not recipes:
    st.info("No recipes cached yet – run a search on 'What's for dinner?' first, "
            "or implement db.get_recipes() / db.save_recipes().")
    st.stop()

# TODO (Person 3):
#   - show one recipe at a time that `who` has not rated yet (image + title)
#   - two buttons 👍 / 👎 -> db.save_rating(flatmate_id, recipe_id, liked)
#     (use st.session_state to move to the next recipe)
#   - show "X ratings – the model needs at least MIN_RATINGS"
#   - a "Train my model" button -> model.train_model(flatmate_id), show accuracy
st.write(f"{len(recipes)} recipes available to rate.")
