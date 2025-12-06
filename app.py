import streamlit as st
import numpy as np
import numpy_financial as nf
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# PAGE SETTINGS
# ---------------------------------------------------------
st.set_page_config(
    page_title="EdTech Financial Dashboard",
    layout="wide",
)

st.title("📊 EdTech + Analytics Financial Intelligence Dashboard")
st.write("A complete investor-ready financial analytics and valuation system.")


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
st.sidebar.title("🔧 App Controls")

section = st.sidebar.radio(
    "Choose a Section",
    ["Overview", "Key Metrics", "Investor Valuation Model", "5-Year Projection", "Market Trend"]
)


# =========================================================
# 1. OVERVIEW TAB
# =========================================================
if section == "Overview":
    st.header("📘 Application Overview")

    st.markdown("""
    ### What this App Does
    This dashboard gives a **complete financial intelligence system** for EdTech–Analytics hybrid organizations.

    ### Features Included:
    - Monthly, quarterly, annual revenue logic  
    - Gross margin, Net margin, EBITDA, OPEX logic  
    - 5-year forecast  
    - Investor valuation model  
    - IRR, ROI, Terminal Value  
    - Market trend comparison (Global EdTech + Analytics)  
    - Interactive charts  

    ### Who It's For
    - Investors analyzing your business  
    - Founders building pitch decks  
    - Finance teams automating forecasting  
    - EdTech/Analytics companies wanting clarity on profitability  
    """)

    st.info("Use the left sidebar to navigate to other tabs.")



# =========================================================
# 2. KEY METRICS TAB
# =========================================================
elif section == "Key Metrics":
    st.header("📌 Important Attributes & Definitions")

    st.markdown("""
    ### 🎯 Key EdTech Financial Metrics
    **Total Revenue:** Sum collected from courses, consulting, B2B, subscriptions.  
    **Operational Cost (Direct Cost):** Mentor cost, delivery cost, program running cost.  
    **OPEX (Indirect Cost):** Salaries, rent, marketing, software tools.  
    **Gross Profit:** Revenue − Direct Cost.  
    **Gross Margin %:** (Gross Profit / Revenue) × 100.  
    **EBITDA:** Earnings before interest, tax, depreciation.  
    **EBITDA Margin %:** EBITDA ÷ Revenue.  
    **Net Profit:** Profit after all costs.  
    **Net Margin %:** Net Profit ÷ Revenue.  
    **FCF (Free Cash Flow):** Money left after reinvestments.  
    **Burn Rate:** How much money the company loses each month.  
    **Runway:** Months the company can survive with current cash.  
    **DCF:** Discounted cash flow valuation.  
    **IRR:** Annualized return rate for investors.  
    **CAGR:** Annual growth rate over multiple years.  
    **CAC:** Acquisition cost per customer.  
    **MRR/ARR:** Subscription revenue metrics.  
    """)


# =========================================================
# 3. INVESTOR VALUATION MODEL TAB
# =========================================================
elif section == "Investor Valuation Model":
    st.header("💰 Investor Valuation Calculator")

    colA, colB = st.columns(2)

    with colA:
        total_investment = st.number_input("Total Investment (₹)", min_value=0.0, step=100000.0)
        equity = st.number_input("Equity (0.20 = 20%)", min_value=0.0, max_value=1.0, value=0.20)
        tenure = st.number_input("Projection Years", min_value=1, max_value=10, value=5)
        exit_year = st.number_input("Exit Year", min_value=1, max_value=10, value=5)

    with colB:
        revenue_y1 = st.number_input("Current Annual Revenue (₹)", min_value=0.0)
        growth = st.number_input("Expected Annual Growth (0.25 = 25%)", min_value=0.0, max_value=1.0, value=0.25)
        ebitda_margin = st.number_input("EBITDA Margin (0.26 = 26%)", min_value=0.0, max_value=1.0, value=0.26)
        exit_multiple = st.number_input("Exit EBITDA Multiple (X)", min_value=1.0, max_value=20.0, value=6.0)

    if st.button("Compute Investor Returns"):
        
        # 5-Year Projection
        years = np.arange(1, tenure + 1)
        rev = []
        ebit = []
        cur = revenue_y1

        for _ in years:
            rev.append(cur)
            ebit.append(cur * ebitda_margin)
            cur *= (1 + growth)

        df = pd.DataFrame({
            "Year": years,
            "Revenue (₹)": rev,
            "EBITDA (₹)": ebit,
            "Valuation (₹)": np.array(ebit) * exit_multiple
        })

        st.subheader("📄 Projection Table")
        st.dataframe(df.style.format("{:,.2f}"))

        exit_ebitda = df.loc[df["Year"] == exit_year, "EBITDA (₹)"].iloc[0]
        terminal_value = exit_ebitda * exit_multiple
        investor_payout = terminal_value * equity
        net_benefit = investor_payout - total_investment
        roi = net_benefit / total_investment
        irr = nf.irr([-total_investment] + [0]*(exit_year-1) + [investor_payout])

        st.subheader("📌 Investor Summary")

        col1, col2, col3 = st.columns(3)
        col1.metric("Terminal Value (₹)", f"{terminal_value:,.2f}")
        col2.metric("Investor Payout (₹)", f"{investor_payout:,.2f}")
        col3.metric("ROI (%)", f"{roi*100:.2f}%")

        col1.metric("IRR (%)", f"{irr*100:.2f}%")
        col2.metric("Net Profit to Investor (₹)", f"{net_benefit:,.2f}")
        col3.metric("Equity (%)", f"{equity*100:.2f}%")


# =========================================================
# 4. 5-YEAR PROJECTION TAB
# =========================================================
elif section == "5-Year Projection":
    st.header("📈 5-Year Financial Projection")

    revenue = st.number_input("Base Revenue (Year 1)", value=6000000.0)
    growth_rate = st.number_input("Annual Growth Rate", value=0.25)
    ebitda_margin = st.number_input("EBITDA Margin", value=0.26)
    
    rev = []
    ebit = []
    cur = revenue

    for _ in range(5):
        rev.append(cur)
        ebit.append(cur * ebitda_margin)
        cur *= (1 + growth_rate)

    df = pd.DataFrame({
        "Year": [1,2,3,4,5],
        "Revenue (₹)": rev,
        "EBITDA (₹)": ebit
    })

    st.dataframe(df.style.format("{:,.2f}"))

    st.subheader("📊 Revenue & EBITDA Chart")
    fig, ax = plt.subplots(figsize=(10,5))
    ax.bar(df["Year"], df["Revenue (₹)"], label="Revenue")
    ax.plot(df["Year"], df["EBITDA (₹)"], marker='o', color='red', label="EBITDA")
    ax.legend()
    st.pyplot(fig)


# =========================================================
# 5. MARKET TREND TAB
# =========================================================
elif section == "Market Trend":
    st.header("🌎 Industry Trend vs Your Growth")

    years = np.arange(1, 6)
    global_base = 142500  # Cr
    segment_base = 20000  # Cr

    global_cagr = 0.18
    segment_cagr = 0.22

    g = []
    s = []
    gc = global_base
    sc = segment_base

    for _ in years:
        g.append(gc)
        s.append(sc)
        gc *= 1 + global_cagr
        sc *= 1 + segment_cagr

    st.subheader("📊 Market Growth Chart")
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(years, g, marker='o', label="Global EdTech + Analytics (₹ Cr)")
    ax.plot(years, s, marker='s', label="Workforce Dev + Analytics (₹ Cr)")
    ax.legend()
    ax.grid(True, linestyle="--")
    st.pyplot(fig)
