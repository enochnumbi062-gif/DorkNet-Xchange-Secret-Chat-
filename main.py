import streamlit as st
import streamlit.components.v1 as components
import random
import os
import time
import requests

# Configuration de la page
st.set_page_config(page_title="DorkNet Xchange | Core", layout="wide", initial_sidebar_state="collapsed")

# --- HACK DE LA BARRE LATÉRALE (FUSIONNÉ) ---
st.markdown("""
    <style>
    /* Masquer le header et le footer Streamlit */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Hack de la barre latérale : Tournois Noir & Turquoise */
    [data-testid="stSidebar"] {
        background-color: #000000 !important;
        border-right: 2px solid #008b8b !important;
    }
    [data-testid="stSidebar"] * {
        color: #008b8b !important;
        font-family: 'Special Elite', sans-serif !important;
    }
    
    /* Style des boutons de navigation Streamlit */
    .stButton>button {
        width: 100%;
        background-color: transparent;
        color: #008b8b;
        border: 1px solid #008b8b;
        margin-bottom: 10px;
        font-family: 'Special Elite';
    }
    .stButton>button:hover {
        background-color: #008b8b;
        color: black;
        border: 1px solid #008b8b;
    }
    </style>
""", unsafe_allow_html=True)

# --- ENGINE : PRIX TEMPS RÉEL VIA API ---
def get_live_market_data():
    try:
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true", timeout=5)
        data = response.json()
        
        btc_price = data['bitcoin']['usd']
        btc_change = data['bitcoin']['usd_24h_change']
        
        dnx_price = round((btc_price / 50000) + random.uniform(0.1, 0.3), 2)
        
        return {
            "btc": "{:,}".format(int(btc_price)).replace(",", " "),
            "dnx": dnx_price,
            "change": round(btc_change, 1)
        }
    except Exception as e:
        return {
            "btc": "65 432",
            "dnx": 1.24,
            "change": 12.5
        }

# --- GESTION DU VAULT ET DU RENDU ---
DB_FILE = "vault_messages.txt"

def save_to_vault(msg):
    if msg:
        with open(DB_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{time.strftime('%H:%M')}] : {msg}\n")

params = st.query_params
if "msg" in params:
    save_to_vault(params["msg"])
    st.query_params.clear()
    st.query_params.update(p="chat")
    st.rerun()

def serve_page(file_name, is_market=False):
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            html = f.read()
        
        if is_market:
            data = get_live_market_data()
            html = html.replace("$1.24", f"${data['dnx']}")
            html = html.replace("+ 12.5%", f"{data['change']}%")
            html = html.replace("$65,432", f"${data['btc']}")
            
        components.html(html, height=1300)
    except:
        st.error(f"Fichier {file_name} manquant.")

# --- ROUTAGE ---
target = params.get("p", "chat")

# Ajout d'une interface de navigation dans la sidebar hackée
with st.sidebar:
    st.markdown("<h2 style='text-align:center; font-family:UnifrakturMaguntia;'>DorkNet Hub</h2>", unsafe_allow_html=True)
    if st.button("ABYSSAL CHAT"):
        st.query_params.update(p="chat")
        st.rerun()
    if st.button("ASSET EXCHANGE"):
        st.query_params.update(p="market")
        st.rerun()
    if st.button("VAULT ACCESS"):
        st.query_params.update(p="vault")
        st.rerun()
    st.markdown("<hr style='border-color:#008b8b'>", unsafe_allow_html=True)

if target == "vault":
    pwd = st.sidebar.text_input("SÉCURITÉ DR_NUMBI", type="password")
    if pwd == "NUMBI_2026":
        st.title("ARCHIVES SCELLÉES")
        if os.path.exists(DB_FILE):
            with open(DB_FILE, "r") as f: st.code(f.read())
    else: st.warning("ACCÈS REFUSÉ")
elif target == "market":
    serve_page("market.html", is_market=True)
else:
    serve_page("index.html")
