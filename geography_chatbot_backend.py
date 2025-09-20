


#!/usr/bin/env python3
"""
Geography AI Chatbot Backend Server with Gemini API Integration
Fixed: Gemini always answers first, fallback only if Gemini fails.

Dependencies:
    pip install flask flask-cors requests python-dotenv google-generativeai geopy pycountry

Environment Setup:
    Create a .env file with:
    GEMINI_API_KEY=your_gemini_api_key_here

Usage:
    python geography_chatbot_backend.py

API Endpoints:
    POST /chat - Send user message, get GeoBot response
"""

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Flask setup
app = Flask(__name__)
CORS(app)

# Gemini API setup
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY in .env")

genai.configure(api_key=GEMINI_API_KEY)


class GeoBot:
    """Geography AI Chatbot powered by Gemini"""

    def __init__(self):
        self.system_prompt = f"""
You are GeoBot 🌍, a friendly geography assistant.
Answer geography questions with helpful details.
If a question is not strictly about geography, still try to answer briefly,
but keep the focus on geographic context whenever possible.

Current date: {datetime.now().strftime("%Y-%m-%d")}
"""
        try:
            self.model = genai.GenerativeModel(
                "gemini-1.5-flash",
                generation_config={
                    "temperature": 0.9,
                    "top_p": 0.95,
                    "top_k": 50,
                    "max_output_tokens": 512,
                },
            )
        except Exception as e:
            print(f"⚠️ Error initializing Gemini model: {e}")
            self.model = None

    def generate_response(self, user_message: str) -> str:
        """Generate a response using Gemini"""
        try:
            if not self.model:
                return "⚠️ Gemini model is not available."

            chat_prompt = f"{self.system_prompt}\n\nUser: {user_message}\nGeoBot:"
            response = self.model.generate_content(chat_prompt)

            if response and response.text.strip():
                return response.text.strip()

            return ""  # Force fallback if Gemini gave nothing

        except Exception as e:
            return f"⚠️ Error with Gemini API: {e}"


# Create GeoBot instance
geo_bot = GeoBot()


@app.route("/chat", methods=["POST"])
def chat():
    """Main chat endpoint"""
    try:
        user_message = request.json.get("message", "").strip()
        if not user_message:
            return jsonify({"error": "Empty message"}), 400

        # Step 1: Always let Gemini try first
        gemini_response = geo_bot.generate_response(user_message)

        if gemini_response:
            return jsonify({
                "response": gemini_response,
                "timestamp": datetime.now().isoformat()
            })

        # Step 2: Fallback if Gemini fails
        return jsonify({
            "response": "I'm GeoBot 🌍! I usually answer geography questions, but I couldn’t find an answer this time."
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)

