import streamlit as st

st.set_page_config(layout="wide")
st.title("🤑 Polymarket Arb Calc ($10 | 2-5%)")

col1, col2 = st.columns([1,2])

with col1:
    yes_price = st.slider("YES ¢", 0, 99, 20)
    no_price = st.slider("NO ¢", 0, 99, 70)
    investment = st.number_input("$", 1.0, 100.0, 10.0)
    
    if st.button("🚀 Check", use_container_width=True):
        total = (yes_price + no_price) / 100
        edge = (1 - total) * 100
        
        if 2 <= edge <= 5:
            yes_buy = investment * no_price/100 / total
            no_buy = investment - yes_buy
            profit = investment * edge / 100
            
            st.balloons()
            st.success(f"**✅ ARB {edge:.1f}%!**\nYES: ${yes_buy:.2f}\nNO: ${no_buy:.2f}\nProfit: **${profit:.2f}**")
        else:
            st.error(f"❌ {edge:.1f}% (need 2-5%)")

st.caption("💡 Scan low-liq markets")
