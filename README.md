# ABN-OCR  
## Note DSI / RSSI – Sécurité & Conformité

---

## 1. Objet du document

Ce document décrit les caractéristiques de sécurité, de conformité et
d’architecture de la solution **ABN-OCR**, afin d’évaluer son adéquation avec
les exigences DSI / RSSI en environnement professionnel ou institutionnel.

---

## 2. Description synthétique de la solution

ABN-OCR est une application de reconnaissance optique de caractères (OCR)
fonctionnant **exclusivement en local**.

Elle permet l’extraction de texte à partir d’images via un modèle d’IA exécuté
localement (Ollama), sans dépendance à un service cloud externe.

---

## 3. Périmètre fonctionnel

- Import d’images (PNG, JPG, JPEG)
- Traitement OCR local
- Restitution du texte à l’utilisateur
- Export au format CSV
- Interface web locale (Streamlit)

Hors périmètre :
- Authentification utilisateur
- Gestion des habilitations
- Archivage long terme
- Sauvegarde automatique

---

## 4. Architecture technique

### 4.1 Composants

- **Interface utilisateur** : Streamlit (port local 8501)
- **Moteur OCR / IA** : Ollama (port local 11434)
- **Traitement image** : Pillow
- **Formats de sortie** : Texte brut, CSV

### 4.2 Schéma de flux

Utilisateur  
→ Navigateur web  
→ Application Streamlit (local)  
→ Service Ollama (local)  
→ Résultat OCR (local)

---

## 5. Sécurité des données

### 5.1 Localisation des données

- Les images importées ne quittent jamais le poste ou le serveur
- Les données OCR sont traitées en mémoire
- Aucun stockage persistant imposé par l’application
- Aucun appel réseau externe

### 5.2 Confidentialité

- Aucun transfert vers Internet
- Aucun service SaaS
- Compatible documents sensibles :
  - données financières
  - données juridiques
  - données internes
  - informations réglementées

---

## 6. Réseau & communications

- Communication HTTP locale uniquement :
  - `localhost:8501` (Streamlit)
  - `localhost:11434` (Ollama)
- Aucun flux sortant requis
- Fonctionne hors ligne après installation du modèle

---

## 7. Gestion des accès

- Accès par défaut : utilisateur local
- Pas d’authentification intégrée
- Le contrôle d’accès est délégué à :
  - l’OS
  - le poste utilisateur
  - ou l’infrastructure interne (reverse proxy, VPN, bastion)

---

## 8. Journalisation & traçabilité

Par défaut :
- Pas de logs applicatifs persistants
- Pas de traçabilité utilisateur

Évolutions possibles :
- Ajout de logs applicatifs
- Journalisation des traitements OCR
- Horodatage et identification utilisateur

---

## 9. Conformité réglementaire

La solution est compatible avec :
- RGPD (pas de transfert externe)
- Exigences de souveraineté des données
- Environnements à données sensibles

Responsabilité du déploiement :
- Paramétrage OS
- Sécurisation du poste ou du serveur
- Politique de conservation des fichiers exportés

---

## 10. Déploiement recommandé

- Poste utilisateur sécurisé
- Serveur interne isolé
- VM ou conteneur (Docker possible)
- Accès restreint au réseau local

---

## 11. Analyse de risques (synthèse)

| Risque | Niveau | Mesure |
|------|-------|-------|
| Fuite de données | Faible | Traitement 100 % local |
| Accès non autorisé | Moyen | Contrôle par l’infrastructure |
| Mauvais usage | Moyen | Procédures internes |
| Perte de données | Faible | Export manuel contrôlé |

---

## 12. Évolutions de sécurité possibles

- Authentification (LDAP / SSO)
- Gestion des rôles
- Chiffrement des exports
- Audit et journalisation
- Déploiement containerisé durci

---

## 13. Conclusion DSI / RSSI

ABN-OCR est une solution :
- **souveraine**
- **hors cloud**
- **à faible surface d’attaque**
- **adaptée aux environnements sensibles**

Elle peut être déployée sous réserve des contrôles habituels
d’infrastructure et de sécurité poste / serveur.
