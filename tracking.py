"""
tracking.py
------------
Gestion des candidatures.

Ce fichier fait le lien entre l'interface Streamlit
et Google Sheets.
"""

from sheets import (
    add_candidate as sheet_add_candidate,
    get_all_candidates,
    update_status as sheet_update_status,
    update_notes as sheet_update_notes,
    delete_candidate as sheet_delete_candidate,
    candidate_exists
)


# ==========================================================
# Lecture
# ==========================================================

def get_candidates():
    """
    Retourne toutes les candidatures.
    """
    return get_all_candidates()


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
    notes=""
):
    """
    Ajoute une candidature.
    """

    return sheet_add_candidate(
        date=date,
        prenom=prenom,
        nom=nom,
        entreprise=entreprise,
        email=email,
        statut=statut,
        poste=poste,
        notes=notes,
    )


# ==========================================================
# Mise à jour
# ==========================================================

def update_status(email, statut):
    """
    Modifie le statut.
    """

    return sheet_update_status(email, statut)


def update_notes(email, notes):
    """
    Modifie les notes.
    """

    return sheet_update_notes(email, notes)


# ==========================================================
# Suppression
# ==========================================================

def delete_candidate(email):
    """
    Supprime une candidature.
    """

    return sheet_delete_candidate(email)


# ==========================================================
# Vérification
# ==========================================================

def exists(email):
    """
    Vérifie si une candidature existe.
    """

    return candidate_exists(email)
