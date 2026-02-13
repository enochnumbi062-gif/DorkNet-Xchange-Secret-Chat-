import streamlit as st
import streamlit.components.v1 as components

# Configuration de la page DorkNet
st.set_page_config(page_title="DorkNet Xchange", layout="wide", initial_sidebar_state="collapsed")

# Suppression des marges Streamlit pour un look full-screen
st.markdown("""
    <style>
        .reportview-container .main .block-container{ padding-top: 0rem; }
        footer {visibility: hidden;}
        header {visibility: hidden;}
        #MainMenu {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Gestion de la Navigation via l'URL ou l'état de la session
query_params = st.query_params
page = query_params.get("p", "chat")

def load_html(file_name):
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"<h2>ERREUR : Fichier {file_name} introuvable dans le dépôt.</h2>"

# AFFICHAGE LOGIQUE
if page == "market":
    content = load_html("market.html")
    # Hauteur ajustée pour le parchemin du marché
    components.html(content, height=1000, scrolling=True)
else:
    content = load_html("index.html")
    # Hauteur ajustée pour le terminal de chat
    components.html(content, height=1000, scrolling=True)
