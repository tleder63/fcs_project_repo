"""
Page: manage flatmates and their preferences – OWNER: Person 1

Covers graded requirement 4 (user interaction: adding data).

--- AI-generated (Claude, 23.11.2026): add form and list as a working example;
prompt: "skeleton for a flat-share recipe recommender in Streamlit".
TODO parts are written by the team. ---
"""

import sqlite3

import streamlit as st

from utils.constants import CUISINES, DIETS, INTOLERANCES
from utils.db import add_flatmate, get_flatmates, init_db

init_db()
st.title("👥 Flatmates")

# ---------------------------------------------------------------------------
# Add a flatmate (finished example)
# ---------------------------------------------------------------------------
with st.form("add_flatmate", clear_on_submit=True):
    st.subheader("Add a flatmate")
    name = st.text_input("Name")
    diet = st.selectbox("Diet", DIETS)
    intolerances = st.multiselect("Allergies / intolerances", INTOLERANCES)
    dislikes_text = st.text_input("Ingredients you don't eat (comma-separated)",
                                  placeholder="e.g. mushrooms, olives")
    cuisines = st.multiselect("Favourite cuisines", CUISINES)
    submitted = st.form_submit_button("Add")

if submitted:
    if not name.strip():
        st.warning("Please enter a name.")
    else:
        try:
            dislikes = [d.strip() for d in dislikes_text.split(",") if d.strip()]
            add_flatmate(name, diet, intolerances, dislikes, cuisines)
            st.success(f"Added {name}!")
        except sqlite3.IntegrityError:
            st.error(f"There is already a flatmate called {name}.")

# ---------------------------------------------------------------------------
# List of flatmates
# ---------------------------------------------------------------------------
st.subheader("Current flatmates")
flatmates = get_flatmates()
if not flatmates:
    st.info("No flatmates yet – add the first one above.")

for mate in flatmates:
    with st.expander(mate["name"]):
        st.write(f"**Diet:** {mate['diet']}")
        st.write(f"**Intolerances:** {', '.join(mate['intolerances']) or '–'}")
        st.write(f"**Doesn't eat:** {', '.join(mate['dislikes']) or '–'}")
        st.write(f"**Favourite cuisines:** {', '.join(mate['cuisines']) or '–'}")
        # TODO (Person 1): "Edit" and "Delete" buttons using
        # db.update_flatmate() / db.delete_flatmate(). Use a unique key per
        # button, e.g. st.button("Delete", key=f"del_{mate['id']}").
