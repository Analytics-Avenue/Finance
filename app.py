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

    # -----------------------------
    # DATASET UPLOAD SECTION
    # -----------------------------
    st.markdown("<div class='section-title'>Step 1: Load Revenue Dataset</div>", unsafe_allow_html=True)

    df_rev = None

    mode = st.radio(
        "Choose dataset mode:",
        ["Google Sheet link", "Upload CSV + Column Mapping"],
        horizontal=True
    )

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

    else:  # Upload CSV + mapping
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

    if df_rev is None:
        st.info("Load a dataset using one of the modes to unlock analytics.")
        st.stop()

    # -----------------------------
    # BASIC PREPROCESSING
    # -----------------------------
    if "first_payment_date" not in df_rev.columns or "collected_amount" not in df_rev.columns:
        st.error("Dataset must at least have 'first_payment_date' and 'collected_amount'.")
        st.stop()

    df_rev["first_payment_date"] = pd.to_datetime(df_rev["first_payment_date"], errors="coerce")
    df_rev = df_rev.dropna(subset=["first_payment_date"])
    df_rev["collected_amount"] = pd.to_numeric(df_rev["collected_amount"], errors="coerce").fillna(0)

    # Date splits
    df_rev["year"] = df_rev["first_payment_date"].dt.year
    df_rev["month_period"] = df_rev["first_payment_date"].dt.to_period("M")
    df_rev["quarter_period"] = df_rev["first_payment_date"].dt.to_period("Q")

    st.markdown("<div class='section-title'>Step 2: Data Snapshot</div>", unsafe_allow_html=True)
    st.dataframe(df_rev.head(10), use_container_width=True)

    # ----------------------------------------------
    # REVENUE SPLITS + MOM / QOQ / YOY CALCULATIONS
    # ----------------------------------------------
    
    # Ensure collected_amount exists
    if "collected_amount" not in df.columns:
        st.error("Your dataset does not have a 'collected_amount' column.")
        st.stop()
    
    # Ensure date column is clean
    df['first_payment_date'] = pd.to_datetime(df['first_payment_date'], errors='coerce')
    df = df.dropna(subset=['first_payment_date'])
    
    # -----------------------------
    # MONTHLY REVENUE
    # -----------------------------
    monthly = (
        df.groupby(df['first_payment_date'].dt.to_period("M"))['collected_amount']
        .sum()
    )
    monthly.index.name = "month_period"
    
    # -----------------------------
    # QUARTERLY REVENUE
    # -----------------------------
    quarterly = (
        df.groupby(df['first_payment_date'].dt.to_period("Q"))['collected_amount']
        .sum()
    )
    quarterly.index.name = "quarter_period"
    
    # -----------------------------
    # ANNUAL REVENUE
    # -----------------------------
    yearly = (
        df.groupby(df['first_payment_date'].dt.year)['collected_amount']
        .sum()
    )
    yearly.index.name = "year"
    
    # -----------------------------
    # MoM Growth
    # -----------------------------
    mom = monthly.pct_change() * 100
    mom.index.name = "month_period"
    
    # -----------------------------
    # QoQ Growth
    # -----------------------------
    qoq = quarterly.pct_change() * 100
    qoq.index.name = "quarter_period"
    
    # -----------------------------
    # YoY Growth
    # -----------------------------
    yoy = yearly.pct_change() * 100
    yoy.index.name = "year"

    # -----------------------------------------------------
    # CLEAN & ORDERED REVENUE + GROWTH ANALYTICS
    # -----------------------------------------------------
    
    st.markdown("<div class='section-title'>Revenue & Growth Analytics</div>", unsafe_allow_html=True)
    
    # --- Monthly Revenue Table ---
    st.markdown("### Monthly Revenue (Table)")
    monthly_df = monthly.to_frame("Revenue (₹)").reset_index()
    monthly_df["month_period"] = monthly_df["month_period"].astype(str)
    st.dataframe(monthly_df.style.format({"Revenue (₹)": "{:,.2f}"}), use_container_width=True)
    
    st.markdown("### Monthly Revenue Trend Chart")
    fig1, ax1 = plt.subplots(figsize=(11,5))
    ax1.plot(monthly_df["month_period"], monthly_df["Revenue (₹)"], marker="o", color="#064b86")
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Revenue (₹)")
    ax1.grid(alpha=0.3)
    plt.xticks(rotation=45)
    st.pyplot(fig1)
    
    st.markdown("---")
    
    # --- MoM Growth Table ---
    st.markdown("### MoM Growth (%)")
    mom_df = mom.to_frame("MoM %").reset_index()
    mom_df["month_period"] = mom_df["month_period"].astype(str)
    st.dataframe(mom_df.style.format({"MoM %": "{:.2f}"}), use_container_width=True)
    
    st.markdown("### MoM Growth Trend Chart")
    fig1b, ax1b = plt.subplots(figsize=(11,5))
    ax1b.bar(mom_df["month_period"], mom_df["MoM %"], color="#ff6b6b", alpha=0.8)
    ax1b.set_xlabel("Month")
    ax1b.set_ylabel("MoM Growth %")
    ax1b.grid(alpha=0.3)
    plt.xticks(rotation=45)
    st.pyplot(fig1b)
    
    st.markdown("---")
    
    # --- Quarterly Revenue Table ---
    st.markdown("### Quarterly Revenue (Table)")
    quarterly_df = quarterly.to_frame("Revenue (₹)").reset_index()
    quarterly_df["quarter_period"] = quarterly_df["quarter_period"].astype(str)
    st.dataframe(quarterly_df.style.format({"Revenue (₹)": "{:,.2f}"}), use_container_width=True)
    
    st.markdown("### Quarterly Revenue Trend Chart")
    fig2, ax2 = plt.subplots(figsize=(11,5))
    ax2.bar(quarterly_df["quarter_period"], quarterly_df["Revenue (₹)"], color="#064b86")
    ax2.set_xlabel("Quarter")
    ax2.set_ylabel("Revenue (₹)")
    ax2.grid(alpha=0.3)
    plt.xticks(rotation=45)
    st.pyplot(fig2)
    
    st.markdown("---")
    
    # --- QoQ Growth Table ---
    st.markdown("### QoQ Growth (%)")
    qoq_df = qoq.to_frame("QoQ %").reset_index()
    qoq_df["quarter_period"] = qoq_df["quarter_period"].astype(str)
    st.dataframe(qoq_df.style.format({"QoQ %": "{:.2f}"}), use_container_width=True)
    
    st.markdown("### QoQ Growth Trend Chart")
    fig2b, ax2b = plt.subplots(figsize=(11,5))
    ax2b.plot(qoq_df["quarter_period"], qoq_df["QoQ %"], marker="o", linewidth=2, color="red")
    ax2b.set_xlabel("Quarter")
    ax2b.set_ylabel("QoQ Growth %")
    ax2b.grid(alpha=0.3)
    plt.xticks(rotation=45)
    st.pyplot(fig2b)
    
    st.markdown("---")
    
    # --- Annual Revenue Table ---
    st.markdown("### Annual Revenue (Table)")
    yearly_df = yearly.to_frame("Revenue (₹)").reset_index()
    st.dataframe(yearly_df.style.format({"Revenue (₹)": "{:,.2f}"}), use_container_width=True)
    
    st.markdown("### Annual Revenue Bar Chart")
    fig3, ax3 = plt.subplots(figsize=(11,5))
    ax3.bar(yearly_df["year"], yearly_df["Revenue (₹)"], color="#064b86")
    ax3.set_xlabel("Year")
    ax3.set_ylabel("Revenue (₹)")
    ax3.grid(alpha=0.3)
    st.pyplot(fig3)
    
    st.markdown("---")
    
    # --- YoY Growth Table ---
    st.markdown("### YoY Growth (%)")
    yoy_df = yoy.to_frame("YoY %").reset_index()
    st.dataframe(yoy_df.style.format({"YoY %": "{:.2f}"}), use_container_width=True)
    
    st.markdown("### YoY Growth Trend Chart")
    fig3b, ax3b = plt.subplots(figsize=(11,5))
    ax3b.plot(yoy_df["year"], yoy_df["YoY %"], marker="o", color="red")
    ax3b.set_xlabel("Year")
    ax3b.set_ylabel("YoY Growth %")
    ax3b.grid(alpha=0.3)
    st.pyplot(fig3b)
    
    st.markdown("---")
    # -----------------------------------------------------
    # BASIC COMPANY KPIs FROM DATA
    # -----------------------------------------------------
    total_revenue = df_rev["collected_amount"].sum()
    unique_students = df_rev["batch"].nunique() if "batch" in df_rev.columns else np.nan
    latest_year = yearly.index.max()
    latest_year_revenue = yearly.loc[latest_year] if len(yearly) > 0 else 0

    st.markdown("<div class='section-title'>Core Revenue KPIs (from dataset)</div>", unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(f"<div class='kpi'>Total Revenue<br/>₹{total_revenue:,.0f}</div>", unsafe_allow_html=True)
    if not np.isnan(unique_students):
        k2.markdown(f"<div class='kpi'>Unique Batches<br/>{int(unique_students)}</div>", unsafe_allow_html=True)
    else:
        k2.markdown(f"<div class='kpi'>Unique Batches<br/>N/A</div>", unsafe_allow_html=True)
    k3.markdown(f"<div class='kpi'>Latest Year Revenue<br/>₹{latest_year_revenue:,.0f}</div>", unsafe_allow_html=True)
    if len(yoy.dropna()) > 0:
        k4.markdown(f"<div class='kpi'>Avg YoY Growth<br/>{yoy.dropna().mean():.2f}%</div>", unsafe_allow_html=True)
    else:
        k4.markdown(f"<div class='kpi'>Avg YoY Growth<br/>N/A</div>", unsafe_allow_html=True)

    # -----------------------------------------------------
    # INVESTOR MODEL (5-YEAR PROJECTION BASED ON LATEST YEAR)
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

        years = np.arange(1, 6)
        rev_proj = []
        ebit_proj = []
        cur = base_revenue

        for _ in years:
            rev_proj.append(cur)
            ebit_proj.append(cur * ebitda_margin)
            cur *= (1 + growth_rate)

        df_proj = pd.DataFrame({
            "Year": years,
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

        # Chart: revenue vs EBITDA
        st.write("### Revenue vs EBITDA Projection")
        fig2, ax = plt.subplots(figsize=(10,5))
        ax.bar(df_proj["Year"], df_proj["Revenue (₹)"], label="Revenue (₹)", alpha=0.7)
        ax.plot(df_proj["Year"], df_proj["EBITDA (₹)"], color="red", marker="o", label="EBITDA (₹)")
        plt.grid(True, alpha=0.3)
        plt.legend()
        st.pyplot(fig2)

        # ------------------------
        # COMPETITOR COMPARISON
        # ------------------------
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

        # ------------------------
        # AUTOMATED INSIGHTS
        # ------------------------
        st.markdown("<div class='section-title'>Automated Insights</div>", unsafe_allow_html=True)

        insights = []

        if len(mom.dropna()) > 0 and mom.dropna().mean() > 5:
            insights.append("Your average MoM growth is strong, indicating healthy short-term momentum in revenue.")

        if len(yoy.dropna()) > 0 and yoy.dropna().mean() > 20:
            insights.append("Your YoY growth is above typical EdTech benchmarks, which is attractive for investors.")

        if ebitda_margin >= 0.25:
            insights.append("EBITDA margins at or above 25% signal a lean cost structure and strong unit economics.")

        if growth_rate > competitors["YoY_Growth"].median():
            insights.append("Your assumed forward growth rate is higher than most key market players, positioning you as a high-growth asset.")

        if terminal_value < base_revenue * 2:
            insights.append("Terminal value is not very aggressive relative to base revenue; consider validating your multiple or growth assumptions.")

        if not insights:
            insights.append("No major red flags or standout strengths detected. Your assumptions look moderate and stable.")

        for text in insights:
            st.markdown(f"<div class='card'>{text}</div>", unsafe_allow_html=True)

        # ------------------------
        # PDF DOWNLOAD (if pdfkit available)
        # ------------------------
        st.markdown("<div class='section-title'>Download Summary</div>", unsafe_allow_html=True)

        if PDFKIT_AVAILABLE:
            if st.button("Generate & Download PDF Summary"):
                html = f"""
                <h1>EdTech Financial Summary</h1>
                <h2>Key Numbers</h2>
                <p><b>Total Revenue (data):</b> ₹{total_revenue:,.0f}</p>
                <p><b>Base Revenue (Year 1):</b> ₹{base_revenue:,.0f}</p>
                <p><b>Terminal Value:</b> ₹{terminal_value:,.0f}</p>
                <p><b>Investor Payout:</b> ₹{investor_payout:,.0f}</p>
                <p><b>ROI:</b> {roi*100:.2f}%</p>
                <p><b>IRR:</b> {irr*100:.2f}%</p>
                <h2>Insights</h2>
                <ul>
                {''.join([f'<li>{ins}</li>' for ins in insights])}
                </ul>
                """

                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
                    pdfkit.from_string(html, tmpfile.name)
                    tmpfile.seek(0)
                    pdf_bytes = tmpfile.read()

                st.download_button(
                    "Download PDF",
                    data=pdf_bytes,
                    file_name="EdTech_Financial_Summary.pdf",
                    mime="application/pdf"
                )
        else:
            st.info("pdfkit not available. Install pdfkit & wkhtmltopdf on server to enable PDF export.")
