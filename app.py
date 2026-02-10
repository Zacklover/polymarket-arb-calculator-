import streamlit as st
import requests
import websocket
import json
import threading

st.set_page_config(page_title="Polymarket Live Arb", layout="wide")
st.title("🤑 Polymarket Live Arb - WebSocket")

st.write("Market slug paste karo, live WebSocket se prices milenge")

# ---------- WEBSOCKET LIVE PRICES ----------
CLOB_WS = "wss://ws-subscriptions-clob.polymarket.com/ws/market"

prices = st.session_state.get("prices", {"yes": 50, "no": 50})

col1, col2 = st.columns([1, 1.2])

with col1:
    slug = st.text_input("Market slug (sol-updown-4h-1770714000)")
    
    if st.button("🔴 Connect Live"):
        def ws_thread():
            ws = websocket.WebSocketApp(CLOB_WS,
                on_message=lambda ws, msg: update_prices(json.loads(msg)),
                on_error=lambda ws, err: st.error(f"WS Error: {err}"),
                on_close=lambda ws: st.warning("WS Closed"))
            ws.run_forever()
        
        threading.Thread(target=ws_thread, daemon=True).start()
        st.success("Live connected!")

    st.metric("YES Live", f"{prices['yes']:.1f}¢")
    st.metric("NO Live", f"{prices['no']:.1f}¢")

def update_prices(data):
    if 'price' in data:
        prices['yes'] = data['price'] * 100
        prices['no'] = (100 - prices['yes'])
        st.session_state.prices
