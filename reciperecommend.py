# Recipe Recommender
# streamlit run main.py
# utils.py

import streamlit as st
from tests import test_nutrition

# """
# {
#     "recipe_name":{
#         "calories":1000,
#         "proteins":1000,
#         "fats":1000,
#         "carbs":1000,
#         "ingredients":[],
#         "rating":5
#     }
# }
# """

if "recipes" not in st.session_state:
    st.session_state.recipes = []

with st.form("recipe_form"):
    st.subheader("Add a Recipe")

    recipe_name = st.text_input("Recipe Name")
    calories = st.number_input("Calories", min_value=0)
    proteins = st.number_input("Proteins (g)", min_value=0)
    fats = st.number_input("Fats (g)", min_value=0)
    carbs = st.number_input("Carbs (g)", min_value=0)
    ingredients = st.text_area("Ingredients (comma-separated)").split(",")
    vegetarian = st.checkbox("Vegetarian?")
    keto = st.checkbox("Keto?")
    gluten = st.checkbox("Gluten-Free?")
    rating = st.slider("Rating", 1, 5, 3)

    submitted = st.form_submit_button("Save Recipe")

    if submitted:
        try:
            if not recipe_name.strip():
                st.error("Recipe name cannot be empty.")
            if not test_nutrition(calories, proteins, fats, carbs):
                st.error("Invalid or unrealistic nutrition values.")
            else:
                recipe_data = {
                    recipe_name: {
                        "calories": calories,
                        "proteins": proteins,
                        "fats": fats,
                        "carbs": carbs,
                        "ingredients": [i.strip() for i in ingredients if i.strip()],
                        "vegetarian": vegetarian,
                        "keto":keto,
                        "gluten":gluten,
                        "rating": rating,
                    }
                }
                #for rec in st.separated.re
                st.session_state.recipes.append(recipe_data)
                st.success(f"✅ '{recipe_name}' saved!")
        except Exception as e:
            st.error(f"Error saving recipe: {e}")

# View saved recipes

if st.button("View Saved Recipes"):
    if st.session_state.recipes:
        st.subheader("Recipe History")
        for idx, recipe_dict in enumerate(st.session_state.recipes, start=1):
            for name, data in recipe_dict.items():
                st.markdown(f"### {idx}. {name}")
                st.markdown(
                    f"""
                    - 🥗 **Vegetarian:** {"Yes" if data["vegetarian"] else "No"}
                    - 🍹 **Keto:** {"Yes" if data["keto"] else "No"}
                    - 🍞 **Gluten-Free:** {"Yes" if data["gluten"] else "No"}
                    - ⭐ **Rating:** {data['rating']} / 5
                    """
                )

                def color_text(value, healthy_threshold):
                    return f"<span style='color:green'>{value}</span>" if value <= healthy_threshold else f"<span style='color:red'>{value}</span>"

                st.markdown(
                    f"""
                    **Calories:** {color_text(data['calories'], 600)} kcal  
                    **Proteins:** {color_text(data['proteins'], 50)} g  
                    **Fats:** {color_text(data['fats'], 20)} g  
                    **Carbs:** {color_text(data['carbs'], 100)} g  
                    """,
                    unsafe_allow_html=True,
                )
                st.markdown(f"**Ingredients:** {', '.join(data['ingredients'])}")
                st.markdown("---")
    else:
        st.info("No recipes saved yet.")

#Simple Recomemendation Engine

st.subheader("Get Recipe Recommendations")

with st.form("recommendation_form"):
    st.markdown("Choose your preferences:")
    prefer_vegetarian = st.checkbox("Vegetarian", value=False)
    prefer_keto = st.checkbox("Keto", value=False)
    prefer_gluten = st.checkbox("Gluten-Free", value=False)
    min_rating = st.slider("Minimum Rating", 1, 5, 3)
    get_recommendations = st.form_submit_button("Recommend")

if get_recommendations:
    recommended = []

    for recipe_dict in st.session_state.recipes:
        for name, data in recipe_dict.items():
            if data["rating"] < min_rating:
                continue
            if prefer_vegetarian and not data["vegetarian"]:
                continue
            if prefer_keto and not data["keto"]:
                continue
            if prefer_gluten and not data["gluten"]:
                continue
            recommended.append((name, data))

    if recommended:
        st.subheader("Recommended Recipes")
        for idx, (name, data) in enumerate(recommended, start=1):
            st.markdown(f"### {idx}. {name}")
            st.markdown(
                f"""
                - 🥗 **Vegetarian:** {"Yes" if data["vegetarian"] else "No"}
                - 🍹 **Keto:** {"Yes" if data["keto"] else "No"}
                - ⭐ **Rating:** {data['rating']} / 5  
                - **Calories:** {data['calories']} kcal  
                - **Proteins:** {data['proteins']} g  
                - **Fats:** {data['fats']} g  
                - **Carbs:** {data['carbs']} g  
                - **Ingredients:** {', '.join(data['ingredients'])}
                """
            )
            st.markdown("---")
    else:
        st.warning("No matching recipes found based on your preferences.")

#Test Section

# if not test_nutrition(calories, proteins, fats, carbs):
#     st.error("Invalid nutrition values.")
# else:
#     pass
