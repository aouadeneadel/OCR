#!/bin/bash

# Script pour installer et configurer un environnement Python pour l'extraction de texte (OCR)

# Vérifier si l'utilisateur est root (ou utilise sudo)
if [ "$(id -u)" -ne 0 ]; then
    echo "Certaines commandes nécessitent les droits root. Vous serez invité à entrer votre mot de passe si nécessaire."
fi

# Mettre à jour les paquets (Linux)
if [ -f /etc/os-release ]; then
    sudo apt update && sudo apt upgrade -y
fi

# Installer les dépendances système
echo "Installation des dépendances système..."
if command -v apt &> /dev/null; then
    # Ubuntu/Debian
    sudo apt install -y python3 python3-pip python3-venv libtesseract-dev tesseract-ocr tesseract-ocr-fra libopencv-dev
elif command -v brew &> /dev/null; then
    # macOS
    brew install python tesseract opencv
else
    echo "Système non supporté. Veuillez installer manuellement Python, Tesseract et OpenCV."
    exit 1
fi

# Créer un dossier pour le projet
PROJECT_DIR="$HOME/ocr_project"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR" || exit

# Créer un environnement virtuel Python
echo "Création de l'environnement virtuel Python..."
python3 -m venv venv

# Activer l'environnement virtuel
source venv/bin/activate

# Installer les dépendances Python
echo "Installation des dépendances Python..."
pip install --upgrade pip
pip install easyocr pandas streamlit pillow opencv-python pytesseract torch torchvision torchaudio

# Vérifier l'installation de Tesseract
if ! command -v tesseract &> /dev/null; then
    echo "Tesseract n'est pas installé. Veuillez l'installer manuellement."
    echo "Sur Ubuntu/Debian : sudo apt install tesseract-ocr tesseract-ocr-fra"
    echo "Sur macOS : brew install tesseract"
    exit 1
fi

# Afficher les informations de configuration
echo ""
echo "=== Configuration terminée ==="
echo "Dossier du projet : $PROJECT_DIR"
echo "Pour activer l'environnement virtuel, exécutez :"
echo "  cd $PROJECT_DIR"
echo "  source venv/bin/activate"
echo ""
echo "Pour exécuter ton script Streamlit :"
echo "  streamlit run ton_script.py"
echo ""

# Désactiver l'environnement virtuel (optionnel)
deactivate
