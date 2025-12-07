import streamlit as st
import pandas as pd
import numpy as np
import numpy_financial as nf
import plotly.graph_objects as go

# ----------------------------------------------------------
# HEADER & LOGO
# ----------------------------------------------------------
logo_url = "https://raw.githubusercontent.com/Analytics-Avenue/streamlit-dataapp/main/logo.png"

st.markdown(f"""
<div style="display: flex; align-items: center; margin-bottom:16px;">
    <img src="{logo_url}" width="60" style="margin-right:12px;">
    <div style="line-height:1;">
        <div style="color:#064b86; font-size:36px; font-weight:700;">Analytics Avenue &</div>
        <div style="color:#064b86; font-size:36px; font-weight:700;">Advanced Analytics</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------
st.set_page_config(
    page_title="Investor Projection Dashboard",
    layout="wide"
)

# Hide sidebar
st.markdown("""
<style>
[data-testid="stSidebarNav"] {display:none;}
section[data-testid="stSidebar"] {display:none;}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------
# GLOBAL UI CSS (SAME AS MAIN APP)
# ----------------------------------------------------------
st.markdown("""
<style>
* { font-family:'Inter', sans-serif; }
body, [class*="css"] { color:#000 !important; font-size:16px; }

/* MAIN HEADER */
.big-header {
    font-size: 32px;
    font-weight: 700;
    color: #000;
    margin-bottom: 10px;
}

/* SECTION TITLE */
.section-title {
    font-size: 22px;
    font-weight: 600;
    margin-top: 28px;
    margin-bottom: 10px;
    position: relative;
    color: #000;
}
.section-title:after {
    content:"";
    position:absolute;
    bottom:-4px;
    left:0;
    height:2px;
    width:0%;
    background:#064b86;
    transition:0.35s ease;
}
.section-title:hover:after { width:40%; }

/* CARD */
.card {
    background:#ffffff;
    padding:18px;
    border-radius:12px;
    border:1px solid #e5e5e5;
    font-size:15.5px;
    box-shadow:0 3px 12px rgba(0,0,0,0.06);
    transition:all 0.25s ease;
}
.card:hover {
    transform:translateY(-3px);
    box-shadow:0 10px 22px rgba(6,75,134,0.18);
    border-color:#064b86;
}

/* KPI */
.kpi {
    background:#ffffff;
    padding:20px;
    border-radius:12px;
    border:1px solid #e2e2e2;
    font-size:18px;
    font-weight:600;
    text-align:center;
    color:#064b86;
    box-shadow:0 3px 10px rgba(0,0,0,0.05);
    transition:all 0.25s ease;
}
.kpi:hover {
    transform:translateY(-4px);
    box-shadow:0 12px 24px rgba(6,75,134,0.2);
}

/* Fade-in */
.block-container { animation: fadeIn 0.4s ease; }
@keyframes fadeIn {
    from {opacity:0; transform:translateY(8px);}
    to {opacity:1; transform:translateY(0);}
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------
# PLOTLY CHART HELPER
# ----------------------------------------------------------
def combo_chart_plotly(df, x_col, bar_col, line_col, title, line_suffix="%"):
    fig = go.Figure()
    if df.empty:
        fig.add_annotation(text="No data", x=0.5, y=0.5, showarrow=False)
        fig.update_layout(title=title, template="plotly_white")
        return fig

    colors = ["#2ecc71" if v >= 0 else "#e74c3c" for v in df[line_col]]

    fig.add_trace(go.Bar(
        x=df[x_col],
        y=df[bar_col],
        name=bar_col,
        marker_color=colors
    ))

    fig.add_trace(go.Scatter(
        x=df[x_col],
        y=df[line_col],
        mode="lines+markers+text",
        text=[f"{v:.1f}{line_suffix}" for v in df[line_col]],
        textposition="top center",
        line=dict(color="#2980b9", width=2)
    ))

    fig.update_layout(
        title=title,
        template="plotly_white",
        xaxis=dict(tickangle=-45),
        yaxis=dict(title=bar_col),
        yaxis2=dict(overlaying="y", side="right"),
        margin=dict(l=40, r=40, t=60, b=80)
    )
    return fig

# ----------------------------------------------------------
# MAIN TABS
# ----------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["Overview", "Important Attributes", "Application"])

# ----------------------------------------------------------
# TAB 1 — OVERVIEW
# ----------------------------------------------------------
with tab1:
    st.markdown("<div class='big-header'>Investor Projection Intelligence</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    A standalone investor-focused dashboard that projects revenue,
    EBITDA, FCF, valuation, ROI, IRR and terminal value.
    Built exclusively for presenting to angel investors or early-stage VCs.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Capabilities</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="card">
    • Multi-year revenue projection<br>
    • EBITDA margin expansion model<br>
    • Free cash flow (FCF) forecast<br>
    • Terminal valuation (EBITDA × Multiple)<br>
    • Investor payout simulation (equity stake)<br>
    • ROI, IRR and DCF valuation<br>
    • Automated investor insights<br>
    </div>
    """, unsafe_allow_html=True)

# ----------------------------------------------------------
# TAB 2 — IMPORTANT ATTRIBUTES
# ----------------------------------------------------------
with tab2:
    st.markdown("<div class='section-title'>Projection Inputs</div>", unsafe_allow_html=True)

    df_gloss = pd.DataFrame([
        ["Base Revenue", "Starting revenue for Year 1."],
        ["YoY Growth %", "Annual revenue growth assumption."],
        ["EBITDA Start %", "Initial EBITDA margin at Year 1."],
        ["EBITDA Improvement %", "Yearly improvement in EBITDA margin."],
        ["Reinvestment %", "Percent of revenue reinvested each year."],
        ["Projection Years (N)", "Number of forward years to model."],
        ["Investor Capital", "Amount invested."],
        ["Equity Stake %", "Ownership granted to investor."],
        ["Exit Multiple", "EBITDA × multiple at exit."],
        ["Discount Rate %", "Used for DCF valuation."]
    ], columns=["Field", "Description"])

    st.dataframe(df_gloss, width="stretch")

# ----------------------------------------------------------
# TAB 3 — APPLICATION
# ----------------------------------------------------------
with tab3:

    st.markdown("<div class='section-title'>Projection Inputs</div>", unsafe_allow_html=True)

    # LEFT SIDE INPUTS
    c1, c2 = st.columns(2)
    with c1:
        base_rev = st.number_input("Base Revenue (₹)", value=600000.0)
        growth_pct = st.number_input("YoY Growth (%)", value=25.0)
        ebitda_start_pct = st.number_input("Starting EBITDA Margin (%)", value=26.0)
        ebitda_growth_pct = st.number_input("EBITDA Margin YoY Improvement (%)", value=4.0)
        reinvest_pct = st.number_input("Reinvestment %", value=8.0)

    with c2:
        years = st.number_input("Projection Years", min_value=1, max_value=20, value=5)
        invest = st.number_input("Investor Capital (₹)", value=1000000.0)
        equity_pct = st.number_input("Equity Stake (%)", value=20.0)
        multiple = st.number_input("Exit EBITDA Multiple", value=6.0)
        discount_rate_pct = st.number_input("Discount Rate (%)", value=12.0)

    # ------------------------------------------------------
    # RUN PROJECTION
    # ------------------------------------------------------
    if st.button("Run Investor Projection"):

        years_arr = np.arange(1, years + 1)
        rev_list = []
        ebit_list = []
        margin_list = []
        fcf_list = []

        cur_rev = base_rev
        cur_margin = ebitda_start_pct / 100

        for _ in years_arr:
            rev_list.append(cur_rev)
            ebit = cur_rev * cur_margin
            ebit_list.append(ebit)
            margin_list.append(cur_margin * 100)
            fcf_list.append(ebit - cur_rev * (reinvest_pct / 100))
            cur_rev *= (1 + growth_pct/100)
            cur_margin *= (1 + ebitda_growth_pct/100)

        proj = pd.DataFrame({
            "Year": years_arr,
            "Revenue (₹)": rev_list,
            "EBITDA (₹)": ebit_list,
            "EBITDA %": margin_list,
            "FCF (₹)": fcf_list
        })

        proj["Valuation (₹)"] = proj["EBITDA (₹)"] * multiple
        terminal_value = proj["Valuation (₹)"].iloc[-1]
        investor_payout = terminal_value * (equity_pct/100)

        # IRR calculation
        cash_flows = [-invest] + [0]*(years-1) + [investor_payout]
        try:
            irr = nf.irr(cash_flows)
        except:
            irr = np.nan

        roi = (investor_payout - invest) / invest

        # DCF
        dcf_val = 0
        for idx, row in proj.iterrows():
            dcf_val += row["FCF (₹)"] / ((1 + discount_rate_pct/100)**row["Year"])
        dcf_val += terminal_value / ((1 + discount_rate_pct/100)**years)

        # TABLE
        st.markdown("<div class='section-title'>Projection Table</div>", unsafe_allow_html=True)
        st.dataframe(
            proj.style.format({
                "Revenue (₹)": "{:,.2f}",
                "EBITDA (₹)": "{:,.2f}",
                "EBITDA %": "{:.2f}",
                "FCF (₹)": "{:,.2f}",
                "Valuation (₹)": "{:,.2f}"
            }),
            width="stretch"
        )

        # CHART
        fig = combo_chart_plotly(proj, "Year", "Revenue (₹)", "EBITDA %", "Revenue + EBITDA% Projection")
        st.plotly_chart(fig, use_container_width=True)

        # KPI BLOCK
        st.markdown("<div class='section-title'>Investor Outcome</div>", unsafe_allow_html=True)
        k1, k2, k3, k4 = st.columns(4)
        k1.markdown(f"<div class='kpi'>Terminal Value<br/>₹{terminal_value:,.0f}</div>", unsafe_allow_html=True)
        k2.markdown(f"<div class='kpi'>Investor Payout<br/>₹{investor_payout:,.0f}</div>", unsafe_allow_html=True)
        k3.markdown(f"<div class='kpi'>ROI<br/>{roi*100:.2f}%</div>", unsafe_allow_html=True)
        k4.markdown(f"<div class='kpi'>IRR<br/>{'N/A' if np.isnan(irr) else f'{irr*100:.2f}%'} </div>", unsafe_allow_html=True)

        st.markdown(f"<div class='kpi'>DCF Valuation<br/>₹{dcf_val:,.0f}</div>", unsafe_allow_html=True)

        # INSIGHTS
        st.markdown("<div class='section-title'>Automated Insights</div>", unsafe_allow_html=True)

        insights = []
        if growth_pct >= 25:
            insights.append("Revenue growth rate indicates strong expansion potential.")
        if ebitda_start_pct >= 20:
            insights.append("EBITDA margin is healthy for an early-stage EdTech/Analytics company.")
        if roi >= 1:
            insights.append("Investment has a realistic chance of doubling the capital.")

        for i, text in enumerate(insights, start=1):
            st.markdown(f"<div class='card'><b>Insight {i}.</b> {text}</div>", unsafe_allow_html=True)
