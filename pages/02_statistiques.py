import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from tracking import get_candidates

st.set_page_config(
    page_title="Statistiques",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Statistiques")

df = get_candidates()

if df.empty:
    st.info("Aucune candidature.")
    st.stop()

# ==========================================================
# Préparation
# ==========================================================

df["date_creation"] = pd.to_datetime(
    df["date_creation"],
    errors="coerce"
)

# ==========================================================
# KPI
# ==========================================================

total = len(df)

entreprises = df["entreprise"].nunique()

entretiens = (df["statut"] == "Entretien").sum()

offres = (df["statut"] == "Offre").sum()

refus = (df["statut"] == "Refus").sum()

envoyes = (df["statut"] == "Envoyé").sum()

reponses = (
    df["statut"].isin(
        ["Réponse reçue", "Entretien", "Offre", "Refus"]
    )
).sum()

taux_reponse = 0

if total > 0:
    taux_reponse = round(
        reponses / total * 100,
        1
    )

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("📨", total)

c2.metric("🏢", entreprises)

c3.metric("🟣", entretiens)

c4.metric("🟢", offres)

c5.metric("📈", f"{taux_reponse}%")

st.divider()

# ==========================================================
# Répartition des statuts
# ==========================================================

left, right = st.columns(2)

with left:

    st.subheader("Statuts")

    status = df["statut"].value_counts()

    fig, ax = plt.subplots(figsize=(6,6))

    ax.pie(
        status,
        labels=status.index,
        autopct="%1.1f%%"
    )

    st.pyplot(fig)

with right:

    st.subheader("Top entreprises")

    top = (
        df["entreprise"]
        .value_counts()
        .head(10)
    )

    fig, ax = plt.subplots(figsize=(8,5))

    ax.barh(
        top.index,
        top.values
    )

    ax.invert_yaxis()

    st.pyplot(fig)

st.divider()

# ==========================================================
# Evolution
# ==========================================================

st.subheader("Evolution mensuelle")

monthly = (
    df
    .groupby(
        df["date_creation"].dt.to_period("M")
    )
    .size()
)

monthly.index = monthly.index.astype(str)

fig, ax = plt.subplots(figsize=(10,4))

ax.plot(
    monthly.index,
    monthly.values,
    marker="o"
)

plt.xticks(rotation=45)

st.pyplot(fig)

st.divider()

# ==========================================================
# Tableau
# ==========================================================

st.subheader("Résumé")

resume = pd.DataFrame({

    "Indicateur":[

        "Candidatures",

        "Entreprises",

        "Envoyées",

        "Réponses",

        "Entretiens",

        "Offres",

        "Refus"

    ],

    "Valeur":[

        total,

        entreprises,

        envoyes,

        reponses,

        entretiens,

        offres,

        refus

    ]

})

st.dataframe(
    resume,
    use_container_width=True,
    hide_index=True
)

st.divider()

st.caption("CRM V3 • Dashboard statistique")
