import gspread
import streamlit as st
from google.oauth2.service_account import Credentials
from datetime import datetime

# -------------------------------------------------------------------
# Configuration Google Sheets
# -------------------------------------------------------------------

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets"
]

SPREADSHEET_ID = "119kBV5RBKBAl1tYYJ4W9TKerVmi2CZS1m4suDRXFQUs"

# -------------------------------------------------------------------
# Connexion
# -------------------------------------------------------------------

def connect_sheet(sheet_name):
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPES,
    )

    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(SPREADSHEET_ID)

    return spreadsheet.worksheet(sheet_name)


# -------------------------------------------------------------------
# Feuilles
# -------------------------------------------------------------------

def campaigns_sheet():
    return connect_sheet("Campagnes")


def scheduling_sheet():
    return connect_sheet("Programmation")


# -------------------------------------------------------------------
# Campagnes
# -------------------------------------------------------------------

def add_draft_to_campaign(
    campaign,
    email,
    firstname,
    lastname,
    subject,
    body,
    cv_id,
    letter_id,
):
    """
    Ajoute un mail à la campagne.
    Le brouillon sera créé ensuite par Google Apps Script.
    """

    worksheet = campaigns_sheet()

    worksheet.append_row([
    campaign,
    email,
    firstname,
    lastname,
    subject,
    body,
    "",                         # Draft ID
    "A créer",                  # Statut
    datetime.now().isoformat(), # Date création
    "",                         # Date brouillon
    "",                         # Date envoi
    cv_id,                      # CV ID
    letter_id                   # LETTER ID
    ])


def get_campaign_drafts(campaign):
    """
    Retourne tous les mails d'une campagne.
    """

    rows = campaigns_sheet().get_all_records()

    return [
        row
        for row in rows
        if row["Campagne"] == campaign
    ]


def update_draft_id(email, draft_id):
    """
    Enregistre le Draft ID créé par Apps Script.
    """

    ws = campaigns_sheet()

    rows = ws.get_all_records()

    for i, row in enumerate(rows, start=2):

        if row["Email"] == email and row["Draft ID"] == "":

            ws.update_cell(i, 7, draft_id)
            return True

    return False


def update_draft_status(draft_id, status):
    """
    Met à jour le statut d'un brouillon.
    """

    ws = campaigns_sheet()

    rows = ws.get_all_records()

    for i, row in enumerate(rows, start=2):

        if row["Draft ID"] == draft_id:

            ws.update_cell(i, 8, status)
            return True

    return False


def update_draft_creation_date(draft_id):
    """
    Enregistre la date de création du brouillon.
    """

    ws = campaigns_sheet()

    rows = ws.get_all_records()

    for i, row in enumerate(rows, start=2):

        if row["Draft ID"] == draft_id:

            ws.update_cell(i, 10, datetime.now().isoformat())
            return True

    return False


def update_send_date(draft_id):
    """
    Enregistre la date d'envoi du mail.
    """

    ws = campaigns_sheet()

    rows = ws.get_all_records()

    for i, row in enumerate(rows, start=2):

        if row["Draft ID"] == draft_id:

            ws.update_cell(i, 11, datetime.now().isoformat())
            return True

    return False


# -------------------------------------------------------------------
# Programmation
# -------------------------------------------------------------------

def create_campaign(
    campaign,
    send_date,
    send_time,
    status="Programmée"
):
    """
    Crée une nouvelle campagne.
    """

    scheduling_sheet().append_row([
        campaign,
        send_date,
        send_time,
        status
    ])


def get_scheduled_campaigns():
    """
    Retourne toutes les campagnes programmées.
    """

    return scheduling_sheet().get_all_records()


def update_campaign_status(campaign, status):
    """
    Met à jour le statut d'une campagne.
    """

    ws = scheduling_sheet()

    rows = ws.get_all_records()

    for i, row in enumerate(rows, start=2):

        if row["Campagne"] == campaign:

            ws.update_cell(i, 4, status)
            return True

    return False
