from flask import Flask, request, render_template_string
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
        match_count = sum(1 for item in recipe["ingredients"] if item.strip() in user_ingredients)

        if match_count > 0:
            results.append((recipe["name"], match_count))

    results.sort(key=lambda x: x[1], reverse=True)
    return results

HTML = """
<h2>🍳 Fridge-to-Table (Real Data)</h2>

<form method="POST">
    <input type="text" name="ingredients" placeholder="Enter ingredients (egg, rice)">
    <button type="submit">Find Recipes</button>
</form>

<ul>
{% for recipe, score in results %}
    <li>{{ recipe }} (Match: {{ score }})</li>
{% endfor %}
</ul>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    results = []
    if request.method == "POST":
        user_input = request.form["ingredients"]
        user_ingredients = [i.strip().lower() for i in user_input.split(",")]
        results = recommend_recipes(user_ingredients)

    return render_template_string(HTML, results=results)

if __name__ == "__main__":
    app.run(debug=True)