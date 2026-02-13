import streamlit as st
import streamlit.components.v1 as components
import random
import time

# --- CONFIGURATION DORKNET ---
st.set_page_config(
    page_title="DorkNet Xchange | Core",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Style pour masquer l'interface Streamlit
st.markdown("""
    <style>
        header {visibility: hidden;}
        footer {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        .stApp { background-color: #1a1a1a; }
        .block-container { padding: 0rem; }
        iframe { display: block; margin: auto; border: none; }
    </style>
""", unsafe_allow_html=True)

# --- ENGINE : GÉNÉRATEUR DE DONNÉES TEMPS RÉEL ---
def get_live_market_data():
    """Génère des données de marché réalistes pour le Dr Numbi"""
    # Simulation du BTC (autour de 65k avec petite variation)
    btc_base = 65432
    btc_price = btc_base + random.randint(-150, 400)
    
    # Simulation du DNX (basé sur un algorithme interne)
    dnx_price = round(random.uniform(1.21, 1.38), 2)
    dnx_change = round(random.uniform(8.5, 14.2), 1)
    
    return {
        "btc": "{:,}".format(btc_price).replace(",", " "),
        "dnx": dnx_price,
        "change": dnx_change
    }

def serve_dorknet_page(file_name):
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        # --- INJECTION DYNAMIQUE DES PRIX ---
        # On remplace les valeurs statiques par les valeurs générées par Python
        data = get_live_market_data()
        
        # Remplacement dans le HTML avant l'envoi au navigateur
        html_content = html_content.replace("$1.24", f"${data['dnx']}")
        html_content = html_content.replace("+ 12.5%", f"+ {data['change']}%")
        html_content = html_content.replace("$65,432", f"${data['btc']}")
        
        # Rendu final
        components.html(html_content, height=1300, scrolling=False)
        
    except FileNotFoundError:
        st.error(f"ERREUR CRITIQUE : Le parchemin '{file_name}' est introuvable.")

# --- ROUTAGE DES AGENTS ---
params = st.query_params
target = params.get("p", "chat")

if target == "market":
    serve_dorknet_page("market.html")
else:
    serve_dorknet_page("index.html")
