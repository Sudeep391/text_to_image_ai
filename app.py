import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# 🔑 Add your Hugging Face API Key here
API_KEY = "YOUR_HUGGINGFACE_API_KEY"

# 🎯 Model (Stable Diffusion)
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

# 🎨 Function to generate image
def generate_image(prompt):
    payload = {"inputs": prompt}

    try:
        response = requests.post(API_URL, headers=headers, json=payload)

        # 🔍 Debug content type
        content_type = response.headers.get("content-type", "")

        # ✅ If image returned
        if "image" in content_type:
            return Image.open(BytesIO(response.content))

        # ❌ If error returned (JSON / text)
        else:
            st.error("API Error:")
            st.code(response.text)
            return None

    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None


# 🌐 Streamlit UI
st.set_page_config(page_title="Text to Image Generator", layout="centered")

st.title("🖼️ AI Text-to-Image Generator")
st.write("Enter a prompt and generate an image using AI")

# ✍️ User input
prompt = st.text_area("Enter your prompt:", "A futuristic city with flying cars, neon lights")

# 🚀 Generate button
if st.button("Generate Image"):
    if prompt.strip() == "":
        st.warning("Please enter a prompt")
    else:
        with st.spinner("Generating image..."):
            image = generate_image(prompt)

            if image:
                st.image(image, caption="Generated Image", use_column_width=True)
