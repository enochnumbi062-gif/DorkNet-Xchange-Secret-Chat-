import streamlit as st
import streamlit.components.v1 as components
import random
import os

# --- CONFIGURATION DORKNET ---
st.set_page_config(page_title="DorkNet Xchange | Core", layout="wide", initial_sidebar_state="collapsed")

# Masquer l'interface Streamlit
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

# --- BASE DE DONNÉES DES OMBRES ---
DB_FILE = "vault_messages.txt"

def save_to_vault(msg):
    """Enregistre le message scellé dans le fichier secret"""
    if msg:
        with open(DB_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M')}] : {msg}\n")

# --- ENGINE : PRIX TEMPS RÉEL ---
def get_live_market_data():
    return {
        "btc": "{:,}".format(65432 + random.randint(-100, 300)).replace(",", " "),
        "dnx": round(random.uniform(1.21, 1.38), 2),
        "change": round(random.uniform(8.5, 14.2), 1)
    }

# --- LOGIQUE D'INTERCEPTION ---
params = st.query_params
if "msg" in params:
    import time
    save_to_vault(params["msg"])
    # Rediriger proprement pour éviter les doublons
    st.query_params.clear()
    st.query_params.update(p="chat")
    st.rerun()

# --- VUE : VISUALISATION SECRÈTE (LE VAULT) ---
def show_secret_vault():
    st.markdown(f"""
        <div style="background-color: #f4ece1; padding: 50px; border: 3px double #2b2621; 
                    font-family: 'Special Elite', serif; width: 80%; margin: auto; min-height: 80vh;
                    background-image: url('https://www.transparenttextures.com/patterns/paper.png');">
            <h1 style="font-family: 'UnifrakturMaguntia'; text-align: center; border-bottom: 2px solid black;">
                ARCHIVES SCELLÉES DU DR NUMBI
            </h1>
            <div style="margin-top: 30px; font-size: 1.2rem; color: #2b2621;">
    """, unsafe_allow_html=True)
    
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in reversed(lines): # Les plus récents en premier
                st.markdown(f"<code>{line}</code><br><hr style='border: 1px dashed rgba(0,0,0,0.1)'>", unsafe_allow_html=True)
    else:
        st.write("AUCUNE ARCHIVE DÉTECTÉE.")
    
    st.markdown("</div></div>", unsafe_allow_html=True)

# --- ROUTAGE ---
target = params.get("p", "chat")

if target == "vault":
    # Protection par mot de passe simple
    pwd = st.sidebar.text_input("SÉCURITÉ DR_NUMBI", type="password")
    if pwd == "NUMBI_2026": # Modifiez votre code ici
        show_secret_vault()
    else:
        st.warning("ACCÈS REFUSÉ : SIGNATURE INCORRECTE")
elif target == "market":
    try:
        with open("market.html", "r", encoding="utf-8") as f:
            content = f.read()
        data = get_live_market_data()
        content = content.replace("$1.24", f"${data['dnx']}").replace("$65,432", f"${data['btc']}")
        components.html(content, height=1300)
    except: st.error("Fichier market.html manquant.")
else:
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()
        components.html(content, height=1300)
    except: st.error("Fichier index.html manquant.")
