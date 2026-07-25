from google.oauth2 import service_account
from googleapiclient.discovery import build
import streamlit as st

# ID du dossier "Mailing"
ROOT_FOLDER_ID = "1FL7plV0kL-DENOts4RwUjYYjCdrI-B45"


# --------------------------------------------------------
# Connexion Google Drive
# --------------------------------------------------------

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]


def get_drive_service():

    info = dict(st.secrets["gcp_service_account"])

    # Streamlit remplace les retours à la ligne par \n
    info["private_key"] = info["private_key"].replace("\\n", "\n")

    credentials = service_account.Credentials.from_service_account_info(
        info,
        scopes=SCOPES,
    )

    return build("drive", "v3", credentials=credentials)


# --------------------------------------------------------
# Recherche d'un sous-dossier
# --------------------------------------------------------

def get_subfolder_id(parent_id, folder_name):

    service = get_drive_service()

    query = (
        f"'{parent_id}' in parents "
        f"and mimeType='application/vnd.google-apps.folder' "
        f"and name='{folder_name}' "
        f"and trashed=false"
    )

    results = service.files().list(
        q=query,
        fields="files(id,name)"
    ).execute()

    files = results.get("files", [])

    if not files:
        raise Exception(f"Dossier '{folder_name}' introuvable.")

    return files[0]["id"]


# --------------------------------------------------------
# Liste des PDF d'un dossier
# --------------------------------------------------------

def list_pdf_files(folder_name):

    service = get_drive_service()

    folder_id = get_subfolder_id(ROOT_FOLDER_ID, folder_name)

    query = (
        f"'{folder_id}' in parents "
        f"and mimeType='application/pdf' "
        f"and trashed=false"
    )

    results = service.files().list(
        q=query,
        orderBy="name",
        fields="files(id,name)"
    ).execute()

    return results.get("files", [])


# --------------------------------------------------------
# Raccourcis
# --------------------------------------------------------

def get_cvs():
    return list_pdf_files("CV")


def get_letters():
    return list_pdf_files("Lettres")
