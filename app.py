import streamlit as st
import requests

# ---------- CONFIG ----------
st.set_page_config(page_title="Polymarket Arb Radar", layout="wide")
st.title("🤑 Polymarket Arb Radar")

st.write(
    "Binary markets only. Either sliders use karo ya Polymarket market ID paste karke "
    "'Fetch from Polymarket' dabao."
)

# ---------- HELPER: API SE PRICE ----------
GAMMA_BASE = "https://gamma-api.polymarket.com"


def get_yes_no_from_api(market_id: str):
    """
    Polymarket Gamma API se given market ka YES/NO last price (cents) laata hai.
    Binary market assume.
    """
    url = f"{GAMMA_BASE}/markets/{market_id}"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    data = r.json()

    # outcomes structure Gamma docs ke hisaab se
    outcomes = data.get("outcomes", [])
    if len(outcomes) < 2:
        raise ValueError("Binary market nahi mila (2 outcomes required).")

    # outcome[0] = YES, outcome[1] = NO (common convention, check if needed)
    yes_price = outcomes[0].get("lastPrice")
    no_price = outcomes[1].get("lastPrice")

    if yes_price is None or no_price is None:
        raise ValueError("Prices missing (lastPrice not found).")

    # to cents
    yes_c = round(yes_price * 100, 2)
    no_c = round(no_price * 100, 2)
    return yes_c, no_c, data.get("question", "Unknown market")


# ---------- SESSION DEFAULTS ----------
if "yes" not in st.session_state:
    st.session_state.yes = 20
if "no" not in st.session_state:
    st.session_state.no = 70

# ---------- LAYOUT ----------
col_left, col_right = st.columns([1, 1.2])

with col_left:
    st.subheader("1️⃣ Prices Input")

    # A) Polymarket se auto fetch
    st.markdown("**Option A: Polymarket se auto**")
    market_id = st.text_input(
        "Polymarket market ID (URL ka last part paste karo)", ""
    )

    if st.button("🔄 Fetch from Polymarket"):
        if not market_id.strip():
            st.warning("Market ID daalo pehle.")
        else:
            try:
                yes_c, no_c, q = get_yes_no_from_api(market_id.strip())
                st.session_state.yes = yes_c
                st.session_state.no = no_c
                st.success(f"Fetched: {q}")
                st.info(f"YES = {yes_c}¢, NO = {no_c}¢")
            except Exception as e:
                st.error(f"API error: {e}")

    st.markdown("---")

    # B) Manual sliders
    st.markdown("**Option B: Manual sliders**")
    yes = st.slider("YES ¢", 0, 99, int(st.session_state.yes))
    no = st.slider("NO ¢", 0, 99, int(st.session_state.no))

    # bankroll & settings
    invest = st.number_input("Investment $", 1.0, 10000.0, 10.0, step=1.0)
    gas = st.number_input("Gas + other fees $", 0.0, 50.0, 0.5, step=0.1)
    min_edge, max_edge = st.slider(
        "Target gross edge range %", 0.0, 30.0, (2.0, 20.0)
    )

    check = st.button("✅ Check ARB")

with col_right:
    st.subheader("2️⃣ Result")

    if check:
        total = (yes + no) / 100  # implied prob
        edge = (1 - total) * 100  # gross %
        gross_profit = invest * edge / 100
        net_profit = gross_profit - gas
        net_edge = (net_profit / invest) * 100

        if min_edge <= edge <= max_edge and net_profit > 0:
            # sizing
            if total <= 0:
                st.error("Total probability 0, prices galat hain.")
            else:
                yes_buy = invest * (no / 100) / total
                no_buy = invest - yes_buy

                st.success(
                    f"✅ ARB FOUND\n\n"
                    f"**Gross edge:** {edge:.2f}%\n\n"
                    f"**Net edge (after fees):** {net_edge:.2f}%\n"
                    f"**Net profit:** ${net_profit:.2f}"
                )

                st.markdown("**Position sizing**")
                st.write(f"YES: **${yes_buy:.2f}** at **{yes}¢**")
                st.write(f"NO: **${no_buy:.2f}** at **{no}¢**")

                st.markdown("---")
                st.markdown("**Copy plan**")
                st.code(
                    f"Buy ${yes_buy:.2f} YES @ {yes}¢ and "
                    f"${no_buy:.2f} NO @ {no}¢.\n"
                    f"Expect ≈ ${net_profit:.2f} profit ({net_edge:.2f}% net) if filled.",
                    language="text",
                )
        else:
            st.error(
                f"No clean arb.\n\n"
                f"Gross edge: {edge:.2f}%\n"
                f"Net edge (after ${gas:.2f} fees): {net_edge:.2f}%\n"
                f"Target: {min_edge:.1f}–{max_edge:.1f}% gross + positive net."
            )

    else:
        st.info("Inputs set karo, phir **Check ARB** dabao.")
```
