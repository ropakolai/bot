"""
sheets.py
----------
Gestion de Google Sheets pour le Mailing Bot.
"""

import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials


# ==========================================================
# Configuration
# ==========================================================

SHEET_NAME = "Mailing Bot"
WORKSHEET_NAME = "Candidatures"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


# ==========================================================
# Connexion
# ==========================================================

@st.cache_resource
def connect_sheet():
    """
    Connexion à Google Sheets.
    """

    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPES,
    )

    client = gspread.authorize(credentials)

    workbook = client.open(SHEET_NAME)

    worksheet = workbook.worksheet(WORKSHEET_NAME)

    return worksheet


# ==========================================================
# Lecture
# ==========================================================

def get_all_candidates():
    """
    Retourne toutes les candidatures.
    """

    worksheet = connect_sheet()

    records = worksheet.get_all_records()

    return pd.DataFrame(records)


# ==========================================================
# Colonnes
# ==========================================================

def get_column_index(column_name):
    """
    Retourne le numéro d'une colonne Google Sheets.
    """

    worksheet = connect_sheet()

    headers = worksheet.row_values(1)

    try:
        return headers.index(column_name) + 1

    except ValueError:
        raise Exception(f"Colonne '{column_name}' introuvable.")


# ==========================================================
# Recherche
# ==========================================================

def candidate_exists(email):
    """
    Vérifie si une candidature existe déjà.

    ATTENTION : fait une lecture complète de la feuille à chaque appel.
    Ne PAS utiliser dans une boucle sur plusieurs contacts —
    préférer get_existing_emails() + vérif en mémoire (cf. add_candidates_batch).
    """

    df = get_all_candidates()

    if df.empty:
        return False

    if "Email" not in df.columns:
        return False

    return (
        df["Email"]
        .astype(str)
        .str.strip()
        .str.lower()
        .eq(email.strip().lower())
        .any()
    )


def get_existing_emails():
    """
    Retourne l'ensemble (set) des emails déjà présents, en minuscule/strip.
    Une seule lecture complète de la feuille — à appeler UNE FOIS avant
    une boucle, plutôt que candidate_exists() par contact.
    """

    df = get_all_candidates()

    if df.empty or "Email" not in df.columns:
        return set()

    return set(
        df["Email"].astype(str).str.strip().str.lower()
    )


def get_row_from_email(email):
    """
    Retourne le numéro de ligne Google Sheets correspondant à un email.
    """

    worksheet = connect_sheet()

    emails = worksheet.col_values(get_column_index("Email"))

    # On ignore la première ligne (en-têtes)
    for row_number, value in enumerate(emails[1:], start=2):

        if str(value).strip().lower() == email.strip().lower():

            return row_number

    return None


# ==========================================================
# Ajout
# ==========================================================

def add_candidate(
    date,
    prenom,
    nom,
    entreprise,
    email,
    statut="Brouillon créé",
    poste="",
    notes="",
):
    """
    Ajoute une candidature si elle n'existe pas déjà.

    ATTENTION : fait 1 lecture complète (candidate_exists) + 1 écriture
    à chaque appel. Ne PAS utiliser dans une boucle sur plusieurs
    contacts — préférer add_candidates_batch().
    """

    if candidate_exists(email):
        return False

    worksheet = connect_sheet()

    worksheet.append_row(
        [
            date,
            prenom,
            nom,
            entreprise,
            email,
            statut,
            poste,
            notes,
        ]
    )

    return True


def add_candidates_batch(candidates):
    """
    Ajoute plusieurs candidatures en 1 seule lecture + 1 seule écriture,
    au lieu d'un aller-retour API par candidat.

    candidates : liste de dicts avec les clés
        date, prenom, nom, entreprise, email, statut (opt), poste (opt), notes (opt)

    Retourne (added_emails, skipped_emails) : les emails ajoutés et ceux
    ignorés car déjà présents dans la feuille (ou en doublon dans le lot).
    """

    existing = get_existing_emails()

    rows = []
    added = []
    skipped = []
    seen_in_batch = set()

    for c in candidates:
        email_norm = c["email"].strip().lower()

        if email_norm in existing or email_norm in seen_in_batch:
            skipped.append(c["email"])
            continue

        seen_in_batch.add(email_norm)
        added.append(c["email"])

        rows.append([
            c["date"],
            c["prenom"],
            c["nom"],
            c["entreprise"],
            c["email"],
            c.get("statut", "Brouillon créé"),
            c.get("poste", ""),
            c.get("notes", ""),
        ])

    if rows:
        worksheet = connect_sheet()
        worksheet.append_rows(rows)

    return added, skipped


# ==========================================================
# Mise à jour
# ==========================================================

def update_field(email, column_name, new_value):
    """
    Met à jour une colonne.
    """

    worksheet = connect_sheet()

    row = get_row_from_email(email)

    if row is None:
        return False

    column = get_column_index(column_name)

    worksheet.update_cell(row, column, new_value)

    return True


def update_status(email, status):
    """
    Modifie le statut.
    """

    return update_field(email, "Statut", status)


def update_notes(email, notes):
    """
    Modifie les notes.
    """

    return update_field(email, "Notes", notes)


# ==========================================================
# Suppression
# ==========================================================

def delete_candidate(email):
    """
    Supprime une candidature.
    """

    worksheet = connect_sheet()

    row = get_row_from_email(email)

    if row is None:
        return False

    worksheet.delete_rows(row)

    return True
