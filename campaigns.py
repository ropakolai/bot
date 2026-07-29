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
# Connexion (mise en cache : 1 seule fois par session Streamlit)
# -------------------------------------------------------------------

@st.cache_resource
def _get_spreadsheet():
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPES,
    )
    client = gspread.authorize(creds)
    return client.open_by_key(SPREADSHEET_ID)


def connect_sheet(sheet_name):
    """
    Retourne un worksheet depuis le classeur déjà ouvert (mis en cache).
    N'appelle plus l'API à chaque fois.
    """
    return _get_spreadsheet().worksheet(sheet_name)


# -------------------------------------------------------------------
# Feuilles
# -------------------------------------------------------------------

def campaigns_sheet():
    return connect_sheet("Campagnes")


def scheduling_sheet():
    return connect_sheet("Programmation")


# -------------------------------------------------------------------
# Campagnes — écriture unitaire
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


def add_drafts_to_campaign_batch(campaign, rows):
    """
    Ajoute plusieurs mails à la campagne en une seule requête API.

    rows : liste de dicts avec les clés
        email, firstname, lastname, subject, body, cv_id, letter_id
    """

    worksheet = campaigns_sheet()
    now = datetime.now().isoformat()

    values = [
        [
            campaign,
            r["email"],
            r["firstname"],
            r["lastname"],
            r["subject"],
            r["body"],
            "",           # Draft ID
            "A créer",    # Statut
            now,          # Date création
            "",           # Date brouillon
            "",           # Date envoi
            r["cv_id"],
            r["letter_id"],
        ]
        for r in rows
    ]

    if values:
        worksheet.append_rows(values)


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


# -------------------------------------------------------------------
# Campagnes — mises à jour unitaires (gardées pour compatibilité,
# mais évitez de les appeler dans une boucle : préférez les versions
# batch ci-dessous)
# -------------------------------------------------------------------

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
# Campagnes — mises à jour PAR LOT (1 lecture + 1 écriture pour N lignes)
# -------------------------------------------------------------------

def update_draft_ids_batch(email_to_draft_id: dict):
    """
    Enregistre plusieurs Draft ID en une seule lecture + une seule écriture.

    email_to_draft_id : { email: draft_id }
    """

    ws = campaigns_sheet()
    rows = ws.get_all_records()

    cells = []
    for i, row in enumerate(rows, start=2):
        email = row["Email"]
        if email in email_to_draft_id and row["Draft ID"] == "":
            cells.append(gspread.Cell(row=i, col=7, value=email_to_draft_id[email]))

    if cells:
        ws.update_cells(cells)

    return len(cells)


def update_draft_statuses_batch(draft_id_to_status: dict):
    """
    Met à jour le statut de plusieurs brouillons.

    draft_id_to_status : { draft_id: status }
    """

    ws = campaigns_sheet()
    rows = ws.get_all_records()

    cells = []
    for i, row in enumerate(rows, start=2):
        draft_id = row["Draft ID"]
        if draft_id in draft_id_to_status:
            cells.append(gspread.Cell(row=i, col=8, value=draft_id_to_status[draft_id]))

    if cells:
        ws.update_cells(cells)

    return len(cells)


def update_draft_creation_dates_batch(draft_ids: list):
    """
    Enregistre la date de création du brouillon pour plusieurs Draft ID.
    """

    ws = campaigns_sheet()
    rows = ws.get_all_records()
    now = datetime.now().isoformat()

    draft_ids = set(draft_ids)

    cells = []
    for i, row in enumerate(rows, start=2):
        if row["Draft ID"] in draft_ids:
            cells.append(gspread.Cell(row=i, col=10, value=now))

    if cells:
        ws.update_cells(cells)

    return len(cells)


def update_send_dates_batch(draft_ids: list):
    """
    Enregistre la date d'envoi pour plusieurs Draft ID.
    """

    ws = campaigns_sheet()
    rows = ws.get_all_records()
    now = datetime.now().isoformat()

    draft_ids = set(draft_ids)

    cells = []
    for i, row in enumerate(rows, start=2):
        if row["Draft ID"] in draft_ids:
            cells.append(gspread.Cell(row=i, col=11, value=now))

    if cells:
        ws.update_cells(cells)

    return len(cells)


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
