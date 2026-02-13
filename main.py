import streamlit as st
import streamlit.components.v1 as components

# 1. Configuration de l'environnement DorkNet
st.set_page_config(
    page_title="DorkNet Xchange",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Nettoyage de l'interface Streamlit (Invisibilité OPSEC)
st.markdown("""
    <style>
        .reportview-container .main .block-container{ padding: 0rem; }
        footer {visibility: hidden;}
        header {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        div.stButton > button:first-child { display: none; }
        [data-testid="stHeader"] {display: none;}
    </style>
""", unsafe_allow_html=True)

# 3. Logique de routage des pages
# Récupère le paramètre 'p' dans l'URL (ex: ?p=market)
query_params = st.query_params
current_page = query_params.get("p", "chat") # 'chat' est la page par défaut

def serve_dorknet_page(file_name):
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            html_code = f.read()
        # Injection du composant HTML
        components.html(html_code, height=1200, scrolling=True)
    except FileNotFoundError:
        st.error(f"ERREUR CRITIQUE : Le parchemin '{file_name}' est introuvable sur le serveur.")

# 4. Exécution du déploiement
if current_page == "market":
    serve_dorknet_page("market.html")
else:
    serve_dorknet_page("index.html")
