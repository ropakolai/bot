import streamlit as st

from templates import (
    get_template_names,
    get_template,
    create_template,
    update_template,
    delete_template,
)

st.set_page_config(
    page_title="Paramètres",
    page_icon="⚙️",
    layout="wide",
)

st.title("⚙️ Paramètres")

st.subheader("📧 Modèles d'e-mails")

models = get_template_names()

if not models:
    st.info("Aucun modèle enregistré.")
    models = []

selected = st.selectbox(
    "Choisir un modèle",
    models if models else [""]
)

if selected:

    template = get_template(selected)

    subject = st.text_input(
        "Objet",
        value=template["Objet"]
    )

    body = st.text_area(
        "Corps du message",
        value=template["Corps"],
        height=350
    )

    c1, c2 = st.columns(2)

    with c1:

        if st.button("💾 Enregistrer"):

            update_template(
                selected,
                subject,
                body
            )

            st.success("Modèle enregistré.")

            st.rerun()

    with c2:

        if st.button("🗑 Supprimer"):

            delete_template(selected)

            st.success("Modèle supprimé.")

            st.rerun()

st.divider()

st.subheader("➕ Nouveau modèle")

new_name = st.text_input("Nom du modèle")

new_subject = st.text_input("Objet du nouveau modèle")

new_body = st.text_area(
    "Corps",
    height=250
)

if st.button("Créer le modèle"):

    if not new_name.strip():

        st.error("Donne un nom au modèle.")

    else:

        ok = create_template(
            new_name,
            new_subject,
            new_body
        )

        if ok:

            st.success("Modèle créé.")

            st.rerun()

        else:

            st.error("Ce modèle existe déjà.")
