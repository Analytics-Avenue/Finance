# app.py

import streamlit as st
import pandas as pd
import numpy as np
import numpy_financial as nf
import matplotlib.pyplot as plt
import plotly.express as px
from io import BytesIO
import tempfile

# Try PDF support (optional)
try:
    import pdfkit
    PDFKIT_AVAILABLE = True
except Exception:
    PDFKIT_AVAILABLE = False

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(page_title="EdTech Financial Intelligence Lab", layout="wide")

# Hide default sidebar
st.markdown("""
<style>
[data-testid="stSidebar"] {display:none;}
[data-testid="stSidebarNav"] {display:none;}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# BRANDING HEADER
# ---------------------------------------------------------
logo_url = "https://raw.githubusercontent.com/Analytics-Avenue/streamlit-dataapp/main/logo.png"

st.markdown(f"""
<div style="display:flex; align-items:center; margin-bottom:16px;">
    <img src="{logo_url}" width="60" style="margin-right:12px;">
    <div style="line-height:1;">
        <div style="color:#064b86; font-size:36px; font-weight:700;">Analytics Avenue</div>
        <div style="color:#064b86; font-size:28px; font-weight:600;">Financial Intelligence Lab</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# GLOBAL CSS – same visual style as your reference app
# ---------------------------------------------------------
st.markdown("""
<style>
* { font-family:'Inter', sans-serif; }
body, [class*="css"] { color:#000 !important; font-size:17px; }

/* HEADERS */
.big-header { font-size:36px; font-weight:700; color:#000; margin-bottom:14px; }
.section-title {
    font-size:24px; font-weight:600; margin-top:28px; margin-bottom:12px;
    position:relative; color:#000;
}
.section-title:after {
    content:""; position:absolute; bottom:-4px; left:0; height:2px; width:0%;
    background:#064b86; transition:0.35s ease;
}
.section-title:hover:after { width:40%; }

/* CARD */
.card {
    background:white; padding:20px; border-radius:14px; 
    border:1px solid #e5e5e5; font-size:16.5px; font-weight:500;
    box-shadow:0 3px 14px rgba(0,0,0,0.08);
    transition:all 0.25s ease;
}
.card:hover {
    transform:translateY(-4px);
    box-shadow:0 12px 25px rgba(6,75,134,0.18);
    border-color:#064b86;
}

/* KPI CARD */
.kpi {
    background:white; padding:22px; border-radius:14px;
    border:1px solid #e2e2e2; font-size:20px; font-weight:600;
    text-align:center; color:#064b86;
    box-shadow:0 3px 14px rgba(0,0,0,0.07);
    transition:0.25s ease;
}
.kpi:hover {
    transform:translateY(-6px);
    box-shadow:0 13px 26px rgba(6,75,134,0.20);
}

/* VARIABLE BOX */
.variable-box {
    padding:14px; border-radius:12px; background:#ffffff;
    border:1px solid #e5e5e5; font-size:16px; font-weight:500;
    color:#064b86; text-align:left;
    box-shadow:0 2px 10px rgba(0,0,0,0.06);
    margin-bottom:8px;
}

/* Fade-in */
.block-container { animation:fadeIn 0.4s ease; }
@keyframes fadeIn {
    from {opacity:0; transform:translateY(10px);}
    to {opacity:1; transform:translateY(0);}
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='big-header'>EdTech Financial Intelligence Dashboard</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# REQUIRED FIELDS FOR REVENUE DATASET
# ---------------------------------------------------------
REQUIRED_COLS = [
    "first_payment_date",
    "collected_amount",
    "total_fee",
    "joined_or_not",
    "pay_status",
    "campaign_name",
    "lead_created_date",
    "batch",
    "pending_amount",
    "co_assignee"
]

# ---------------------------------------------------------
# TABS
# ---------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["Overview", "Important Attributes", "Application"])

# =========================================================
# TAB 1 - OVERVIEW
# =========================================================
with tab1:
    st.markdown("<div class='section-title'>Overview</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="card">
    This lab gives you a complete **financial and investor analytics cockpit** for your EdTech + Analytics business.
    It connects actual revenue data with projections, growth analytics, investor outcome modeling, and market context.
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='section-title'>What This App Delivers</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="card">
        • Revenue trend analysis (Monthly / Quarterly / Annual)<br>
        • MoM / QoQ / YoY growth calculation<br>
        • EBITDA, Terminal Value, IRR, ROI and 5-year projection<br>
        • Market size overlay vs your revenue trajectory<br>
        • Competitor benchmarking view<br>
        • Automated financial insights for your deck
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='section-title'>Who Should Use This</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="card">
        • Founders raising in the next 3–12 months<br>
        • Finance and strategy leads<br>
        • Investor relations and reporting<br>
        • EdTech revenue & growth teams<br>
        • Anyone tired of juggling 14 Excel files
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Core KPIs Tracked</div>", unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)
    k1.markdown("<div class='kpi'>Revenue</div>", unsafe_allow_html=True)
    k2.markdown("<div class='kpi'>EBITDA Margin</div>", unsafe_allow_html=True)
    k3.markdown("<div class='kpi'>IRR</div>", unsafe_allow_html=True)
    k4.markdown("<div class='kpi'>Terminal Value</div>", unsafe_allow_html=True)

# =========================================================
# TAB 2 - IMPORTANT ATTRIBUTES
# =========================================================
with tab2:
    st.markdown("<div class='section-title'>Required Revenue Dataset Columns</div>", unsafe_allow_html=True)

    desc_map = {
        "first_payment_date": "First payment date from student (used for time slicing).",
        "collected_amount": "Amount collected from the student / client (₹).",
        "total_fee": "Total course / program fee for that deal/student.",
        "joined_or_not": "Whether the student actually joined (Yes/No or 1/0).",
        "pay_status": "Payment completion flag (Paid/Partially paid/Pending).",
        "campaign_name": "Campaign / source attribution for CAC analysis.",
        "lead_created_date": "Date when the lead was created.",
        "batch": "Batch identifier for the program.",
        "pending_amount": "Fee still pending from the student (₹).",
        "co_assignee": "Coordinator / sales owner name for performance split."
    }

    df_gloss = pd.DataFrame(
        [{"Field": k, "Description": v} for k, v in desc_map.items()]
    )
    st.dataframe(df_gloss, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='section-title'>Key Financial Metrics</div>", unsafe_allow_html=True)
        metrics_list = [
            "Total Revenue",
            "Operational Cost",
            "OPEX",
            "Gross Profit & Margin",
            "EBITDA & EBITDA Margin",
            "Net Profit & Net Margin",
            "Free Cash Flow (FCF)",
            "Burn Rate & Runway",
            "ARR / MRR"
        ]
        for m in metrics_list:
            st.markdown(f"<div class='variable-box'>{m}</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='section-title'>Investor & Growth Metrics</div>", unsafe_allow_html=True)
        metrics_list_2 = [
            "IRR (Internal Rate of Return)",
            "ROI (Return on Investment)",
            "DCF (Discounted Cash Flow) logic",
            "Terminal Value (EBITDA × multiple)",
            "CAGR (Revenue growth curve)",
            "MoM / QoQ / YoY trend view",
            "Competitor comparisons"
        ]
        for m in metrics_list_2:
            st.markdown(f"<div class='variable-box'>{m}</div>", unsafe_allow_html=True)


# =========================================================
# TAB 3 - APPLICATION
# =========================================================
with tab3:

    st.markdown("<div class='section-title'>Step 1: Load Revenue Dataset</div>", unsafe_allow_html=True)

    df_rev = None

    mode = st.radio(
        "Choose dataset mode:",
        ["Google Sheet link", "Upload CSV + Column Mapping"],
        horizontal=True
    )

    # -----------------------------
    # MODE 1: GOOGLE SHEET LINK
    # -----------------------------
    if mode == "Google Sheet link":
        sheet_url = st.text_input("Paste your Google Sheet link (must be public or accessible):", "")

        if sheet_url:
            try:
                sheet_id = sheet_url.split("/d/")[1].split("/")[0]
                csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
                df_raw = pd.read_csv(csv_url)
                df_raw.columns = df_raw.columns.str.strip().str.lower().str.replace(" ", "_")
                st.success("Google Sheet loaded successfully.")
                st.dataframe(df_raw.head(), use_container_width=True)
                df_rev = df_raw.copy()
            except Exception as e:
                st.error(f"Failed to load Google Sheet: {e}")

    # -----------------------------
    # MODE 2: UPLOAD CSV + COLUMN MAPPING
    # -----------------------------
    else:
        uploaded = st.file_uploader("Upload CSV file", type=["csv"])
        if uploaded is not None:
            df_raw = pd.read_csv(uploaded)
            df_raw.columns = df_raw.columns.str.strip().str.lower().str.replace(" ", "_")

            st.markdown("Preview of uploaded file:")
            st.dataframe(df_raw.head(), use_container_width=True)

            st.markdown("Map your columns to required fields:")
            mapping = {}
            for req in REQUIRED_COLS:
                mapping[req] = st.selectbox(
                    f"Map to → {req}",
                    options=["-- Select --"] + list(df_raw.columns),
                    key=f"map_{req}"
                )

            if st.button("Apply Mapping"):
                missing = [k for k, v in mapping.items() if v == "-- Select --"]
                if missing:
                    st.error("Please map all required fields: " + ", ".join(missing))
                else:
                    inv = {v: k for k, v in mapping.items()}
                    df_mapped = df_raw.rename(columns=inv)
                    st.success("Mapping applied successfully.")
                    st.dataframe(df_mapped.head(), use_container_width=True)
                    df_rev = df_mapped.copy()

    # If still nothing loaded
    if df_rev is None:
        st.info("Load a dataset using one of the modes to unlock analytics.")
        st.stop()

    # -----------------------------------------------------
    # BASIC PREPROCESSING
    # -----------------------------------------------------
    df = df_rev.copy()  # <- use df internally from here
    if "first_payment_date" not in df.columns or "collected_amount" not in df.columns:
        st.error("Dataset must at least have 'first_payment_date' and 'collected_amount' columns after mapping.")
        st.stop()

    df["first_payment_date"] = pd.to_datetime(df["first_payment_date"], errors="coerce")
    df = df.dropna(subset=["first_payment_date"])
    df["collected_amount"] = pd.to_numeric(df["collected_amount"], errors="coerce").fillna(0)

    df["year"] = df["first_payment_date"].dt.year
    df["month_period"] = df["first_payment_date"].dt.to_period("M")
    df["quarter_period"] = df["first_payment_date"].dt.to_period("Q")

    st.markdown("<div class='section-title'>Step 2: Data Snapshot</div>", unsafe_allow_html=True)
    st.dataframe(df.head(10), use_container_width=True)

    # -----------------------------------------------------
    # REVENUE SPLITS + MOM / QOQ / YOY
    # -----------------------------------------------------
    st.markdown("<div class='section-title'>Revenue & Growth Analytics</div>", unsafe_allow_html=True)

    monthly = df.groupby("month_period")["collected_amount"].sum().sort_index()
    quarterly = df.groupby("quarter_period")["collected_amount"].sum().sort_index()
    yearly = df.groupby("year")["collected_amount"].sum().sort_index()

    mom = monthly.pct_change() * 100
    qoq = quarterly.pct_change() * 100
    yoy = yearly.pct_change() * 100

    # -----------------------------
    # MONTHLY: TABLE → CHART
    # -----------------------------
    st.markdown("### 📌 Monthly Revenue (Table)")
    monthly_df = monthly.to_frame("Revenue (₹)").reset_index()
    monthly_df["month_period"] = monthly_df["month_period"].astype(str)
    st.dataframe(monthly_df.style.format({"Revenue (₹)": "{:,.2f}"}), use_container_width=True)

    st.markdown("### 📈 Monthly Revenue Trend")
    if len(monthly_df) > 0:
        fig_m1, ax_m1 = plt.subplots(figsize=(11,5))
        ax_m1.plot(monthly_df["month_period"], monthly_df["Revenue (₹)"], marker="o", color="#064b86")
        ax_m1.set_xlabel("Month")
        ax_m1.set_ylabel("Revenue (₹)")
        ax_m1.grid(alpha=0.3)
        plt.xticks(rotation=45)
        st.pyplot(fig_m1)
    else:
        st.info("Not enough data for monthly chart.")

    st.markdown("---")

    # -----------------------------
    # MoM GROWTH: TABLE → CHART
    # -----------------------------
    st.markdown("### 📌 MoM Growth (%)")
    mom_df = mom.to_frame("MoM %").reset_index()
    mom_df["month_period"] = mom_df["month_period"].astype(str)
    st.dataframe(mom_df.style.format({"MoM %": "{:.2f}"}), use_container_width=True)

    st.markdown("### 📈 MoM Growth Trend")
    if len(mom_df) > 1:
        fig_m2, ax_m2 = plt.subplots(figsize=(11,5))
        ax_m2.bar(mom_df["month_period"], mom_df["MoM %"], color="#ff6b6b", alpha=0.8)
        ax_m2.set_xlabel("Month")
        ax_m2.set_ylabel("MoM Growth %")
        ax_m2.grid(alpha=0.3)
        plt.xticks(rotation=45)
        st.pyplot(fig_m2)
    else:
        st.info("Need at least 2 months for MoM trend.")

    st.markdown("---")

    # -----------------------------
    # QUARTERLY: TABLE → CHART
    # -----------------------------
    st.markdown("### 📌 Quarterly Revenue (Table)")
    quarterly_df = quarterly.to_frame("Revenue (₹)").reset_index()
    quarterly_df["quarter_period"] = quarterly_df["quarter_period"].astype(str)
    st.dataframe(quarterly_df.style.format({"Revenue (₹)": "{:,.2f}"}), use_container_width=True)

    st.markdown("### 📈 Quarterly Revenue Trend")
    if len(quarterly_df) > 0:
        fig_q1, ax_q1 = plt.subplots(figsize=(11,5))
        ax_q1.bar(quarterly_df["quarter_period"], quarterly_df["Revenue (₹)"], color="#064b86")
        ax_q1.set_xlabel("Quarter")
        ax_q1.set_ylabel("Revenue (₹)")
        ax_q1.grid(alpha=0.3)
        plt.xticks(rotation=45)
        st.pyplot(fig_q1)
    else:
        st.info("Not enough data for quarterly chart.")

    st.markdown("---")

    # -----------------------------
    # QoQ: TABLE → CHART
    # -----------------------------
    st.markdown("### 📌 QoQ Growth (%)")
    qoq_df = qoq.to_frame("QoQ %").reset_index()
    qoq_df["quarter_period"] = qoq_df["quarter_period"].astype(str)
    st.dataframe(qoq_df.style.format({"QoQ %": "{:.2f}"}), use_container_width=True)

    st.markdown("### 📈 QoQ Growth Trend")
    if len(qoq_df) > 1:
        fig_q2, ax_q2 = plt.subplots(figsize=(11,5))
        ax_q2.plot(qoq_df["quarter_period"], qoq_df["QoQ %"], marker="o", color="red")
        ax_q2.set_xlabel("Quarter")
        ax_q2.set_ylabel("QoQ Growth %")
        ax_q2.grid(alpha=0.3)
        plt.xticks(rotation=45)
        st.pyplot(fig_q2)
    else:
        st.info("Need at least 2 quarters for QoQ trend.")

    st.markdown("---")

    # -----------------------------
    # ANNUAL: TABLE → CHART
    # -----------------------------
    st.markdown("### 📌 Annual Revenue (Table)")
    yearly_df = yearly.to_frame("Revenue (₹)").reset_index()
    st.dataframe(yearly_df.style.format({"Revenue (₹)": "{:,.2f}"}), use_container_width=True)

    st.markdown("### 📈 Annual Revenue Trend")
    if len(yearly_df) > 0:
        fig_y1, ax_y1 = plt.subplots(figsize=(11,5))
        ax_y1.bar(yearly_df["year"], yearly_df["Revenue (₹)"], color="#064b86")
        ax_y1.set_xlabel("Year")
        ax_y1.set_ylabel("Revenue (₹)")
        ax_y1.grid(alpha=0.3)
        st.pyplot(fig_y1)
    else:
        st.info("Not enough data for annual chart.")

    st.markdown("---")

    # -----------------------------
    # YoY: TABLE → CHART
    # -----------------------------
    st.markdown("### 📌 YoY Growth (%)")
    yoy_df = yoy.to_frame("YoY %").reset_index()
    st.dataframe(yoy_df.style.format({"YoY %": "{:.2f}"}), use_container_width=True)

    st.markdown("### 📈 YoY Growth Trend")
    if len(yoy_df) > 1:
        fig_y2, ax_y2 = plt.subplots(figsize=(11,5))
        ax_y2.plot(yoy_df["year"], yoy_df["YoY %"], marker="o", color="red")
        ax_y2.set_xlabel("Year")
        ax_y2.set_ylabel("YoY Growth %")
        ax_y2.grid(alpha=0.3)
        st.pyplot(fig_y2)
    else:
        st.info("Need at least 2 years for YoY trend.")

    st.markdown("---")

    # -----------------------------------------------------
    # CORE KPIs
    # -----------------------------------------------------
    total_revenue = df["collected_amount"].sum()
    latest_year = yearly.index.max() if len(yearly) > 0 else None
    latest_year_revenue = yearly.loc[latest_year] if latest_year is not None else 0
    avg_yoy = yoy.dropna().mean() if len(yoy.dropna()) > 0 else np.nan

    st.markdown("<div class='section-title'>Core KPIs</div>", unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(f"<div class='kpi'>Total Revenue<br/>₹{total_revenue:,.0f}</div>", unsafe_allow_html=True)
    if latest_year is not None:
        k2.markdown(f"<div class='kpi'>Latest Year<br/>{int(latest_year)}</div>", unsafe_allow_html=True)
        k3.markdown(f"<div class='kpi'>Latest Year Revenue<br/>₹{latest_year_revenue:,.0f}</div>", unsafe_allow_html=True)
    else:
        k2.markdown(f"<div class='kpi'>Latest Year<br/>N/A</div>", unsafe_allow_html=True)
        k3.markdown(f"<div class='kpi'>Latest Year Revenue<br/>N/A</div>", unsafe_allow_html=True)
    if not np.isnan(avg_yoy):
        k4.markdown(f"<div class='kpi'>Avg YoY Growth<br/>{avg_yoy:.2f}%</div>", unsafe_allow_html=True)
    else:
        k4.markdown(f"<div class='kpi'>Avg YoY Growth<br/>N/A</div>", unsafe_allow_html=True)

    st.markdown("---")

    # -----------------------------------------------------
    # INVESTOR MODEL (5-YEAR)
    # -----------------------------------------------------
    st.markdown("<div class='section-title'>Investor Projection & Valuation Model</div>", unsafe_allow_html=True)

    colA, colB = st.columns(2)
    with colA:
        base_revenue = st.number_input(
            "Base Annual Revenue for Year 1 (₹)",
            value=float(latest_year_revenue if latest_year_revenue > 0 else total_revenue),
            step=100000.0
        )
        growth_rate = st.number_input("YoY Growth (0.25 = 25%)", min_value=0.0, max_value=1.0, value=0.25)
        ebitda_margin = st.number_input("EBITDA Margin (0.26 = 26%)", min_value=0.0, max_value=1.0, value=0.26)

    with colB:
        investment = st.number_input("Investor Total Investment (₹)", min_value=0.0, step=100000.0, value=1000000.0)
        equity = st.number_input("Equity % (0.20 = 20%)", min_value=0.0, max_value=1.0, value=0.20)
        exit_multiple = st.number_input("Exit EBITDA Multiple (X)", min_value=1.0, max_value=20.0, value=6.0)

    if st.button("Run 5-Year Projection & Investor Outcome"):

        years_proj = np.arange(1, 6)
        rev_proj = []
        ebit_proj = []
        cur = base_revenue

        for _ in years_proj:
            rev_proj.append(cur)
            ebit_proj.append(cur * ebitda_margin)
            cur *= (1 + growth_rate)

        df_proj = pd.DataFrame({
            "Year": years_proj,
            "Revenue (₹)": rev_proj,
            "EBITDA (₹)": ebit_proj,
            "Valuation (₹)": np.array(ebit_proj) * exit_multiple
        })

        st.write("### 5-Year Projection Table")
        st.dataframe(df_proj.style.format("{:,.2f}"), use_container_width=True)

        terminal_value = df_proj["Valuation (₹)"].iloc[-1]
        investor_payout = terminal_value * equity
        net_gain = investor_payout - investment
        roi = net_gain / investment if investment > 0 else np.nan
        irr = nf.irr([-investment] + [0, 0, 0, investor_payout]) if investment > 0 else np.nan

        k1, k2, k3, k4 = st.columns(4)
        k1.markdown(f"<div class='kpi'>Terminal Value<br/>₹{terminal_value:,.0f}</div>", unsafe_allow_html=True)
        k2.markdown(f"<div class='kpi'>Investor Payout<br/>₹{investor_payout:,.0f}</div>", unsafe_allow_html=True)
        if not np.isnan(roi):
            k3.markdown(f"<div class='kpi'>ROI<br/>{roi*100:.2f}%</div>", unsafe_allow_html=True)
        else:
            k3.markdown(f"<div class='kpi'>ROI<br/>N/A</div>", unsafe_allow_html=True)
        if not np.isnan(irr):
            k4.markdown(f"<div class='kpi'>IRR<br/>{irr*100:.2f}%</div>", unsafe_allow_html=True)
        else:
            k4.markdown(f"<div class='kpi'>IRR<br/>N/A</div>", unsafe_allow_html=True)

        st.write("### Revenue vs EBITDA Projection")
        fig2, ax2 = plt.subplots(figsize=(11,5))
        ax2.bar(df_proj["Year"], df_proj["Revenue (₹)"], label="Revenue (₹)", alpha=0.7)
        ax2.plot(df_proj["Year"], df_proj["EBITDA (₹)"], color="red", marker="o", label="EBITDA (₹)")
        ax2.set_xlabel("Year")
        ax2.set_ylabel("Amount (₹)")
        ax2.grid(alpha=0.3)
        ax2.legend()
        st.pyplot(fig2)

        # -------------------------------------------------
        # COMPETITOR COMPARISON (STATIC)
        # -------------------------------------------------
        st.markdown("<div class='section-title'>Competitor Comparison (Static Benchmarks)</div>", unsafe_allow_html=True)

        competitors = pd.DataFrame({
            "Company": ["Your Org", "Scaler", "UpGrad", "Simplilearn", "Great Learning"],
            "Revenue_Cr": [
                base_revenue / 1e7,
                400, 1200, 600, 800
            ],
            "EBITDA_Margin": [
                ebitda_margin,
                0.14, 0.09, 0.11, 0.12
            ],
            "YoY_Growth": [
                growth_rate,
                0.29, 0.24, 0.18, 0.22
            ]
        })

        st.dataframe(
            competitors.style.format({
                "Revenue_Cr": "{:,.1f}",
                "EBITDA_Margin": "{:.1%}",
                "YoY_Growth": "{:.1%}"
            }),
            use_container_width=True
        )

        fig3 = px.bar(
            competitors,
            x="Company",
            y="Revenue_Cr",
            title="Revenue Benchmark (₹ Cr)",
            text="Revenue_Cr"
        )
        fig3.update_traces(texttemplate="%{text:.1f}", textposition="outside")
        fig3.update_layout(yaxis_title="Revenue (₹ Cr)")
        st.plotly_chart(fig3, use_container_width=True)

        # -------------------------------------------------
        # AUTOMATED INSIGHTS
        # -------------------------------------------------
        st.markdown("<div class='section-title'>Automated Insights</div>", unsafe_allow_html=True)

        insights = []

        if len(mom.dropna()) > 0 and mom.dropna().mean() > 5:
            insights.append("Your average MoM growth is strong, indicating healthy short-term demand.")

        if len(yoy.dropna()) > 0 and yoy.dropna().mean() > 20:
            insights.append("Your YoY growth is above typical EdTech benchmarks, which is attractive to investors.")

        if ebitda_margin >= 0.25:
            insights.append("EBITDA margin ≥ 25% signals strong cost discipline and good unit economics.")

        if growth_rate > competitors["YoY_Growth"].median():
            insights.append("Your assumed growth rate is higher than major competitors, positioning you as a high-growth asset.")

        if terminal_value < base_revenue * 2:
            insights.append("Terminal value isn't very aggressive vs Year 1 revenue. Consider validating your growth or multiple assumptions.")

        if not insights:
            insights.append("No unusual red flags or outliers in your current assumptions. The model looks balanced.")

        for text in insights:
            st.markdown(f"<div class='card'>{text}</div>", unsafe_allow_html=True)
