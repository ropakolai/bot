"""
database.py
-----------------------------------
Gestion de la base SQLite.
"""

import sqlite3

DATABASE_NAME = "candidatures.db"


def get_connection():
    """
    Ouvre une connexion SQLite.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """
    Création de la base si elle n'existe pas.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidatures (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        date_creation TEXT NOT NULL,
        date_modification TEXT NOT NULL,

        prenom TEXT NOT NULL DEFAULT '',
        nom TEXT NOT NULL DEFAULT '',

        entreprise TEXT NOT NULL DEFAULT '',
        email TEXT NOT NULL DEFAULT '',

        statut TEXT NOT NULL DEFAULT 'Brouillon créé',

        poste TEXT DEFAULT '',
        localisation TEXT DEFAULT '',

        linkedin TEXT DEFAULT '',
        site_offre TEXT DEFAULT '',

        telephone TEXT DEFAULT '',

        priorite INTEGER DEFAULT 3,

        date_envoi TEXT DEFAULT '',
        date_relance TEXT DEFAULT '',

        notes TEXT DEFAULT '',

        cv TEXT DEFAULT '',
        lettre TEXT DEFAULT ''
    )
    """)

    conn.commit()

    _upgrade_database(cursor)

    conn.commit()
    conn.close()


def _column_exists(cursor, table, column):

    cursor.execute(f"PRAGMA table_info({table})")

    cols = [row[1] for row in cursor.fetchall()]

    return column in cols


def _upgrade_database(cursor):
    """
    Ajoute automatiquement les nouvelles colonnes
    si l'utilisateur possède une ancienne base.
    """

    columns = {

        "poste": "TEXT DEFAULT ''",
        "localisation": "TEXT DEFAULT ''",
        "linkedin": "TEXT DEFAULT ''",
        "site_offre": "TEXT DEFAULT ''",
        "telephone": "TEXT DEFAULT ''",
        "priorite": "INTEGER DEFAULT 3",
        "date_envoi": "TEXT DEFAULT ''",
        "date_relance": "TEXT DEFAULT ''",
        "notes": "TEXT DEFAULT ''",
        "cv": "TEXT DEFAULT ''",
        "lettre": "TEXT DEFAULT ''"

    }

    for column, sql_type in columns.items():

        if not _column_exists(cursor, "candidatures", column):

            cursor.execute(
                f"""
                ALTER TABLE candidatures
                ADD COLUMN {column} {sql_type}
                """
            )
