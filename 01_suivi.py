import streamlit as st
import pandas as pd

from tracking import (
    get_candidates,
    get_statistics,
    update_candidate,
    delete_candidate
)

st.set_page_config(
    page_title="Suivi des candidatures",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Suivi des candidatures")

# ==========================================================
# Statistiques
# ==========================================================

stats = get_statistics()

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "📨 Candidatures",
    stats["total"]
)

c2.metric(
    "🏢 Entreprises",
    stats["entreprises"]
)

c3.metric(
    "🟣 Entretiens",
    stats["entretiens"]
)

c4.metric(
    "🟢 Offres",
    stats["offres"]
)

st.divider()

# ==========================================================
# Chargement
# ==========================================================

df = get_candidates()

if df.empty:

    st.info("Aucune candidature enregistrée.")

    st.stop()

# ==========================================================
# Barre d'outils
# ==========================================================

left, right = st.columns([3, 1])

with left:

    search = st.text_input(
        "Recherche",
        placeholder="Nom, entreprise, email, poste..."
    )

with right:

    statut = st.selectbox(
        "Statut",
        [
            "Tous",
            "Brouillon créé",
            "Envoyé",
            "Réponse reçue",
            "Entretien",
            "Offre",
            "Refus"
        ]
    )

# ==========================================================
# Recherche
# ==========================================================

if search:

    mask = (

        df["prenom"].str.contains(
            search,
            case=False,
            na=False
        )

        |

        df["nom"].str.contains(
            search,
            case=False,
            na=False
        )

        |

        df["entreprise"].str.contains(
            search,
            case=False,
            na=False
        )

        |

        df["email"].str.contains(
            search,
            case=False,
            na=False
        )

        |

        df["poste"].str.contains(
            search,
            case=False,
            na=False
        )

    )

    df = df[mask]

# ==========================================================
# Filtre
# ==========================================================

if statut != "Tous":

    df = df[
        df["statut"] == statut
    ]

# ==========================================================
# Colonnes affichées
# ==========================================================

display = df[
    [
        "id",
        "prenom",
        "nom",
        "entreprise",
        "poste",
        "email",
        "statut",
        "priorite",
        "date_creation"
    ]
].copy()

display.rename(
    columns={
        "prenom": "Prénom",
        "nom": "Nom",
        "entreprise": "Entreprise",
        "poste": "Poste",
        "email": "Email",
        "statut": "Statut",
        "priorite": "Priorité",
        "date_creation": "Créée le"
    },
    inplace=True
)

st.divider()

st.subheader("Candidatures")

# ==========================================================
# Tableau interactif
# ==========================================================

edited = st.data_editor(

    display,

    hide_index=True,

    use_container_width=True,

    num_rows="fixed",

    column_config={

        "id": st.column_config.NumberColumn(
            "ID",
            disabled=True,
            width="small"
        ),

        "Prénom": st.column_config.TextColumn(
            width="small"
        ),

        "Nom": st.column_config.TextColumn(
            width="small"
        ),

        "Entreprise": st.column_config.TextColumn(
            width="medium"
        ),

        "Poste": st.column_config.TextColumn(
            width="medium"
        ),

        "Email": st.column_config.TextColumn(
            width="large"
        ),

        "Statut": st.column_config.SelectboxColumn(

            options=[
                "Brouillon créé",
                "Envoyé",
                "Réponse reçue",
                "Entretien",
                "Offre",
                "Refus"
            ]

        ),

        "Priorité": st.column_config.NumberColumn(

            min_value=1,
            max_value=5,
            step=1

        ),

        "Créée le": st.column_config.TextColumn(
            disabled=True
        )

    }

)

st.divider()

left, right = st.columns([1, 1])

save = left.button(
    "💾 Enregistrer les modifications",
    use_container_width=True
)

refresh = right.button(
    "🔄 Actualiser",
    use_container_width=True
)

if refresh:

    st.rerun()

# ==========================================================
# Sauvegarde
# ==========================================================

if save:

    for _, row in edited.iterrows():

        update_candidate(

            int(row["id"]),

            prenom=row["Prénom"],
            nom=row["Nom"],
            entreprise=row["Entreprise"],
            poste=row["Poste"],
            email=row["Email"],
            statut=row["Statut"],
            priorite=int(row["Priorité"])

        )

    st.success("Les modifications ont été enregistrées.")

    st.rerun()

# ==========================================================
# Suppression
# ==========================================================

st.divider()

st.subheader("🗑️ Supprimer une candidature")

candidate_ids = edited["id"].tolist()

candidate_to_delete = st.selectbox(

    "Choisir une candidature",

    candidate_ids,

    format_func=lambda x: (
        f"{int(x)} - "
        f"{edited.loc[edited['id'] == x, 'Prénom'].values[0]} "
        f"{edited.loc[edited['id'] == x, 'Nom'].values[0]} "
        f"({edited.loc[edited['id'] == x, 'Entreprise'].values[0]})"
    )

)

if st.button(
    "Supprimer cette candidature",
    type="primary"
):

    delete_candidate(int(candidate_to_delete))

    st.success("Candidature supprimée.")

    st.rerun()

# ==========================================================
# Résumé
# ==========================================================

st.divider()

c1, c2, c3 = st.columns(3)

c1.metric(
    "Affichées",
    len(edited)
)

c2.metric(
    "Entretiens",
    len(
        edited[
            edited["Statut"] == "Entretien"
        ]
    )
)

c3.metric(
    "Offres",
    len(
        edited[
            edited["Statut"] == "Offre"
        ]
    )
)

st.caption(
    "CRM V3 • Les modifications sont enregistrées dans SQLite."
)
