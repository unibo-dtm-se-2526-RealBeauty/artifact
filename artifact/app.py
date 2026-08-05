import json
from flask import Flask, render_template, request, jsonify
from artifact.database import init_db

app = Flask(__name__, template_folder="../templates")
init_db()

@app.route("/")
def index():
    return render_template("index.html")

from flask import request, jsonify
from artifact.beauty_api import get_product_by_barcode
from artifact.analyzer import analyze_ingredients
from artifact.database import save_analysis

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    barcode = data.get("barcode", "").strip()
    manual_ingredients = data.get("ingredients", "").strip()

    if barcode:
        product = get_product_by_barcode(barcode)
        if not product:
            return jsonify({"error": "Product not found"}), 404
        ingredients_text = product["ingredients_text"]
        product_name = product["name"]
        brand = product["brand"]
    elif manual_ingredients:
        ingredients_text = manual_ingredients
        product_name = "Manual Entry"
        brand = "Unknown"
    else:
        return jsonify({"error": "Please provide a barcode or ingredients"}), 400

    if not ingredients_text:
        return jsonify({"error": "No ingredients found for this product"}), 404

    result = analyze_ingredients(ingredients_text)
    save_analysis(barcode, product_name, brand, ingredients_text, result)

    return jsonify({
        "product_name": product_name,
        "brand": brand,
        "score": result["score"],
        "summary": result["summary"],
        "flagged": result["flagged"],
        "safe_highlights": result["safe_highlights"]
    })