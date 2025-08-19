import os
from flask import Flask, render_template, request, jsonify, session
from groq import Groq

from dotenv import load_dotenv
# Load .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Use a strong secret key in production

# Get Groq API key from environment variable (safer for production)
API_KEY = os.environ.get("GROQ_API_KEY")

# Debug: Print API key status (without exposing the actual key)
if API_KEY:
    print(f"API key found: {API_KEY[:10]}...")
else:
    print("No API key found in environment variables")

# Initialize Groq client only if API key is available
client = None
if API_KEY:
    try:
        client = Groq(api_key=API_KEY)
        print("Groq client initialized successfully")
    except Exception as e:
        print(f"Error initializing Groq client: {e}")
        client = None
else:
    print("No API key available - chatbot will be disabled")

def chatbot_response(messages):
    """
    messages: List of {"role": "user"/"assistant", "content": "..."}
    """
    if not client:
        return "I'm sorry, the chatbot service is currently unavailable. Please try again later or contact support."
    
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", 
                 "content": (
                     "You are an expert courier assistant. "
                     "Answer questions about package tracking, delivery schedules, pricing, and customer support. "
                     "Be polite, helpful, and do not answer unrelated questions."
                 )
                },
                *messages
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error in chatbot response: {e}")
        return "I'm sorry, I'm having trouble processing your request right now. Please try again later."

@app.route("/")
def home():
    session["chat_history"] = []  # Reset chat on page load
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def get_bot_response():
    user_input = request.json["message"]

    # Load chat history
    chat_history = session.get("chat_history", [])

    # Append user message
    chat_history.append({"role": "user", "content": user_input})

    # Get AI response
    bot_response = chatbot_response(chat_history)

    # Append bot response
    chat_history.append({"role": "assistant", "content": bot_response})

    # Save updated history
    session["chat_history"] = chat_history

    return jsonify({"response": bot_response})

# --- Simple pricing estimator ---
def compute_price_estimate(distance_km: float, weight_kg: float, service_speed: str) -> dict:
    """Compute a courier price estimate with a simple transparent formula.

    service_speed: one of {"standard", "express", "same_day"}
    """
    # Guardrails
    distance_km = max(0.0, float(distance_km))
    weight_kg = max(0.0, float(weight_kg))
    speed = (service_speed or "standard").lower()

    # Base pricing parameters
    base_fee = 5.00
    per_km = 0.75
    per_kg = 0.60
    speed_multiplier_map = {
        "standard": 1.0,
        "express": 1.35,
        "same_day": 1.85,
    }
    speed_multiplier = speed_multiplier_map.get(speed, 1.0)

    # Compute
    distance_cost = distance_km * per_km
    weight_cost = weight_kg * per_kg
    subtotal = base_fee + distance_cost + weight_cost
    total = round(subtotal * speed_multiplier, 2)

    return {
        "currency": "USD",
        "total": total,
        "breakdown": {
            "base_fee": base_fee,
            "distance_km": distance_km,
            "distance_cost": round(distance_cost, 2),
            "weight_kg": weight_kg,
            "weight_cost": round(weight_cost, 2),
            "service_speed": speed,
            "speed_multiplier": speed_multiplier,
        },
    }


@app.route("/estimate", methods=["POST"])
def estimate_price():
    data = request.get_json(silent=True) or {}
    try:
        distance_km = float(data.get("distance_km", 0))
        weight_kg = float(data.get("weight_kg", 0))
        service_speed = str(data.get("service_speed", "standard"))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid inputs"}), 400

    estimate = compute_price_estimate(distance_km, weight_kg, service_speed)
    return jsonify(estimate)


@app.route("/services")
def services_page():
    return render_template("services.html")


@app.route("/pricing")
def pricing_page():
    return render_template("pricing.html")


@app.route("/contact")
def contact_page():
    return render_template("contact.html")


@app.route("/debug")
def debug_info():
    """Debug endpoint to check environment variables and client status"""
    return jsonify({
        "api_key_set": bool(API_KEY),
        "api_key_length": len(API_KEY) if API_KEY else 0,
        "client_initialized": client is not None,
        "environment_vars": {
            "GROQ_API_KEY": "SET" if API_KEY else "NOT SET"
        }
    })


# For Vercel deployment
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
