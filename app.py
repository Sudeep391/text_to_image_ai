import streamlit as st
import requests
import os
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HF_API_KEY = os.getenv("HF_API_KEY")

# -------------------------------
# Function: Enhance Prompt (Groq)
# -------------------------------
def enhance_prompt(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "Enhance image prompts for AI art generation."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    return result ["choices"] [0]["message"]["content"]


# -------------------------------
# Function: Generate Image
# -------------------------------
def generate_image(prompt):
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
    
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}"
    }

    payload = {"inputs": prompt}

    response = requests.post(API_URL, headers=headers, json=payload)

    return Image.open(BytesIO(response.content))


# -------------------------------
# Streamlit UI
# -------------------------------
st.title("🎨 Text to Image Generator")
st.write("Generate images using AI + Groq-enhanced prompts")

user_prompt = st.text_input("Enter your prompt:")

if st.button("Generate Image"):
    if user_prompt:
        with st.spinner("Enhancing prompt with Groq..."):
            enhanced = enhance_prompt(user_prompt)

        st.subheader("✨ Enhanced Prompt")
        st.write(enhanced)

        with st.spinner("Generating image..."):
            image = generate_image(enhanced)

        st.image(image, caption="Generated Image", use_column_width=True)
    else:
        st.warning("Please enter a prompt!")
