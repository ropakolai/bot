import streamlit as st
import pandas as pd

from tracking import get_candidates


st.set_page_config(
    page_title="Statistiques",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Tableau de bord")

df = get_candidates()

if df.empty:
    st.info("Aucune candidature enregistrée.")
    st.stop()

# ==========================================================
# Nettoyage
# ==========================================================

df["Statut"] = df["Statut"].fillna("")
df["Entreprise"] = df["Entreprise"].fillna("")
df["Date"] = pd.to_datetime(
    df["Date"],
    format="%d/%m/%Y",
    errors="coerce"
)

# ==========================================================
# KPIs
# ==========================================================

total = len(df)

drafts = (df["Statut"] == "Brouillon créé").sum()
sent = (df["Statut"] == "Envoyé").sum()
interviews = (df["Statut"] == "Entretien").sum()
positive = (df["Statut"] == "Réponse positive").sum()
negative = (df["Statut"] == "Réponse négative").sum()

rate_interview = interviews / total * 100 if total else 0
rate_success = positive / total * 100 if total else 0

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Total", total)
c2.metric("Brouillons", drafts)
c3.metric("Entretiens", interviews)
c4.metric("Positives", positive)
c5.metric("Négatives", negative)

st.divider()

c1, c2 = st.columns(2)

c1.metric(
    "Taux d'entretien",
    f"{rate_interview:.1f}%"
)

c2.metric(
    "Taux de réussite",
    f"{rate_success:.1f}%"
)

# ==========================================================
# Graphiques
# ==========================================================

st.divider()

col1, col2 = st.columns(2)

with col1:

    st.subheader("Répartition des statuts")

    st.bar_chart(
        df["Statut"].value_counts()
    )

with col2:

    st.subheader("Top entreprises")

    companies = (
        df["Entreprise"]
        .replace("", pd.NA)
        .dropna()
        .value_counts()
        .head(10)
    )

    st.bar_chart(companies)

# ==========================================================
# Evolution
# ==========================================================

st.divider()

st.subheader("Candidatures au fil du temps")

timeline = (
    df
    .dropna(subset=["Date"])
    .groupby("Date")
    .size()
)

st.line_chart(timeline)

# ==========================================================
# Tableau
# ==========================================================

st.divider()

st.subheader("Toutes les candidatures")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)
