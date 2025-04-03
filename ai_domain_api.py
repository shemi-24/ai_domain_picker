from flask import Flask, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API Key
API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Flask app
app = Flask(__name__)

# Configure Gemini AI
if not API_KEY:
    raise ValueError("❌ API Key not found. Please set the GEMINI_API_KEY environment variable.")
genai.configure(api_key=API_KEY)

# Define Route for Domain Name Generation
@app.route('/generate', methods=['POST'])
def generate_domains():
    try:
        # Get user input (keyword) from request
        data = request.get_json()
        keyword = data.get("keyword", "").strip()
        description = data.get("description")
        style = data.get("style")

        if not keyword:
            return jsonify({"error": "Keyword is required"}), 400

        # Initialize Gemini Model
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Generate Domain Name Ideas
        response = model.generate_content(
            f"""
            I am creating a website about {description}.
            I want the domain name to sound {style}.
            It should include the keyword {keyword} if provided.
            Suggest 25 unique domain names, including variations with .com, .net, .ai, .io, and other creative extensions.
            Ensure the names are brandable, catchy, and easy to remember.
            """
        )

        # Return JSON response
        return jsonify({"keyword": keyword, "domain_suggestions": response.text.strip().split("\n")})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run Flask App
if __name__ == '__main__':
    app.run(debug=True)
