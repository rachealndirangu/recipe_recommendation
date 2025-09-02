from flask import Flask, render_template, request, redirect
import MySQLdb
import openai
import os
from dotenv import load_dotenv

# --- LOAD ENVIRONMENT VARIABLES ---
load_dotenv()

app = Flask(__name__)

# --- CONFIG ---
openai.api_key = os.getenv("OPENAI_API_KEY")

db = MySQLdb.connect(
    host="localhost",
    user="root",
    passwd="1234@2003",
    db="recipe_app"
)

@app.route("/", methods=["GET", "POST"])
def index():
    cursor = db.cursor()

    if request.method == "POST":
        ingredients = request.form["ingredients"]

        # Query OpenAI for recipes
        prompt = f"Suggest 3 simple recipes using these ingredients: {ingredients}. Format: Title, Ingredients, Steps."
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful recipe assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )

        recipes_text = response.choices[0].message["content"].strip().split("\n\n")

        # Save to DB
        for recipe in recipes_text:
            parts = recipe.split("\n")
            title = parts[0].replace("Title:", "").strip() if "Title:" in parts[0] else parts[0]
            ingredients_text = "\n".join([p for p in parts if "Ingredients:" in p or "-" in p])
            steps = "\n".join([p for p in parts if "Steps:" in p or p.startswith("1.")])

            cursor.execute(
                "INSERT INTO recipes (title, ingredients, steps, user_id) VALUES (%s, %s, %s, %s)",
                (title, ingredients_text, steps, 1)
            )
        db.commit()
        return redirect("/")

    cursor.execute("SELECT title, ingredients, steps FROM recipes ORDER BY id DESC")
    recipes = cursor.fetchall()
    return render_template("index.html", recipes=recipes)

if __name__ == "__main__":
    app.run(debug=True)
