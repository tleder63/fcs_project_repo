"""
Combining the preferences of everyone eating tonight – OWNER: Person 2

This is the core idea of the app: several flatmates, one meal that works for all.

Rules we agreed on
------------------
Hard rules (nobody may get something they can't/won't eat) -> UNION
    - intolerances: if ANYONE has one, exclude it for everyone
    - dislikes:     if ANYONE dislikes an ingredient, exclude it
    - diet:         the strictest diet wins (Vegan > Vegetarian > Pescetarian > None)
Soft preferences (only used for ranking, never to filter) -> collect
    - cuisines: count how many people like each cuisine

--- AI-generated (Claude, 23.11.2026): module structure, docstrings and the
expected output format; prompt: "skeleton for a flat-share recipe recommender
in Streamlit". The function bodies are written by the team. ---
"""

# Order from least to most strict. TODO: decide how to handle "Gluten Free",
# "Ketogenic", "Paleo" – they are not stricter/looser than vegetarian, they are
# different. Idea: treat Gluten Free as the intolerance "Gluten" instead.
DIET_STRICTNESS = ["None", "Pescetarian", "Vegetarian", "Vegan"]


def combine_preferences(flatmates: list[dict]) -> dict:
    """Merge the preferences of the selected flatmates into one set of filters.

    Input: list of flatmate dicts as returned by db.get_flatmates().
    Output: a dict whose keys match the arguments of api.search_recipes(), e.g.

        {
            "diet": "Vegetarian",
            "intolerances": ["Peanut", "Dairy"],
            "exclude_ingredients": ["mushrooms"],
            "cuisines": [],            # don't filter by cuisine – see cuisine_votes
        }

    TODO (Person 2): implement the rules from the module docstring.
    Placeholder: returns "no filters" so the app already runs.
    """
    return {"diet": None, "intolerances": [], "exclude_ingredients": [], "cuisines": []}


def cuisine_votes(flatmates: list[dict]) -> dict[str, int]:
    """Count how many of the selected flatmates like each cuisine.

    Example: {"Italian": 3, "Thai": 1}. Used to rank recipes and for a chart.
    TODO (Person 2): implement (hint: collections.Counter).
    """
    return {}
