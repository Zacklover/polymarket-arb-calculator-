import streamlit as st
import requests
import time

st.set_page_config(page_title="Polymarket Live Arb", layout="wide")
st.title("🤑 Polymarket Live Arb Radar")

st.write("Market URL paste karo → live YES/NO prices → instant arb calc")

# ---------- LIVE API (2026 working) ----------
DATA_BASE = "https://data-api.polymarket.com"

@st.cache_data(ttl=15)
def fetch_live_prices(slug):
    """
    Polymarket data API se live prices
    """
    try:
        # Try markets endpoint first
        url = f"{DATA_BASE}/markets"
        params = {"slug": slug, "limit": 1}
        r = requests.get(url, params=params, timeout=10)
        
        if r.status_code == 200:
            data = r.json()
            if data:
                market = data[0]
                tokens = market.get("tokens", [])
                if len(tokens) >= 2:
                    yes = tokens[0].get("last_price", 0.5) * 100
                    no = tokens[1].get("last_price
