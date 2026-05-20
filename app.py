import json
import os
import re
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "products.json"

app = Flask(__name__, static_folder="static", template_folder="static")


def load_products():
    with DATA_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


PRODUCTS = load_products()


def parse_budget(message):
    patterns = [
        r"under\s+(?:rs\.?|inr|rupees)?\s*([0-9,]+)",
        r"below\s+(?:rs\.?|inr|rupees)?\s*([0-9,]+)",
        r"less than\s+(?:rs\.?|inr|rupees)?\s*([0-9,]+)",
        r"budget\s+(?:is|of|around)?\s*(?:rs\.?|inr|rupees)?\s*([0-9,]+)",
        r"([0-9,]+)\s*(?:rs|inr|rupees)",
    ]
    lowered = message.lower()
    for pattern in patterns:
        match = re.search(pattern, lowered)
        if match:
            return int(match.group(1).replace(",", ""))
    return None


def infer_category(message):
    lowered = message.lower()
    category_keywords = {
        "Shoes": ["shoe", "shoes", "sneaker", "running", "jogging", "walking"],
        "Headphones": ["headphone", "headphones", "earphone", "earphones", "music", "travel", "noise"],
        "Backpacks": ["bag", "backpack", "college", "laptop", "travel bag"],
        "Skincare": ["skin", "skincare", "face", "serum", "moisturizer", "mother", "gift"],
        "Smartwatch": ["watch", "smartwatch", "fitness", "steps", "health"],
        "Home": ["home", "kitchen", "lamp", "desk", "room"],
    }
    for category, keywords in category_keywords.items():
        if any(keyword in lowered for keyword in keywords):
            return category
    return None


def infer_use_cases(message):
    lowered = message.lower()
    use_cases = []
    mapping = {
        "daily use": ["daily", "everyday", "regular"],
        "travel": ["travel", "trip", "flight", "train"],
        "college": ["college", "student", "campus", "class"],
        "fitness": ["fitness", "gym", "running", "jogging", "workout"],
        "gift": ["gift", "birthday", "mother", "father", "friend"],
        "work": ["office", "work", "professional", "laptop"],
        "budget": ["cheap", "affordable", "budget", "value"],
    }
    for use_case, keywords in mapping.items():
        if any(keyword in lowered for keyword in keywords):
            use_cases.append(use_case)
    return use_cases


def score_product(product, message, budget, category, use_cases):
    lowered = message.lower()
    score = 0
    reasons = []

    if category and product["category"] == category:
        score += 35
        reasons.append(f"matches the {category.lower()} category")

    if budget:
        if product["price"] <= budget:
            score += 25
            reasons.append(f"fits your budget of Rs {budget}")
        else:
            score -= 30

    for use_case in use_cases:
        if use_case in product["use_cases"]:
            score += 12
            reasons.append(f"works well for {use_case}")

    for tag in product["tags"]:
        if tag.lower() in lowered:
            score += 8
            reasons.append(f"matches your preference for {tag}")

    if product["rating"] >= 4.5:
        score += 8
        reasons.append("has a strong customer rating")

    if product["stock"] > 0:
        score += 5
    else:
        score -= 25

    return score, reasons


def build_follow_up(category, budget, use_cases):
    questions = []
    if not category:
        questions.append("What type of product are you looking for?")
    if not budget:
        questions.append("Do you have a budget range?")
    if not use_cases:
        questions.append("Who is it for and how will they use it?")
    return questions[:2]


def deterministic_reply(message):
    budget = parse_budget(message)
    category = infer_category(message)
    use_cases = infer_use_cases(message)
    follow_up = build_follow_up(category, budget, use_cases)

    ranked = []
    for product in PRODUCTS:
        score, reasons = score_product(product, message, budget, category, use_cases)
        ranked.append({**product, "score": score, "match_reasons": reasons[:4]})

    ranked.sort(key=lambda item: item["score"], reverse=True)
    recommendations = [item for item in ranked if item["score"] > 0 and item["stock"] > 0][:3]

    if not recommendations:
        recommendations = [item for item in ranked if item["stock"] > 0][:3]
        intro = "I could not find an exact match, so here are the closest available options."
    elif follow_up:
        intro = "I can narrow this further, but based on what you shared, these are strong starting options."
    else:
        intro = "Based on your needs, these are the best matches from the catalog."

    best = recommendations[0]
    explanation = (
        f"My top pick is {best['name']} because it {best['benefit'].lower()} "
        f"It is priced at Rs {best['price']} and rated {best['rating']}."
    )

    tradeoffs = []
    for product in recommendations:
        if product["price"] > best["price"]:
            tradeoffs.append(f"{product['name']} costs more but may offer stronger features.")
        elif product["price"] < best["price"]:
            tradeoffs.append(f"{product['name']} is cheaper, but check if its features are enough for you.")

    return {
        "intro": intro,
        "questions": follow_up,
        "recommendations": recommendations,
        "explanation": explanation,
        "tradeoffs": tradeoffs[:2],
        "cart_suggestion": {
            "product_id": best["id"],
            "name": best["name"],
            "message": f"Add {best['name']} to cart if you want the strongest overall match.",
        },
    }


def openai_polish(message, base_reply):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return base_reply

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        compact_products = [
            {
                "name": product["name"],
                "price": product["price"],
                "benefit": product["benefit"],
                "reasons": product["match_reasons"],
            }
            for product in base_reply["recommendations"]
        ]
        prompt = (
            "You are a concise AI shopping assistant. Rewrite the recommendation in a helpful, "
            "honest tone. Do not invent products or prices. Ask at most one follow-up question.\n\n"
            f"User message: {message}\n"
            f"Recommendations: {json.dumps(compact_products)}\n"
            f"Current explanation: {base_reply['explanation']}"
        )
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
        )
        base_reply["llm_summary"] = completion.choices[0].message.content
    except Exception:
        base_reply["llm_summary"] = ""

    return base_reply


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/api/products")
def products():
    return jsonify(PRODUCTS)


@app.post("/api/chat")
def chat():
    payload = request.get_json(force=True)
    message = payload.get("message", "").strip()
    if not message:
        return jsonify({"error": "Message is required"}), 400

    base_reply = deterministic_reply(message)
    reply = openai_polish(message, base_reply)
    return jsonify(reply)


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
