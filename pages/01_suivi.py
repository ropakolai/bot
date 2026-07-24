import streamlit as st
import pandas as pd

from tracking import get_candidates

# ==========================================================
# Configuration
# ==========================================================

st.set_page_config(
    page_title="Suivi des candidatures",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Suivi des candidatures")

# ==========================================================
# Chargement
# ==========================================================

try:

    df = get_candidates()

except Exception as e:

    st.error(f"Erreur lors du chargement des candidatures : {e}")

    st.stop()


# ==========================================================
# Vérification
# ==========================================================

if df.empty:

    st.info("Aucune candidature enregistrée.")

    st.stop()


# ==========================================================
# Statistiques rapides
# ==========================================================

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Nombre de candidatures",
        len(df)
    )

with col2:

    st.metric(
        "Entreprises",
        df["Entreprise"].nunique()
    )


st.divider()

# ==========================================================
# Recherche
# ==========================================================

search = st.text_input(
    "🔍 Rechercher",
    placeholder="Nom, prénom, entreprise, email ou poste..."
)

if search:

    mask = (

        df["Prénom"].astype(str).str.contains(search, case=False)

        |

        df["Nom"].astype(str).str.contains(search, case=False)

        |

        df["Entreprise"].astype(str).str.contains(search, case=False)

        |

        df["Email"].astype(str).str.contains(search, case=False)

        |

        df["Poste"].astype(str).str.contains(search, case=False)

    )

    df = df[mask]


# ==========================================================
# Filtre statut
# ==========================================================

statuts = ["Tous"] + sorted(df["Statut"].dropna().unique().tolist())

selected_status = st.selectbox(

    "Statut",

    statuts

)

if selected_status != "Tous":

    df = df[df["Statut"] == selected_status]


st.divider()

# ==========================================================
# Tableau
# ==========================================================

st.subheader("Candidatures")

display_columns = [

    "Date",
    "Prénom",
    "Nom",
    "Entreprise",
    "Poste",
    "Email",
    "Statut"

]

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

# ==========================================================
# Sélection d'une candidature
# ==========================================================

st.divider()

st.subheader("✏️ Modifier une candidature")

if df.empty:

    st.info("Aucune candidature disponible.")

else:

    candidates = (

        df["Prénom"].fillna("")
        + " "
        + df["Nom"].fillna("")
        + " - "
        + df["Entreprise"].fillna("")

    ).tolist()

    selected = st.selectbox(

        "Sélectionner une candidature",

        candidates

    )

    row = df.iloc[candidates.index(selected)]

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        st.text_input(
            "Prénom",
            value=row["Prénom"],
            disabled=True
        )

        st.text_input(
            "Nom",
            value=row["Nom"],
            disabled=True
        )

        st.text_input(
            "Entreprise",
            value=row["Entreprise"],
            disabled=True
        )

        st.text_input(
            "Email",
            value=row["Email"],
            disabled=True
        )

    with col2:

        new_status = st.selectbox(

            "Statut",

            [

                "Brouillon créé",
                "Envoyé",
                "Entretien",
                "Réponse positive",
                "Réponse négative",
                "Sans réponse"

            ],

            index=[

                "Brouillon créé",
                "Envoyé",
                "Entretien",
                "Réponse positive",
                "Réponse négative",
                "Sans réponse"

            ].index(row["Statut"])

            if row["Statut"] in [

                "Brouillon créé",
                "Envoyé",
                "Entretien",
                "Réponse positive",
                "Réponse négative",
                "Sans réponse"

            ]

            else 0

        )

        new_notes = st.text_area(

            "Notes",

            value=row.get("Notes", ""),

            height=150

        )

# ==========================================================
# Boutons
# ==========================================================

    col_save, col_delete = st.columns(2)

    with col_save:

        if st.button("💾 Enregistrer", use_container_width=True):

            from tracking import update_status, update_notes

            update_status(

                row["Email"],

                new_status

            )

            update_notes(

                row["Email"],

                new_notes

            )

            st.success("Candidature mise à jour.")

            st.rerun()

    with col_delete:

        if st.button(

            "🗑 Supprimer",

            type="primary",

            use_container_width=True

        ):

            from tracking import delete_candidate

            delete_candidate(

                row["Email"]

            )

            st.success("Candidature supprimée.")

            st.rerun()
# ==========================================================
# Statistiques
# ==========================================================

st.divider()

st.subheader("📈 Statistiques")

col1, col2, col3, col4 = st.columns(4)

status_counts = df["Statut"].value_counts()

with col1:
    st.metric(
        "📬 Brouillons",
        status_counts.get("Brouillon créé", 0)
    )

with col2:
    st.metric(
        "📤 Envoyées",
        status_counts.get("Envoyé", 0)
    )

with col3:
    st.metric(
        "🤝 Entretiens",
        status_counts.get("Entretien", 0)
    )

with col4:
    st.metric(
        "✅ Réponses positives",
        status_counts.get("Réponse positive", 0)
    )

# ==========================================================
# Graphique
# ==========================================================

st.divider()

st.subheader("Répartition des candidatures")

chart = df["Statut"].value_counts()

st.bar_chart(chart)

# ==========================================================
# Export CSV
# ==========================================================

st.divider()

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Télécharger le suivi (CSV)",
    data=csv,
    file_name="suivi_candidatures.csv",
    mime="text/csv",
    use_container_width=True
)
