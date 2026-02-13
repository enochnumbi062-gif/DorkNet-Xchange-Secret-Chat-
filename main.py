import streamlit as st
import streamlit.components.v1 as components

# Configuration de la page
st.set_page_config(page_title="DorkNet Xchange", layout="wide")

# Lecture du fichier HTML
with open("index.html", "r", encoding="utf-8") as f:
    html_code = f.read()

# Affichage du terminal dans Streamlit
components.html(html_code, height=1300, scrolling=True)

