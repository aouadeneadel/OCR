import streamlit as st
import requests
import base64
from PIL import Image
import io
import csv
from datetime import datetime

# --- CONFIGURATION OCR ---
# Si Docker utilise --network host, localhost fonctionne pour OLLAMA
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "deepseek-ocr"

# --- CONFIGURATION NEXTCLOUD ---
# Remplace par ton serveur Nextcloud / login / app password
NEXTCLOUD_SERVER = "<NEXTCLOUD_SERVER>"  # ex: 100.x.x.x ou https://cloud.mondomaine.com
NEXTCLOUD_USER = "<NEXTCLOUD_USER>"
NEXTCLOUD_PASS = "<NEXTCLOUD_APP_PASSWORD>"
NEXTCLOUD_FOLDER = "OCR-CSVs"  # dossier sur Nextcloud où stocker les CSV

# --- PAGE STREAMLIT ---
st.set_page_config(
    page_title="ABN-OCR",
    page_icon="ABN_128_128.png"
)

st.title("ABN-OCR")

# --- Logo ---
logo = Image.open("banque-du-numerique-logo_couleur.jpg")
st.image(logo, width=150)
st.caption("OCR local")

# --- Upload image ---
uploaded_file = st.file_uploader(
    "Upload une image (PNG / JPG / JPEG)",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, use_column_width=True)

    if st.button("🔍 Lancer l’OCR"):
        with st.spinner("Analyse OCR en cours…"):
            # --- Convert image to base64 ---
            buf = io.BytesIO()
            image.save(buf, format="PNG")
            img_base64 = base64.b64encode(buf.getvalue()).decode()

            payload = {
                "model": MODEL,
                "prompt": "Extract the text in the image.",
                "images": [img_base64],
                "stream": False
            }

            # --- Appel à OLLAMA ---
            try:
                r = requests.post(OLLAMA_URL, json=payload, timeout=30)
                r.raise_for_status()
                result_text = r.json().get("response", "")
            except requests.exceptions.RequestException as e:
                result_text = f"❌ Erreur lors de la requête OCR : {e}"

        # --- Affichage OCR ---
        st.text_area("📝 Texte reconnu", result_text, height=300)

        # --- Génération CSV ---
        csv_buffer = io.StringIO()
        writer = csv.writer(csv_buffer)
        for line in result_text.splitlines():
            writer.writerow([line])
        csv_data = csv_buffer.getvalue()

        # --- Nom de fichier horodaté ---
        filename = f"ocr_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        # --- Upload sur Nextcloud via WebDAV ---
        nextcloud_url = f"https://{NEXTCLOUD_SERVER}/remote.php/webdav/{NEXTCLOUD_FOLDER}/{filename}"
        try:
            response = requests.put(
                nextcloud_url,
                data=csv_data.encode("utf-8"),
                auth=(NEXTCLOUD_USER, NEXTCLOUD_PASS)
            )
            if response.status_code in [200, 201, 204]:
                st.success(f"✅ CSV uploadé sur Nextcloud : {filename}")
            else:
                st.error(f"❌ Erreur upload Nextcloud : {response.status_code} {response.text}")
        except Exception as e:
            st.error(f"❌ Exception lors de l’upload Nextcloud : {e}")

        # --- Bouton téléchargement local CSV ---
        st.download_button(
            "⬇️ Télécharger CSV localement",
            csv_data,
            file_name=filename,
            mime="text/csv"
        )
