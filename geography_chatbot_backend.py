



# #!/usr/bin/env python3
# """
# Geography AI Chatbot Backend Server with Gemini API Integration
# Fixed: Gemini always answers first, fallback only if Gemini fails.
# Auto-opens geobot.html when server starts.

# Dependencies:
#     pip install flask flask-cors requests python-dotenv google-generativeai geopy pycountry

# Environment Setup:
#     Create a .env file with:
#     GEMINI_API_KEY=your_gemini_api_key_here

# Usage:
#     python geography_chatbot_backend.py

# API Endpoints:
#     POST /chat - Send user message, get GeoBot response
# """
       





# import os
# from flask import Flask, request, jsonify, send_file
# from flask_cors import CORS
# from datetime import datetime
# from dotenv import load_dotenv
# import google.generativeai as genai
# from flask import render_template
# # Load environment variables
# load_dotenv()

# # Flask setup
# app = Flask(__name__)
# CORS(app)

# # Gemini API setup
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# if not GEMINI_API_KEY:
#     raise ValueError("Missing GEMINI_API_KEY in .env")

# genai.configure(api_key=GEMINI_API_KEY)


# class GeoBot:
#     """Geography AI Chatbot powered by Gemini"""

#     def __init__(self):
#         self.system_prompt = f"""
# You are GeoBot 🌍, a friendly geography assistant.
# Answer geography questions with helpful details.
# If a question is not strictly about geography, still try to answer briefly,
# but keep the focus on geographic context whenever possible.

# Current date: {datetime.now().strftime("%Y-%m-%d")}
# """
#         try:
#             self.model = genai.GenerativeModel(
#                 "gemini-1.5-flash",
#                 generation_config={
#                     "temperature": 0.9,
#                     "top_p": 0.95,
#                     "top_k": 50,
#                     "max_output_tokens": 512,
#                 },
#             )
#         except Exception as e:
#             print(f"⚠️ Error initializing Gemini model: {e}")
#             self.model = None

#     def generate_response(self, user_message: str) -> str:
#         """Generate a response using Gemini"""
#         try:
#             if not self.model:
#                 return "⚠️ Gemini model is not available."

#             chat_prompt = f"{self.system_prompt}\n\nUser: {user_message}\nGeoBot:"
#             response = self.model.generate_content(chat_prompt)

#             if response and response.text.strip():
#                 return response.text.strip()

#             return ""  # Force fallback if Gemini gave nothing

#         except Exception as e:
#             return f"⚠️ Error with Gemini API: {e}"


# # Create GeoBot instance
# geo_bot = GeoBot()


# def find_html_file():
#     """Find geobot.html in common locations"""
#     html_paths = [
#         "geobot.html",
#         os.path.join(os.getcwd(), "geobot.html"),
#         os.path.join(os.path.dirname(__file__), "geobot.html"),
#         os.path.join("templates", "geobot.html"),
#         os.path.join("static", "geobot.html")
#     ]
    
#     for path in html_paths:
#         if os.path.exists(path):
#             return os.path.abspath(path)
    
#     return None


# @app.route("/chat", methods=["POST"])
# def chat():
#     """Main chat endpoint"""
#     try:
#         user_message = request.json.get("message", "").strip()
#         if not user_message:
#             return jsonify({"error": "Empty message"}), 400

#         # Step 1: Always let Gemini try first
#         gemini_response = geo_bot.generate_response(user_message)

#         if gemini_response:
#             return jsonify({
#                 "response": gemini_response,
#                 "timestamp": datetime.now().isoformat()
#             })

#         # Step 2: Fallback if Gemini fails
#         return jsonify({
#             "response": "I'm GeoBot 🌍! I usually answer geography questions, but I couldn't find an answer this time."
#         })

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# @app.route("/")
# def home():
#     """Serve the geobot.html file from templates/"""
#     return render_template("geobot.html")


# if __name__ == "__main__":
#     print("🚀 Starting GeoBot server...")
#     print("🌐 Server running on: http://127.0.0.1:5000")
    
#     # Check if HTML file exists and show status
#     html_file = find_html_file()
#     if html_file:
#         print(f"🌍 GeoBot interface found: {os.path.basename(html_file)}")
#         print("📱 Visit http://127.0.0.1:5000 to use GeoBot!")
#     else:
#         print("⚠️ geobot.html not found - check file location")
    
#     # Start Flask server
#     port = int(os.environ.get("PORT", 5000))  
#     app.run(host="0.0.0.0", port=port, debug=False)
#!/usr/bin/env python3
"""
Geography AI Chatbot Backend Server with Gemini API Integration
Fixed for Railway deployment - uses PORT environment variable and serves frontend correctly.

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
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
from flask import render_template, send_from_directory

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
            "response": "I'm GeoBot 🌍! I usually answer geography questions, but I couldn't find an answer this time."
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/")
def home():
    """Serve the frontend HTML - create inline since templates folder may not exist"""
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GeoBot 🌍 - Geography AI Assistant</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .chat-container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            width: 90%;
            max-width: 600px;
            height: 80vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        
        .chat-header {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }
        
        .chat-header h1 {
            font-size: 1.8rem;
            margin-bottom: 5px;
        }
        
        .chat-header p {
            opacity: 0.9;
            font-size: 0.9rem;
        }
        
        .chat-messages {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            background: #f8f9fa;
        }
        
        .message {
            margin-bottom: 15px;
            display: flex;
            align-items: flex-start;
        }
        
        .message.user {
            justify-content: flex-end;
        }
        
        .message-content {
            max-width: 80%;
            padding: 12px 16px;
            border-radius: 18px;
            font-size: 0.9rem;
            line-height: 1.4;
        }
        
        .message.user .message-content {
            background: #007bff;
            color: white;
            border-bottom-right-radius: 4px;
        }
        
        .message.bot .message-content {
            background: white;
            color: #333;
            border: 1px solid #e9ecef;
            border-bottom-left-radius: 4px;
        }
        
        .chat-input {
            padding: 20px;
            background: white;
            border-top: 1px solid #e9ecef;
            display: flex;
            gap: 10px;
        }
        
        .chat-input input {
            flex: 1;
            padding: 12px 16px;
            border: 2px solid #e9ecef;
            border-radius: 25px;
            outline: none;
            font-size: 0.9rem;
        }
        
        .chat-input input:focus {
            border-color: #007bff;
        }
        
        .chat-input button {
            background: #007bff;
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 25px;
            cursor: pointer;
            font-weight: 600;
            transition: background 0.3s;
        }
        
        .chat-input button:hover {
            background: #0056b3;
        }
        
        .chat-input button:disabled {
            background: #6c757d;
            cursor: not-allowed;
        }
        
        .typing {
            display: none;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .typing .message-content {
            background: white;
            border: 1px solid #e9ecef;
            padding: 12px 16px;
        }
        
        .typing-dots {
            display: flex;
            gap: 4px;
        }
        
        .typing-dots span {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #999;
            animation: typing 1.4s ease-in-out infinite both;
        }
        
        .typing-dots span:nth-child(1) { animation-delay: -0.32s; }
        .typing-dots span:nth-child(2) { animation-delay: -0.16s; }
        
        @keyframes typing {
            0%, 80%, 100% { transform: scale(0); }
            40% { transform: scale(1); }
        }
        
        .error-message {
            background: #f8d7da;
            color: #721c24;
            padding: 10px;
            border-radius: 8px;
            margin: 10px 20px;
            border: 1px solid #f5c6cb;
            text-align: center;
            font-size: 0.9rem;
        }
        
        @media (max-width: 768px) {
            .chat-container {
                width: 95%;
                height: 90vh;
            }
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <h1>GeoBot 🌍</h1>
            <p>Your friendly geography assistant</p>
        </div>
        
        <div class="chat-messages" id="chatMessages">
            <div class="message bot">
                <div class="message-content">
                    Hello! I'm GeoBot 🌍, your geography assistant. Ask me about countries, capitals, landmarks, or anything geography-related!
                </div>
            </div>
        </div>
        
        <div class="typing" id="typingIndicator">
            <div class="message-content">
                <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        </div>
        
        <div class="chat-input">
            <input type="text" id="messageInput" placeholder="Ask me about geography..." maxlength="500">
            <button id="sendButton">Send</button>
        </div>
    </div>

    <script>
        class GeoBot {
            constructor() {
                this.chatMessages = document.getElementById('chatMessages');
                this.messageInput = document.getElementById('messageInput');
                this.sendButton = document.getElementById('sendButton');
                this.typingIndicator = document.getElementById('typingIndicator');
                
                // Use current origin for API calls (works for both local and deployed)
                this.API_BASE = window.location.origin;
                
                this.initializeEventListeners();
            }
            
            initializeEventListeners() {
                this.sendButton.addEventListener('click', () => this.handleSendMessage());
                this.messageInput.addEventListener('keypress', (e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault();
                        this.handleSendMessage();
                    }
                });
            }
            
            async handleSendMessage() {
                const message = this.messageInput.value.trim();
                if (!message) return;
                
                // Add user message
                this.addMessage(message, 'user');
                this.messageInput.value = '';
                this.setLoading(true);
                
                try {
                    const response = await fetch(`${this.API_BASE}/chat`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ message: message })
                    });
                    
                    if (!response.ok) {
                        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                    }
                    
                    const data = await response.json();
                    this.addMessage(data.response, 'bot');
                    
                } catch (error) {
                    console.error('Error:', error);
                    this.addMessage(
                        `I'm having trouble connecting right now. Please check that the backend server is running. Error: ${error.message}`,
                        'bot'
                    );
                } finally {
                    this.setLoading(false);
                }
            }
            
            addMessage(content, sender) {
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${sender}`;
                
                const contentDiv = document.createElement('div');
                contentDiv.className = 'message-content';
                contentDiv.textContent = content;
                
                messageDiv.appendChild(contentDiv);
                this.chatMessages.appendChild(messageDiv);
                
                this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
            }
            
            setLoading(loading) {
                this.sendButton.disabled = loading;
                this.messageInput.disabled = loading;
                this.typingIndicator.style.display = loading ? 'flex' : 'none';
                
                if (loading) {
                    this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
                }
            }
        }
        
        // Initialize the chatbot when the page loads
        document.addEventListener('DOMContentLoaded', () => {
            new GeoBot();
        });
    </script>
</body>
</html>
    '''


@app.route("/health")
def health():
    """Health check endpoint for Railway"""
    return jsonify({"status": "healthy", "service": "GeoBot"})


if __name__ == "__main__":
    print("🚀 Starting GeoBot server...")
    
    # Use Railway's PORT environment variable, fallback to 5000 for local development
    port = int(os.environ.get("PORT", 5000))
    host = "0.0.0.0"  # Required for Railway
    
    print(f"🌐 Server running on: http://{host}:{port}")
    print("📱 Visit the URL provided by Railway to use GeoBot!")
    
    # Start Flask server
    app.run(host=host, port=port, debug=False)