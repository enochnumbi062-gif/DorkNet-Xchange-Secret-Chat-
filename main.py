import streamlit as st
import streamlit.components.v1 as components
import random
import os

st.set_page_config(page_title="DorkNet Xchange | Core", layout="wide", initial_sidebar_state="collapsed")

# --- SYSTÈME DE STOCKAGE SECRET ---
DB_FILE = "vault_messages.txt"

def save_message(msg):
    if msg:
        with open(DB_FILE, "a", encoding="utf-8") as f:
            f.write(f"{msg}\n---\n")

# --- ENGINE : PRIX ET RENDU ---
def get_live_market_data():
    return {
        "btc": "{:,}".format(65432 + random.randint(-100, 300)).replace(",", " "),
        "dnx": round(random.uniform(1.21, 1.38), 2),
        "change": round(random.uniform(8.5, 14.2), 1)
    }

# --- INTERCEPTION DES MESSAGES VIA L'URL ---
params = st.query_params
if "msg" in params:
    save_message(params["msg"])
    # On nettoie l'URL après enregistrement
    st.query_params.update(p=params.get("p", "chat"))

def serve_dorknet_page(file_name):
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            html_content = f.read()
        data = get_live_market_data()
        html_content = html_content.replace("$1.24", f"${data['dnx']}")
        html_content = html_content.replace("+ 12.5%", f"+ {data['change']}%")
        html_content = html_content.replace("$65,432", f"${data['btc']}")
        components.html(html_content, height=1300, scrolling=False)
    except FileNotFoundError:
        st.error(f"Fichier '{file_name}' introuvable.")

# ROUTAGE
target = params.get("p", "chat")
serve_dorknet_page("market.html" if target == "market" else "index.html")
