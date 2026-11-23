# FlatFood 🍲 – recipe recommendations for shared flats

*(working title)* – FCS group project, HSG, autumn 2026.

**Problem:** In a shared flat, people have different diets, allergies and tastes.
Deciding what to cook together takes time and often ends in compromise meals
nobody really likes. FlatFood stores each flatmate's preferences, combines them
for whoever is eating tonight, fetches matching recipes from the Spoonacular API
and ranks them with a machine-learning model trained on each flatmate's ratings.

## How to run

```
# 1. create and activate a virtual environment (once)
python -m venv .venv
.venv\Scripts\activate          # Mac: source .venv/bin/activate

# 2. install packages
pip install -r requirements.txt

# 3. add your API key
#    copy .streamlit/secrets.toml.example to .streamlit/secrets.toml
#    and paste your Spoonacular key into it

# 4. start the app
streamlit run app.py
```

The SQLite database (`data/flatshare.db`) is created automatically on first start.

## Project structure and owners

| File | What it does | Owner | Graded requirement |
| --- | --- | --- | --- |
| `utils/db.py`, `pages/1_Flatmates.py` | SQLite tables, flatmate management | Person 1 | 2, 4 |
| `utils/api.py`, `utils/preferences.py`, `pages/2_Whats_for_dinner.py` | Spoonacular API + caching, combining preferences, suggestions | Person 2 | 2, 4 |
| `utils/model.py`, `pages/3_Rate_recipes.py` | Ratings, ML model, group score | Person 3 | 4, 5 |
| `pages/4_Insights.py`, `app.py`, README, video | Charts, home page, presentation | Person 4 | 1, 3 |
| `utils/constants.py` | Shared option lists and paths | everyone | – |

Replace "Person 1–4" with your names. Everyone is responsible for comments (req. 6).

## Open tasks (TODO)

- [ ] **P1** `db.py`: update/delete flatmate, save/get recipes, save/get ratings, search cache
- [ ] **P1** Flatmates page: edit and delete buttons
- [ ] **P2** `preferences.py`: combine_preferences(), cuisine_votes()
- [ ] **P2** `api.py`: search_recipes_cached() using the database cache
- [ ] **P2** Dinner page: nicer recipe cards
- [ ] **P3** `model.py`: build_features(), train_model(), predict_like_probability(), group_score()
- [ ] **P3** Rate page: 👍/👎 flow, train button, show accuracy
- [ ] **P4** Insights page: 2–3 charts
- [ ] **P4** Demo data: a few flatmates + ratings so the demo isn't empty
- [ ] **All** Contribution matrix and AI-use slide for the video

Search the code for `TODO` to find every open spot (VS Code: Ctrl+Shift+F).

## AI use

Per HSG rules, AI-generated code is marked in the source code.
- **Claude (Anthropic), 23.11.2026:** generated the project skeleton – folder
  structure, database schema, the Spoonacular wrapper, page outlines and
  docstrings. Each file's header says exactly which parts. Prompt: *"skeleton
  for a flat-share recipe recommender in Streamlit"*.
- Add any further AI use here (tool, date, what for).
