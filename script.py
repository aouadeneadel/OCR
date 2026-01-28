import easyocr
import pandas as pd
import streamlit as st
import cv2
import numpy as np
from PIL import Image
import tempfile

def extraire_texte_depuis_image(image):
    """Extraire le texte depuis une image en utilisant EasyOCR."""
    # Convertir l'image téléversée en tableau NumPy
    image_np = np.array(image)
    reader = easyocr.Reader(['fr'])  # Initialiser le lecteur pour le français
    result = reader.readtext(image_np)
    texte_extraits = [detection[1] for detection in result]
    return texte_extraits

def convertir_en_csv(texte_extraits, nom_donateur="CASA", chemin_sortie='sortie.csv'):
    """
    Convertir le texte extrait en un fichier CSV structuré.
    Le paramètre `nom_donateur` permet de spécifier le nom à rechercher dans le texte.
    """
    données = []
    for texte in texte_extraits:
        if nom_donateur in texte and len(texte.split()) >= 3:
            parties = texte.split()
            données.append({
                "Nom Donateur": parties[0],
                "N° Série": parties[1],
                "N° Inventaire ABN": parties[2]
            })

    df = pd.DataFrame(données)
    df.to_csv(chemin_sortie, index=False)
    return df, chemin_sortie

def main():
    """Interface Streamlit pour téléverser une image et extraire le texte."""
    st.title("Outil d'extraction de texte depuis une image")

    uploaded_file = st.file_uploader("Choisir une image...", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        # Afficher l'image téléversée
        image = Image.open(uploaded_file)
        st.image(image, caption="Image téléchargée", use_column_width=True)

        # Champ pour spécifier le nom du donateur
        nom_donateur = st.text_input("Nom du donateur (par exemple, CASA) :", "CASA")

        # Extraire le texte
        st.write("Extraction en cours...")
        texte_extraits = extraire_texte_depuis_image(image)

        # Afficher le texte extrait
        st.write("Texte extrait :")
        st.write(texte_extraits)

        # Convertir en CSV
        df, chemin_sortie = convertir_en_csv(texte_extraits, nom_donateur)

        # Afficher les données structurées
        st.write("Données structurées :")
        st.dataframe(df)

        # Bouton pour télécharger le CSV
        csv = df.to_csv(index=False)
        st.download_button(
            label="Télécharger le CSV",
            data=csv,
            file_name=chemin_sortie,
            mime='text/csv',
        )

if __name__ == "__main__":
    main()
