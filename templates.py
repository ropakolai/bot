"""
templates.py
------------
Gestion des modèles d'e-mails stockés dans Google Sheets.
"""

import pandas as pd
from sheets import connect_sheet


WORKSHEET_NAME = "Templates"


# ==========================================================
# Feuille Templates
# ==========================================================

def connect_templates():
    """
    Retourne la feuille Google Sheets 'Templates'.
    """

    workbook = connect_sheet().spreadsheet

    return workbook.worksheet(WORKSHEET_NAME)


# ==========================================================
# Lecture
# ==========================================================

def get_templates():
    """
    Retourne tous les modèles.
    """

    worksheet = connect_templates()

    records = worksheet.get_all_records()

    return pd.DataFrame(records)


def get_template_names():
    """
    Retourne la liste des noms des modèles.
    """

    df = get_templates()

    if df.empty:
        return []

    return df["Nom"].tolist()


def get_template(name):
    """
    Retourne un modèle.
    """

    df = get_templates()

    if df.empty:
        return None

    template = df[df["Nom"] == name]

    if template.empty:
        return None

    return template.iloc[0].to_dict()


# ==========================================================
# Recherche
# ==========================================================

def template_exists(name):
    """
    Vérifie si un modèle existe.
    """

    return get_template(name) is not None


def get_row_from_name(name):
    """
    Retourne le numéro de ligne Google Sheets.
    """

    worksheet = connect_templates()

    names = worksheet.col_values(1)

    for row_number, value in enumerate(names[1:], start=2):

        if str(value).strip().lower() == name.strip().lower():

            return row_number

    return None


# ==========================================================
# Création
# ==========================================================

def create_template(name, subject, body):
    """
    Crée un nouveau modèle.
    """

    if template_exists(name):
        return False

    worksheet = connect_templates()

    worksheet.append_row(
        [
            name,
            subject,
            body,
        ]
    )

    return True


# ==========================================================
# Mise à jour
# ==========================================================

def update_template(name, subject, body):
    """
    Met à jour un modèle existant.
    """

    worksheet = connect_templates()

    row = get_row_from_name(name)

    if row is None:
        return False

    worksheet.update_cell(row, 2, subject)
    worksheet.update_cell(row, 3, body)

    return True


# ==========================================================
# Suppression
# ==========================================================

def delete_template(name):
    """
    Supprime un modèle.
    """

    worksheet = connect_templates()

    row = get_row_from_name(name)

    if row is None:
        return False

    worksheet.delete_rows(row)

    return True
