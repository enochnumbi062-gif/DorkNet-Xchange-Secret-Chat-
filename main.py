import streamlit as st
import streamlit.components.v1 as components
import random

st.set_page_config(page_title="DorkNet Xchange | Network", layout="wide", initial_sidebar_state="collapsed")

# --- SIMULATION DE FLUX DE MARCHÉ (Dr Numbi Engine) ---
def get_market_data():
    # Ici, on pourrait utiliser une API comme CoinGecko
    return {
        "dnx_price": round(random.uniform(1.20, 1.45), 2),
        "dnx_change": round(random.uniform(5.0, 15.0), 1),
        "btc_price": "{:,}".format(random.randint(64000, 67000)),
    }

def serve_dorknet_page(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        # --- AUTOMATISATION : Injection des variables ---
        data = get_market_data()
        html_content = html_content.replace("$1.24", f"${data['dnx_price']}")
        html_content = html_content.replace("+ 12.5%", f"+ {data['dnx_change']}%")
        html_content = html_content.replace("$65,432", f"${data['btc_price']}")
        
        components.html(html_content, height=1300, scrolling=True)
    except FileNotFoundError:
        st.error(f"Fichier '{file_path}' introuvable.")

# --- ROUTAGE ---
query_params = st.query_params
current_page = query_params.get("p", "chat")

if current_page == "market":
    serve_dorknet_page("market.html")
else:
    serve_dorknet_page("index.html")
