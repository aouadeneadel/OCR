import streamlit as st
import requests
import base64
from PIL import Image
import io
import csv

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "deepseek-ocr"

# --- Page configuration ---
st.set_page_config(
    page_title="ABN-OCR", 
    page_icon="ABN_128_128.png"  # This works if it's in the same folder
)

st.title("ABN-OCR")

# --- Load and display logo ---
logo = Image.open("banque-du-numerique-logo_couleur.jpg")  # Local file
st.image(logo, width=150)
st.caption("OCR local")

uploaded_file = st.file_uploader(
    "Upload une image (PNG / JPG)",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, use_column_width=True)

    if st.button("🔍 Lancer l’OCR"):
        with st.spinner("Analyse OCR en cours…"):
            # Convert image to base64
            buf = io.BytesIO()
            image.save(buf, format="PNG")
            img_base64 = base64.b64encode(buf.getvalue()).decode()

            payload = {
                "model": MODEL,
                "prompt": "Extract the text in the image.",
                "images": [img_base64],
                "stream": False
            }

            r = requests.post(OLLAMA_URL, json=payload)

            if r.status_code == 200:
                result_text = r.json()["response"]
            else:
                result_text = f"❌ Erreur {r.status_code}\n{r.text}"

        # Display OCR text
        st.text_area("📝 Texte reconnu", result_text, height=300)

        # Convert OCR text to CSV
        csv_buffer = io.StringIO()
        writer = csv.writer(csv_buffer)

        # Simple splitting by lines, adjust if your OCR returns structured text
        for line in result_text.splitlines():
            # If you want each word in a separate column, use: writer.writerow(line.split())
            writer.writerow([line])  # Each line in one row

        csv_data = csv_buffer.getvalue()

        # Download CSV
        st.download_button(
            "⬇️ Télécharger CSV",
            csv_data,
            file_name="ocr.csv",
            mime="text/csv"
        )

