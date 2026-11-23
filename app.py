"""
FlatFood – recipe recommendations for shared flats.  (working title, rename freely)

Home page / entry point. Run with:   streamlit run app.py
The other pages live in the pages/ folder and appear in the sidebar automatically.

OWNER: Person 4 (home page text, overall look)

--- AI-generated (Claude, 23.11.2026), prompt: "skeleton for a flat-share recipe
recommender in Streamlit"; reviewed by the team --- (see README, "AI use")
"""

import streamlit as st

from utils.db import get_flatmates, init_db

st.set_page_config(page_title="FlatFood", page_icon="🍲", layout="wide")

# Make sure the database and its tables exist before any page uses them.
init_db()

st.title("🍲 FlatFood")
st.subheader("What should we cook tonight – that everyone can and will eat?")

# TODO (Person 4): write the problem statement here (graded requirement 1).
st.write(
    "Shared flats waste time and food deciding what to cook when flatmates "
    "have different diets, allergies and tastes. FlatFood combines everyone's "
    "preferences and suggests recipes the whole group will like."
)

flatmates = get_flatmates()
col1, col2 = st.columns(2)
col1.metric("Flatmates", len(flatmates))
col2.metric("Ratings so far", "–")   # TODO: len(db.get_ratings()) once implemented

st.markdown(
    """
**How it works**
1. **Flatmates** – everyone adds their diet, allergies and favourite cuisines.
2. **What's for dinner?** – tick who's eating tonight and get suggestions.
3. **Rate recipes** – 👍 / 👎 so the app learns your taste.
4. **Insights** – see how the flat's tastes compare.
"""
)
