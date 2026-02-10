import streamlit as st
import requests

st.set_page_config(page_title="Polymarket Live Arb", layout="wide")
st.title("🤑 Polymarket Live Arb")

st.write("Market URL paste karo, live prices fetch ho jayenge")

# ---------- LIVE API ----------
def fetch_polymarket_prices(slug):
    url = f"https://clob.polymarket.com/markets?slug={slug}"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            tokens = data[0]["tokens"] if data else []
            if len(tokens) >= 2:
                yes = tokens[0]["price"] * 100
                no = tokens[1]["price"] * 100
                return yes, no
    except:
        pass
    return None, None

# ---------- UI ----------
col1, col2
