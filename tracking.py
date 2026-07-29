"""
tracking.py
------------
Gestion des candidatures.
Ce fichier fait le lien entre l'interface Streamlit
et Google Sheets.
"""
from sheets import (
    add_candidate as sheet_add_candidate,
    add_candidates_batch as sheet_add_candidates_batch,
    get_all_candidates,
    get_existing_emails as sheet_get_existing_emails,
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

    ATTENTION : fait 1 lecture complète + 1 écriture à chaque appel.
    Pour ajouter plusieurs candidatures (ex. boucle sur un CSV importé),
    utiliser add_candidates_batch() à la place.
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


def add_candidates_batch(candidates):
    """
    Ajoute plusieurs candidatures en 1 seule lecture + 1 seule écriture.

    candidates : liste de dicts avec les clés
        date, prenom, nom, entreprise, email, statut (opt), poste (opt), notes (opt)

    Retourne (added_emails, skipped_emails).
    """
    return sheet_add_candidates_batch(candidates)


def get_existing_emails():
    """
    Retourne l'ensemble des emails déjà présents (1 seule lecture).
    À appeler une fois avant une boucle de traitement.
    """
    return sheet_get_existing_emails()

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
