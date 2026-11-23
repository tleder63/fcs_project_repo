"""
Page: charts about the flat's tastes and the recipes – OWNER: Person 4

Covers graded requirement 3 (visualisation that serves the use case).

--- AI-generated (Claude, 23.11.2026): page outline only; prompt: "skeleton
for a flat-share recipe recommender in Streamlit". TODO parts are written by
the team. ---
"""

import streamlit as st

from utils.db import get_flatmates, get_ratings, get_recipes, init_db

init_db()
st.title("📊 Insights")

flatmates = get_flatmates()
recipes = get_recipes()
ratings = get_ratings()

# TODO (Person 4): pick 2–3 charts that help the flat decide, for example
#   - Cuisine votes: bar chart of how many flatmates like each cuisine
#     (preferences.cuisine_votes) -> "where do our tastes overlap?"
#   - Constraints: which intolerances/diets restrict the flat the most
#   - Taste matrix: heatmap flatmates x recipes (liked / disliked) from ratings
#   - Recipes: scatter of cooking time vs calories, coloured by cuisine
# Libraries: st.bar_chart for quick ones, plotly.express for nicer/interactive.

st.write(f"{len(flatmates)} flatmates · {len(recipes)} cached recipes · {len(ratings)} ratings")
st.info("Charts coming soon.")
