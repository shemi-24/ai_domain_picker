import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv



# Load environment variables
load_dotenv()

# Set up Streamlit app title
st.title("🌐 AI-Powered Domain Name Generator")

# Securely Get API Key
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("❌ API Key not found. Please set the GEMINI_API_KEY environment variable.")
else:
    genai.configure(api_key=API_KEY)

    # User Input
    keyword = st.text_input("Enter a name to generate domain ideas:")

    # Button to generate domains
    if st.button("Generate Domains",key="generate") and keyword.strip():
        with st.spinner("Generating domain names..."):
            try:
                # Initialize Gemini Model
                model = genai.GenerativeModel("gemini-1.5-flash")

                # Generate Domain Ideas
                response = model.generate_content(
                    f"Suggest 25 creative domain name ideas for '{keyword}', including variations with .com, .net, .ai, and unique extensions."
                )

                # Display Results
                st.subheader("🔹 Suggested Domain Names:")
                st.write(response.text)

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
   
