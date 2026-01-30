# ABN-OCR
Solution OCR locale et sécurisée

## Présentation

ABN-OCR est une application de reconnaissance optique de caractères (OCR)
fonctionnant entièrement en local. Elle permet l’extraction de texte à partir
d’images tout en garantissant la confidentialité des données.

La solution repose sur Streamlit pour l’interface utilisateur et Ollama pour
l’exécution des modèles IA.

## Fonctionnalités

- Interface web simple et ergonomique
- Import d’images PNG / JPG / JPEG
- OCR local via Ollama
- Visualisation du texte reconnu
- Export des résultats au format CSV
- Aucune transmission de données vers l’extérieur

## Architecture

Utilisateur
→ Interface Streamlit
→ OCR local via Ollama
→ Résultat texte + export CSV

## Prérequis

- Python 3.9 ou supérieur
- Ollama installé localement
- Modèle OCR compatible vision (ex: deepseek-ocr)

## Structure du projet
.
├── app.py
├── README.md
├── ABN_128_128.png
├── banque-du-numerique-logo_couleur.jpg


Installation du modèle :
```bash
ollama pull deepseek-ocr
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install streamlit requests pillow
streamlit run app.py
```
## Accès via navigateur
http://localhost:8501

## Sécurité et conformité
###  Traitement 100 % local
### Aucune donnée transmise vers l’extérieur
### Compatible avec des environnements sensibles (finance, juridique, secteur public)
### Déploiement possible sur poste utilisateur ou serveur interne

