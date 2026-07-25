import streamlit as st
import drive

st.title("Test Google Drive")

try:
    cvs = drive.get_cvs()
    lettres = drive.get_letters()

    st.success("Connexion à Google Drive réussie !")

    st.subheader("CV")
    st.write(cvs)

    st.subheader("Lettres")
    st.write(lettres)

except Exception as e:
    st.error(e)
