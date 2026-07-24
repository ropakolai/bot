import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Paramètres",
    page_icon="⚙️",
    layout="wide"
)

st.title("⚙️ Paramètres")

st.caption("Configuration du CRM et du générateur de brouillons Gmail.")

st.divider()

# ==========================================================
# Gmail
# ==========================================================

st.header("📧 Gmail")

gmail_address = st.text_input(
    "Adresse Gmail",
    placeholder="prenom.nom@gmail.com"
)

signature = st.text_area(
    "Signature par défaut",
    height=120,
    placeholder="""Cordialement,

Valentine Martin"""
)

st.divider()

# ==========================================================
# Dossiers
# ==========================================================

st.header("📂 Dossiers")

cv_folder = st.text_input(
    "Dossier des CV",
    value="CV"
)

letter_folder = st.text_input(
    "Dossier des lettres",
    value="Lettres"
)

export_folder = st.text_input(
    "Dossier des exports",
    value="Exports"
)

st.divider()

# ==========================================================
# CRM
# ==========================================================

st.header("📊 CRM")

default_status = st.selectbox(

    "Statut par défaut",

    [
        "Brouillon créé",
        "Envoyé"
    ]

)

default_priority = st.slider(

    "Priorité par défaut",

    1,

    5,

    3

)

st.checkbox(
    "Détecter automatiquement les doublons",
    value=True
)

st.checkbox(
    "Créer automatiquement une fiche après génération du brouillon",
    value=True
)

st.divider()

# ==========================================================
# Relances
# ==========================================================

st.header("🔔 Relances")

days = st.number_input(

    "Relancer après (jours)",

    min_value=1,

    max_value=60,

    value=7

)

st.checkbox(
    "Afficher les candidatures à relancer au démarrage",
    value=True
)

st.divider()

# ==========================================================
# IA
# ==========================================================

st.header("🤖 Intelligence artificielle")

st.checkbox(
    "Activer la personnalisation IA",
    value=False
)

st.checkbox(
    "Suggérer une relance IA",
    value=False
)

st.checkbox(
    "Analyser automatiquement les offres",
    value=False
)

st.divider()

# ==========================================================
# Sauvegarde
# ==========================================================

st.header("💾 Base de données")

db = Path("candidatures.db")

if db.exists():

    size = db.stat().st_size / 1024

    st.success(f"Base détectée ({size:.1f} Ko)")

else:

    st.error("Base introuvable")

st.divider()

# ==========================================================
# Informations
# ==========================================================

st.header("ℹ️ Informations")

st.write("Version : **CRM V3**")

st.write("Base : SQLite")

st.write("Interface : Streamlit")

st.write("Gestion des brouillons : Gmail")

st.divider()

if st.button(
    "💾 Enregistrer les paramètres",
    use_container_width=True
):

    st.success(
        "Les paramètres seront persistés dans la V4."
    )