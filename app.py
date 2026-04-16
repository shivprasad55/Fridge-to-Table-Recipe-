from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load CSV
data = pd.read_csv("recipes.csv")

recipes = []
for _, row in data.iterrows():
    ingredients = row["ingredients"].lower().split(",")
    recipes.append({
        "name": row["name"],
        "ingredients": ingredients
    })

def recommend_recipes(user_ingredients):
    results = []

    for recipe in recipes:
        match_count = sum(
            1 for item in recipe["ingredients"] 
            if item.strip() in user_ingredients
        )

        if match_count > 0:
            results.append((recipe["name"], match_count))

    results.sort(key=lambda x: x[1], reverse=True)
    return results

@app.route("/", methods=["GET", "POST"])
def home():
    results = []
    if request.method == "POST":
        user_input = request.form["ingredients"]
        user_ingredients = [i.strip().lower() for i in user_input.split(",")]
        results = recommend_recipes(user_ingredients)

    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)