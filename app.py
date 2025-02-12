import os
import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# Configure Google API
GOOGLE_API_KEY = os.getenv("AIzaSyBCotlXtIwhvkRFPrqVY0zkVx8cJDi9T3k")
genai.configure(api_key=GOOGLE_API_KEY)

# Create the model
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "image/png",
}

model = genai.GenerativeModel("gemini-2.0-vision", generation_config=generation_config)

def generate_logo(prompt):
    response = model.generate_content(prompt)
    if response and response.parts:
        image_data = response.parts[0]
        return Image.open(io.BytesIO(image_data))
    return None

# Streamlit UI
st.title("AI Logo Generator with Google API")
st.write("Generate logos using Google's generative AI model.")

company_name = st.text_input("Enter Company Name:")
keywords = st.text_input("Enter Keywords (comma-separated):")
color = st.color_picker("Pick a Color:")
style = st.selectbox("Select Logo Style:", ["Minimalist", "Modern", "Classic", "Playful"])

if st.button("Generate Logo"):
    if company_name and keywords:
        prompt = f"Generate a logo for '{company_name}' with keywords '{keywords}' in {color} color and {style} style."
        logo = generate_logo(prompt)
        if logo:
            st.image(logo, caption="Generated Logo", use_column_width=True)
        else:
            st.error("Failed to generate logo. Try again!")
    else:
        st.warning("Please enter both company name and keywords.")
