"""
tracking.py
-----------------------------------
Toutes les opérations sur la base SQLite.
"""

from datetime import datetime
import pandas as pd

from database import get_connection


# ==========================================================
# Ajouter une candidature
# ==========================================================

def add_candidate(
    prenom="",
    nom="",
    entreprise="",
    email="",
    poste="",
    localisation="",
    linkedin="",
    site_offre="",
    telephone="",
    cv="",
    lettre=""
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM candidatures
        WHERE email = ?
        AND entreprise = ?
        """,
        (email, entreprise)
    )

    if cursor.fetchone():
        conn.close()
        return False

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        """
        INSERT INTO candidatures (

            date_creation,
            date_modification,

            prenom,
            nom,

            entreprise,
            email,

            statut,

            poste,
            localisation,

            linkedin,
            site_offre,

            telephone,

            cv,
            lettre

        )

        VALUES (
            ?,?,?,?,?,?,?,?,?,?,?,?,?,?
        )
        """,
        (

            now,
            now,

            prenom,
            nom,

            entreprise,
            email,

            "Brouillon créé",

            poste,
            localisation,

            linkedin,
            site_offre,

            telephone,

            cv,
            lettre

        )

    )

    conn.commit()
    conn.close()

    return True


# ==========================================================
# Toutes les candidatures
# ==========================================================

def get_candidates():

    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT *
        FROM candidatures
        ORDER BY date_creation DESC
        """,
        conn
    )

    conn.close()

    return df


# ==========================================================
# Une candidature
# ==========================================================

def get_candidate(candidate_id):

    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT *
        FROM candidatures
        WHERE id=?
        """,
        conn,
        params=(candidate_id,)
    )

    conn.close()

    if df.empty:
        return None

    return df.iloc[0]


# ==========================================================
# Recherche
# ==========================================================

def search_candidates(search):

    conn = get_connection()

    value = f"%{search}%"

    df = pd.read_sql_query(
        """
        SELECT *
        FROM candidatures

        WHERE

            prenom LIKE ?
            OR nom LIKE ?
            OR entreprise LIKE ?
            OR email LIKE ?
            OR poste LIKE ?
            OR localisation LIKE ?

        ORDER BY date_creation DESC
        """,
        conn,
        params=(
            value,
            value,
            value,
            value,
            value,
            value
        )
    )

    conn.close()

    return df


# ==========================================================
# Modifier le statut
# ==========================================================

def update_status(candidate_id, statut):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE candidatures

        SET

            statut=?,
            date_modification=?

        WHERE id=?
        """,
        (
            statut,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            candidate_id
        )
    )

    conn.commit()
    conn.close()


# ==========================================================
# Mettre à jour une candidature
# ==========================================================

def update_candidate(candidate_id, **fields):

    if not fields:
        return

    fields["date_modification"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_connection()
    cursor = conn.cursor()

    sql = ", ".join(f"{k}=?" for k in fields.keys())

    values = list(fields.values())
    values.append(candidate_id)

    cursor.execute(
        f"""
        UPDATE candidatures
        SET {sql}
        WHERE id=?
        """,
        values
    )

    conn.commit()
    conn.close()


# ==========================================================
# Supprimer
# ==========================================================

def delete_candidate(candidate_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM candidatures
        WHERE id=?
        """,
        (candidate_id,)
    )

    conn.commit()
    conn.close()


# ==========================================================
# Statistiques
# ==========================================================

def get_statistics():

    conn = get_connection()
    cursor = conn.cursor()

    stats = {}

    cursor.execute(
        "SELECT COUNT(*) FROM candidatures"
    )
    stats["total"] = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(DISTINCT entreprise) FROM candidatures"
    )
    stats["entreprises"] = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM candidatures
        WHERE statut='Entretien'
        """
    )
    stats["entretiens"] = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM candidatures
        WHERE statut='Offre'
        """
    )
    stats["offres"] = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM candidatures
        WHERE statut='Refus'
        """
    )
    stats["refus"] = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM candidatures
        WHERE statut='Réponse reçue'
        """
    )
    stats["reponses"] = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM candidatures
        WHERE statut='Envoyé'
        """
    )
    stats["envoyes"] = cursor.fetchone()[0]

    conn.close()

    return stats


# ==========================================================
# Export Excel
# ==========================================================

def export_dataframe():

    return get_candidates()
