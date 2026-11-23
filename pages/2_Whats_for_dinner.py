"""
Page: pick who's eating tonight and get recipe suggestions – OWNER: Person 2
(ranking by the ML group score comes from Person 3's utils/model.py)

Covers graded requirements 2 (API data) and 4 (user interaction).

--- AI-generated (Claude, 23.11.2026): page layout and the flow between the
modules; prompt: "skeleton for a flat-share recipe recommender in Streamlit".
TODO parts are written by the team. ---
"""

import streamlit as st

from utils.api import search_recipes_cached
from utils.db import get_flatmates, init_db
from utils.model import group_score, predict_like_probability
from utils.preferences import combine_preferences

init_db()
st.title("🍽️ What's for dinner?")

flatmates = get_flatmates()
if not flatmates:
    st.info("Add flatmates first (page 'Flatmates').")
    st.stop()

# 1. Who is eating? -----------------------------------------------------------
names = [m["name"] for m in flatmates]
selected_names = st.multiselect("Who's eating tonight?", names, default=names)
query = st.text_input("Anything specific? (optional)", placeholder="e.g. pasta, curry")
number = st.slider("Number of suggestions", 3, 20, 8)
strategy = st.radio("Group decision", ["least_misery", "average"], horizontal=True,
                    help="least_misery: nobody should dislike it. average: best for the group overall.")

selected = [m for m in flatmates if m["name"] in selected_names]

# 2. Combined filters (shown so users understand what is happening) ---------
filters = combine_preferences(selected)
with st.expander("Combined preferences used for the search"):
    st.json(filters)

# 3. Search + rank ------------------------------------------------------------
if st.button("Find recipes", type="primary", disabled=not selected):
    with st.spinner("Asking Spoonacular..."):
        recipes = search_recipes_cached(query=query, number=number, **filters)

    if not recipes:
        st.warning("No recipes found – try fewer restrictions or another search term.")
        st.stop()

    # Probability per person per recipe, then one group score per recipe.
    probs_per_person = {m["id"]: predict_like_probability(m["id"], recipes) for m in selected}
    for i, recipe in enumerate(recipes):
        recipe["score"] = group_score([probs[i] for probs in probs_per_person.values()], strategy)
    recipes.sort(key=lambda r: r["score"], reverse=True)

    # TODO (Person 2): nicer cards, e.g. 3 per row with st.columns.
    for recipe in recipes:
        col_img, col_text = st.columns([1, 3])
        if recipe.get("image"):
            col_img.image(recipe["image"])
        col_text.markdown(f"### {recipe['title']}")
        col_text.write(f"⏱️ {recipe.get('ready_in_minutes', '?')} min · "
                       f"🔥 {recipe.get('calories') or '?'} kcal · "
                       f"Group score: {recipe['score']:.0%}")
        if recipe.get("source_url"):
            col_text.markdown(f"[Open recipe]({recipe['source_url']})")
