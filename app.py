import streamlit as st

st.title("🤑 Polymarket Arb ($10 | 2-20%)")

yes = st.slider("YES ¢", 0, 99, 20)
no = st.slider("NO ¢", 0, 99, 70)
invest = st.number_input("$", 1.0, 100.0, 10.0)

if st.button("Check"):
    total = (yes + no) / 100
    edge = (1 - total) * 100
    
    if 2 <= edge <= 20:  # Changed: 2-20% profit
        yes_buy = invest * (no / 100) / total
        profit = invest * edge / 100
        st.success(f"""✅ ARB {edge:.1f}%!
YES: ${yes_buy:.2f} ({yes}¢)
NO: ${(invest - yes_buy):.2f} ({no}¢)
Profit: **${profit:.2f}**""")
    else:
        st.error(f"No arb: {edge:.1f}% (need 2-20%)")
