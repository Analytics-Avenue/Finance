import streamlit as st
import pandas as pd
import numpy as np
import numpy_financial as nf
import plotly.graph_objects as go

# Header & Logo
# -------------------------
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

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="EdTech Financial Intelligence Dashboard",
    layout="wide"
)

# Hide default sidebar nav (optional)
st.markdown("""
<style>
[data-testid="stSidebarNav"] {display:none;}
section[data-testid="stSidebar"] {display:none;}
</style>
""", unsafe_allow_html=True)

# =========================================================
# GLOBAL CSS
# =========================================================
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

/* KPI CARD */
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

/* VARIABLE BOX */
.variable-box {
    padding:12px;
    border-radius:10px;
    border:1px solid #e0e0e0;
    background:#ffffff;
    color:#064b86;
    font-weight:500;
    margin-bottom:8px;
}

/* Fade in */
.block-container {
    animation: fadeIn 0.4s ease;
}
@keyframes fadeIn {
    from {opacity:0; transform:translateY(8px);}
    to {opacity:1; transform:translateY(0);}
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# PLOTLY COMBO CHART HELPER (BAR + LINE, GREEN/RED TREND)
# =========================================================
def combo_chart_plotly(df, x_col, bar_col, line_col, title, line_suffix="%"):
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No data", x=0.5, y=0.5, showarrow=False)
        fig.update_layout(title=title, template="plotly_white")
        return fig

    # Color bars: green if line >=0, red if <0
    if df[line_col].notna().any():
        colors = ["#2ecc71" if v >= 0 else "#e74c3c" for v in df[line_col].fillna(0)]
    else:
        colors = ["#3498db"] * len(df)

    fig = go.Figure()

    # Bar trace (Revenue or any main metric)
    fig.add_trace(
        go.Bar(
            x=df[x_col],
            y=df[bar_col],
            name=bar_col,
            marker_color=colors,
            yaxis="y1",
            hovertemplate=f"{bar_col}: %{{y:,.0f}}<extra></extra>"
        )
    )

    # Line trace (growth %)
    fig.add_trace(
        go.Scatter(
            x=df[x_col],
            y=df[line_col],
            name=line_col,
            mode="lines+markers+text",
            text=[f"{v:.1f}{line_suffix}" if pd.notna(v) else "" for v in df[line_col]],
            textposition="top center",
            line=dict(color="#2980b9", width=2),
            marker=dict(size=7),
            yaxis="y2",
            hovertemplate=f"{line_col}: %{{y:.2f}}{line_suffix}<extra></extra>"
        )
    )

    fig.update_layout(
        title=title,
        template="plotly_white",
        xaxis=dict(
            title=x_col,
            tickangle=-45
        ),
        yaxis=dict(
            title=bar_col,
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)"
        ),
        yaxis2=dict(
            title=line_col,
            overlaying="y",
            side="right",
            showgrid=False
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        margin=dict(l=40, r=40, t=60, b=90),
        bargap=0.2
    )

    return fig

# =========================================================
# MAIN HEADER
# =========================================================
st.markdown("<div class='big-header'>EdTech Financial Intelligence Dashboard</div>", unsafe_allow_html=True)
st.write("Upload revenue data, apply filters, compute EdTech finance metrics, and simulate investor outcomes.")

# =========================================================
# TABS
# =========================================================
tab1, tab2, tab3 = st.tabs(["Overview", "Important Attributes", "Application"])

# =========================================================
# TAB 1 — OVERVIEW
# =========================================================
with tab1:
    st.markdown("<div class='section-title'>Overview</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="card">
    This dashboard converts your fee collection data into financial intelligence:
    revenue trends, operational metrics, CAC, burn, FCF, DCF, and investor returns (ROI, IRR).
    It supports both a fixed 'industry model' and a fully configurable 'custom model'.
    </div>
    """, unsafe_allow_html=True)

    colA, colB = st.columns(2)
    with colA:
        st.markdown("<div class='section-title'>Capabilities</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="card">
        • Monthly / Quarterly / Annual Revenue<br>
        • MoM / QoQ / YoY Growth & CAGR<br>
        • Operational Cost vs OPEX<br>
        • EBITDA, Net Profit, FCF, Burn, Runway<br>
        • CAC, MRR, ARR, conversion metrics<br>
        • 5–20 Year Projection with rising EBITDA%<br>
        • ROI / IRR / DCF Valuation / Exit Value<br>
        </div>
        """, unsafe_allow_html=True)

    with colB:
        st.markdown("<div class='section-title'>Ideal For</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="card">
        • Founders pitching to investors<br>
        • EdTech & Analytics strategy/finance teams<br>
        • People consolidating financials from Google Sheets<br>
        • Anyone who wants formulas + charts + story in one place<br>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='section-title'>KPIs</div>", unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)
    k1.markdown("<div class='kpi'>Revenue & Growth</div>", unsafe_allow_html=True)
    k2.markdown("<div class='kpi'>Margins & EBITDA</div>", unsafe_allow_html=True)
    k3.markdown("<div class='kpi'>Cash, Burn, FCF</div>", unsafe_allow_html=True)
    k4.markdown("<div class='kpi'>Valuation & IRR</div>", unsafe_allow_html=True)

# =========================================================
# TAB 2 — IMPORTANT ATTRIBUTES
# =========================================================
with tab2:
    st.markdown("<div class='section-title'>Required Columns</div>", unsafe_allow_html=True)

    desc_map = {
        "first_payment_date": "Date of first payment (used for monthly/quarterly/yearly slicing).",
        "collected_amount": "Fee actually collected (₹).",
        "total_fee": "Total agreed fee per student (used for MRR proxy).",
        "joined_or_not": "Whether student joined (for completion / enrollment stats).",
        "pay_status": "Payment status.",
        "campaign_name": "Campaign / source (used for CAC drilling later if extended).",
        "lead_created_date": "Lead creation date (for funnel analysis).",
        "batch": "Batch or cohort identifier.",
        "pending_amount": "Pending fee per student.",
        "co_assignee": "Sales / coordinator owner."
    }

    df_gloss = pd.DataFrame(
        [{"Field": k, "Description": v} for k, v in desc_map.items()]
    )
    st.dataframe(df_gloss, width="stretch")

    colA, colB = st.columns(2)
    with colA:
        st.markdown("<div class='section-title'>Financial Metrics (Formulas)</div>", unsafe_allow_html=True)
        for m in [
            "Total Revenue = Σ(revenue)",
            "Operational Cost = revenue × 0.22 (Mode A)",
            "Gross Profit = revenue − Operational Cost",
            "Gross Margin % = Gross Profit / revenue × 100",
            "OPEX = revenue × 0.52 (Mode A)",
            "EBITDA = revenue − Operational Cost − OPEX",
            "EBITDA Margin % = EBITDA / revenue × 100",
            "Net Profit ≈ revenue × EBITDA Margin %",
            "Net Profit Margin % = Net Profit / revenue × 100",
            "FCF ≈ Net Profit − reinvestment (8% of revenue)"
        ]:
            st.markdown(f"<div class='variable-box'>{m}</div>", unsafe_allow_html=True)

    with colB:
        st.markdown("<div class='section-title'>Growth & Funnel Metrics</div>", unsafe_allow_html=True)
        for m in [
            "Revenue Growth Rate % = (Curr − Prev)/Prev × 100",
            "CAGR = ((Ending/Beginning)^(1/years) − 1)",
            "CAC = (Ad + Sales + CRM tools)/New Customers",
            "MRR ≈ Total Fee / 3 (for 3 EMIs)",
            "ARR = MRR × 12",
            "Burn Rate = Monthly loss during scaling",
            "Runway = Cash in Bank / Monthly Burn",
            "Lead Conversion Rate = Converted / Total Leads × 100",
            "Course Completion Rate = Completed / Enrolled × 100",
            "Placement Rate = Placed / Eligible × 100",
            "CSAT = Positive Ratings / Total Ratings × 100"
        ]:
            st.markdown(f"<div class='variable-box'>{m}</div>", unsafe_allow_html=True)

# =========================================================
# TAB 3 — APPLICATION
# =========================================================
with tab3:

    st.markdown("<div class='section-title'>Step 1: Load Dataset</div>", unsafe_allow_html=True)

    df_rev = None
    REQUIRED_COLS = ["first_payment_date", "collected_amount"]

    data_mode = st.radio(
        "Choose Data Source:",
        ["Google Sheet link", "Upload CSV + Mapping"],
        horizontal=True
    )

    # --------------------
    # GOOGLE SHEET MODE
    # --------------------
    if data_mode == "Google Sheet link":
        link = st.text_input("Paste Google Sheet link:")

        if link:
            try:
                sheet_id = link.split("/d/")[1].split("/")[0]
                csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
                df_tmp = pd.read_csv(csv_url)
                df_tmp.columns = (
                    df_tmp.columns
                    .str.strip()
                    .str.lower()
                    .str.replace(" ", "_")
                )
                st.success("Google Sheet loaded successfully.")
                st.dataframe(df_tmp.head(), width="stretch")
                df_rev = df_tmp.copy()
            except Exception as e:
                st.error(f"Failed to fetch Google Sheet: {e}")

    # --------------------
    # CSV UPLOAD + MAPPING
    # --------------------
    else:
        file = st.file_uploader("Upload CSV file", type=["csv"])
        if file:
            raw = pd.read_csv(file)
            raw.columns = (
                raw.columns
                .str.strip()
                .str.lower()
                .str.replace(" ", "_")
            )
            st.write("Preview of uploaded file:")
            st.dataframe(raw.head(), width="stretch")

            st.write("Map uploaded columns to required fields:")
            mapping = {}
            for col in REQUIRED_COLS:
                mapping[col] = st.selectbox(
                    f"Map → {col}",
                    ["-- Select --"] + list(raw.columns),
                    key=f"map_to_{col}"
                )

            if st.button("Apply Mapping"):
                missing = [c for c, v in mapping.items() if v == "-- Select --"]
                if missing:
                    st.error("Please complete all mapping fields.")
                else:
                    inv = {v: k for k, v in mapping.items()}
                    df_rev = raw.rename(columns=inv)
                    st.success("Mapping Applied.")
                    st.dataframe(df_rev.head(), width="stretch")

    # If still no data, stop
    if df_rev is None:
        st.info("Please load a dataset to proceed.")
        st.stop()

    # =========================================================
    # PREPROCESSING
    # =========================================================
    df = df_rev.copy()

    if any(col not in df.columns for col in REQUIRED_COLS):
        st.error("Dataset must contain first_payment_date & collected_amount after mapping.")
        st.stop()

    df["first_payment_date"] = pd.to_datetime(df["first_payment_date"], errors="coerce")
    df = df.dropna(subset=["first_payment_date"])

    df["collected_amount"] = pd.to_numeric(df["collected_amount"], errors="coerce").fillna(0)

    # Optional columns
    if "total_fee" in df.columns:
        df["total_fee"] = pd.to_numeric(df["total_fee"], errors="coerce").fillna(0)

    df["year"] = df["first_payment_date"].dt.year
    df["month"] = df["first_payment_date"].dt.month
    df["month_period"] = df["first_payment_date"].dt.to_period("M").astype(str)
    df["quarter_period"] = df["first_payment_date"].dt.to_period("Q").astype(str)

    # =========================================================
    # STEP 2 — FILTERS
    # =========================================================
    st.markdown("<div class='section-title'>Step 2: Filters</div>", unsafe_allow_html=True)

    all_years = sorted(df["year"].unique())
    if len(all_years) == 1:
        year_range = (int(all_years[0]), int(all_years[0]))
    else:
        year_range = st.slider(
            "Select Year Range:",
            min_value=int(min(all_years)),
            max_value=int(max(all_years)),
            value=(int(min(all_years)), int(max(all_years)))
        )

    df = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]

    st.success(f"Filtered rows: {len(df)}")
    st.dataframe(df.head(), width="stretch")

    # =========================================================
    # STEP 3 — MONTHLY / QUARTERLY / YEARLY + GROWTH
    # =========================================================
    # Monthly
    st.markdown("<div class='section-title'>Monthly Revenue</div>", unsafe_allow_html=True)

    monthly = (
        df.groupby("month_period")["collected_amount"]
        .sum()
        .reset_index()
        .sort_values("month_period")
    )
    monthly.rename(columns={"collected_amount": "Revenue (₹)"}, inplace=True)
    monthly["MoM %"] = monthly["Revenue (₹)"].pct_change() * 100
    monthly["MoM %"].fillna(0, inplace=True)

    st.write("### Table: Monthly Revenue")
    st.dataframe(monthly.style.format({"Revenue (₹)": "{:,.2f}", "MoM %": "{:.2f}"}), width="stretch")

    fig_m = combo_chart_plotly(
        monthly, "month_period", "Revenue (₹)", "MoM %",
        "Monthly Revenue + MoM Growth", "%"
    )
    st.plotly_chart(fig_m, width="stretch")

    # Quarterly
    st.markdown("<div class='section-title'>Quarterly Revenue</div>", unsafe_allow_html=True)

    quarterly = (
        df.groupby("quarter_period")["collected_amount"]
        .sum()
        .reset_index()
        .sort_values("quarter_period")
    )
    quarterly.rename(columns={"collected_amount": "Revenue (₹)"}, inplace=True)
    quarterly["QoQ %"] = quarterly["Revenue (₹)"].pct_change() * 100
    quarterly["QoQ %"].fillna(0, inplace=True)

    st.write("### Table: Quarterly Revenue")
    st.dataframe(quarterly.style.format({"Revenue (₹)": "{:,.2f}", "QoQ %": "{:.2f}"}), width="stretch")

    fig_q = combo_chart_plotly(
        quarterly, "quarter_period", "Revenue (₹)", "QoQ %",
        "Quarterly Revenue + QoQ Growth", "%"
    )
    st.plotly_chart(fig_q, width="stretch")

    # Yearly
    st.markdown("<div class='section-title'>Annual Revenue</div>", unsafe_allow_html=True)

    yearly = (
        df.groupby("year")["collected_amount"]
        .sum()
        .reset_index()
        .sort_values("year")
    )
    yearly.rename(columns={"collected_amount": "Revenue (₹)"}, inplace=True)
    yearly["YoY %"] = yearly["Revenue (₹)"].pct_change() * 100
    yearly["YoY %"].fillna(0, inplace=True)

    # CAGR
    if len(yearly) > 1:
        beginning = yearly["Revenue (₹)"].iloc[0]
        ending = yearly["Revenue (₹)"].iloc[-1]
        n_years = len(yearly) - 1
        if beginning > 0 and n_years > 0:
            cagr = (ending / beginning)**(1 / n_years) - 1
        else:
            cagr = 0.0
    else:
        cagr = 0.0

    st.write("### Table: Annual Revenue")
    st.dataframe(yearly.style.format({"Revenue (₹)": "{:,.2f}", "YoY %": "{:.2f}"}), width="stretch")

    fig_y = combo_chart_plotly(
        yearly, "year", "Revenue (₹)", "YoY %",
        "Yearly Revenue + YoY Growth", "%"
    )
    st.plotly_chart(fig_y, width="stretch")

    # =========================================================
    # STEP 4 — KPI SUMMARY
    # =========================================================
    st.markdown("<div class='section-title'>Key KPIs (from Filtered Data)</div>", unsafe_allow_html=True)

    total_rev = df["collected_amount"].sum()
    avg_yoy = yearly["YoY %"].mean() if len(yearly) > 1 else 0.0
    latest_yoy = yearly["YoY %"].iloc[-1] if len(yearly) > 0 else 0.0

    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(f"<div class='kpi'>Total Revenue<br/>₹{total_rev:,.0f}</div>", unsafe_allow_html=True)
    k2.markdown(f"<div class='kpi'>Latest YoY Growth<br/>{latest_yoy:.2f}%</div>", unsafe_allow_html=True)
    k3.markdown(f"<div class='kpi'>Average YoY Growth<br/>{avg_yoy:.2f}%</div>", unsafe_allow_html=True)
    k4.markdown(f"<div class='kpi'>CAGR<br/>{cagr*100:.2f}%</div>", unsafe_allow_html=True)

    # =========================================================
    # STEP 5 — MODE SELECTOR (A vs B)
    # =========================================================
    st.markdown("<div class='section-title'>Step 3: Metric Engine Mode</div>", unsafe_allow_html=True)

    mode_engine = st.selectbox(
        "Select Calculation Mode:",
        ["Mode A – Industry Standard (Fixed 22% / 52%)", "Mode B – Custom Financial Engine"]
    )

    # =========================================================
    # STEP 6 — METRICS CALCULATION (MODE A or B)
    # =========================================================
    st.markdown("<div class='section-title'>Financial Metrics (Based on Total Revenue)</div>", unsafe_allow_html=True)

    cash_in_bank = st.number_input(
        "Cash in Bank (₹) for Runway calculation",
        min_value=0.0,
        value=500000.0,
        step=50000.0
    )

    if mode_engine.startswith("Mode A"):
        # --------------------------
        # MODE A — INDUSTRY MODEL
        # --------------------------
        st.info("Mode A: Using fixed industry assumptions → Operational Cost = 22%, OPEX = 52%, Reinvestment = 8%.")

        op_cost_pct = 22.0
        opex_pct = 52.0
        reinvest_pct = 8.0

    else:
        # --------------------------
        # MODE B — CUSTOM MODEL
        # --------------------------
        st.info("Mode B: Using your custom percentage inputs for Op Cost, OPEX, and Reinvestment.")
        c1, c2, c3 = st.columns(3)
        with c1:
            op_cost_pct = st.number_input(
                "Operational Cost % (Direct costs)",
                min_value=0.0, max_value=100.0, value=22.0
            )
        with c2:
            opex_pct = st.number_input(
                "Operating Expenses (OPEX) % (Indirect costs)",
                min_value=0.0, max_value=100.0, value=52.0
            )
        with c3:
            reinvest_pct = st.number_input(
                "Reinvestment % (Capex / growth reinvestment)",
                min_value=0.0, max_value=100.0, value=8.0
            )

    # Compute metric block
    if total_rev > 0:
        operational_cost = total_rev * (op_cost_pct / 100)
        opex = total_rev * (opex_pct / 100)

        gross_profit = total_rev - operational_cost
        gross_margin_pct = (gross_profit / total_rev) * 100 if total_rev > 0 else 0

        ebitda = total_rev - operational_cost - opex
        ebitda_margin_pct = (ebitda / total_rev) * 100 if total_rev > 0 else 0

        # As per your table (approx): Net Profit = revenue * EBITDA Margin%
        net_profit = total_rev * (ebitda_margin_pct / 100)
        net_profit_margin_pct = (net_profit / total_rev) * 100 if total_rev > 0 else 0

        # FCF approx = Net Profit − revenue × reinvestment%
        fcf = net_profit - (total_rev * (reinvest_pct / 100))

        # Burn: if EBITDA < 0 → company is burning
        burn_rate = 0.0
        if ebitda < 0:
            burn_rate = abs(ebitda)
        # If using your earlier (0.74−1) logic, we can also show that:
        approx_burn = total_rev * ((op_cost_pct + opex_pct)/100 - 1)

        # Runway
        runway_months = cash_in_bank / burn_rate if burn_rate > 0 else float('inf')

        # CAC inputs
        st.markdown("<div class='section-title'>CAC & Subscription Metrics</div>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            ad_spend = st.number_input("Monthly Ad Spend (₹)", min_value=0.0, value=50000.0, step=10000.0)
        with c2:
            sales_salaries = st.number_input("Sales Team Salaries (₹)", min_value=0.0, value=80000.0, step=10000.0)
        with c3:
            crm_tools_cost = st.number_input("CRM / Tools Cost (₹)", min_value=0.0, value=10000.0, step=5000.0)
        with c4:
            new_customers = st.number_input("New Customers / Month", min_value=1, value=25, step=1)

        cac = (ad_spend + sales_salaries + crm_tools_cost) / new_customers if new_customers > 0 else 0

        # MRR / ARR
        if "total_fee" in df.columns and df["total_fee"].sum() > 0:
            total_program_fee = df["total_fee"].sum()
        else:
            # fallback: assume total_fee ≈ collected_amount for now
            total_program_fee = total_rev

        # Assuming 3 installments (your 30k → 3 × 10k logic) as proxy
        mrr = total_program_fee / 3
        arr = mrr * 12

        metrics_data = {
            "Metric": [
                "Total Revenue",
                "Operational Cost (Direct)",
                "Gross Profit",
                "Gross Margin %",
                "OPEX (Operating Expenses)",
                "EBITDA",
                "EBITDA Margin %",
                "Net Profit (Approx.)",
                "Net Profit Margin %",
                "Free Cash Flow (FCF, approx)",
                "Burn Rate (if EBITDA < 0)",
                "Approx Burn (using (op+opex-100%))",
                "Runway (Months, if burning)",
                "CAC (Cost per new customer)",
                "MRR (3-EMI proxy)",
                "ARR (12 × MRR)"
            ],
            "Value": [
                f"₹{total_rev:,.2f}",
                f"₹{operational_cost:,.2f}",
                f"₹{gross_profit:,.2f}",
                f"{gross_margin_pct:.2f}%",
                f"₹{opex:,.2f}",
                f"₹{ebitda:,.2f}",
                f"{ebitda_margin_pct:.2f}%",
                f"₹{net_profit:,.2f}",
                f"{net_profit_margin_pct:.2f}%",
                f"₹{fcf:,.2f}",
                f"₹{burn_rate:,.2f}",
                f"₹{approx_burn:,.2f}",
                "∞" if runway_months == float('inf') else f"{runway_months:.1f} months",
                f"₹{cac:,.2f}",
                f"₹{mrr:,.2f}",
                f"₹{arr:,.2f}"
            ]
        }
        metrics_df = pd.DataFrame(metrics_data)
        st.dataframe(metrics_df, width="stretch")
    else:
        st.warning("Total Revenue is zero after filters. Metrics cannot be computed.")

    # =========================================================
    # STEP 7 — FUNNEL METRICS INPUTS (Completion, Placement, Leads, CSAT)
    # =========================================================
    st.markdown("<div class='section-title'>Funnel & Outcome Metrics</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        total_enrolled = st.number_input("Total Enrolled Students", min_value=0, value=100)
        completed_students = st.number_input("Students Who Completed", min_value=0, value=80)
    with c2:
        eligible_students = st.number_input("Students Eligible / Looking for Placement", min_value=0, value=70)
        placed_students = st.number_input("Students Placed", min_value=0, value=50)
    with c3:
        total_leads = st.number_input("Total Leads", min_value=0, value=300)
        converted_leads = st.number_input("Converted Leads (Paid)", min_value=0, value=75)

    c4, c5 = st.columns(2)
    with c4:
        positive_ratings = st.number_input("Positive Ratings (4★ / 5★)", min_value=0, value=60)
    with c5:
        total_ratings = st.number_input("Total Ratings Collected", min_value=0, value=80)

    course_completion_rate = (completed_students / total_enrolled * 100) if total_enrolled > 0 else 0
    placement_rate = (placed_students / eligible_students * 100) if eligible_students > 0 else 0
    lead_conversion_rate = (converted_leads / total_leads * 100) if total_leads > 0 else 0
    avg_deal_size = (total_rev / converted_leads) if converted_leads > 0 else 0
    csat = (positive_ratings / total_ratings * 100) if total_ratings > 0 else 0

    funnel_df = pd.DataFrame({
        "Metric": [
            "Course Completion Rate",
            "Placement Rate",
            "Lead Conversion Rate",
            "Average Deal Size",
            "Customer Satisfaction Score (CSAT)"
        ],
        "Value": [
            f"{course_completion_rate:.2f}%",
            f"{placement_rate:.2f}%",
            f"{lead_conversion_rate:.2f}%",
            f"₹{avg_deal_size:,.2f}",
            f"{csat:.2f}%"
        ]
    })
    st.dataframe(funnel_df, width="stretch")

    # =========================================================
    # STEP 8 — INVESTOR PROJECTION (N-YEAR, RISING EBITDA%) + DCF
    # =========================================================
    st.markdown("<div class='section-title'>Investor Projection Model</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        base_rev = st.number_input(
            "Base Revenue for Projection (₹)",
            value=float(total_rev) if total_rev > 0 else 600000.0,
            min_value=0.0,
            step=50000.0
        )

        growth_pct = st.number_input(
            "Expected YoY Revenue Growth (%)",
            min_value=-50.0,
            max_value=300.0,
            value=25.0,
            help="Example: 25 means revenue grows 25% every year."
        )
        growth = growth_pct / 100.0

        ebitda_start_pct_proj = st.number_input(
            "Starting EBITDA Margin (% for Projection)",
            min_value=-50.0,
            max_value=100.0,
            value=26.0,
            help="EBITDA margin in Year 1. Example: 26 means 26%."
        )
        ebitda_start_proj = ebitda_start_pct_proj / 100.0

        ebitda_growth_pct_proj = st.number_input(
            "EBITDA Margin YoY Improvement (%)",
            min_value=-50.0,
            max_value=100.0,
            value=4.0,
            help="Example: 4 means EBITDA margin grows 4% per year (compounded)."
        )
        ebitda_growth_proj = ebitda_growth_pct_proj / 100.0

    with c2:
        projection_years = st.number_input(
            "Number of Projection Years (N)",
            min_value=1,
            max_value=20,
            value=5,
            step=1
        )

        invest = st.number_input(
            "Investor Capital (₹)",
            value=1000000.0,
            min_value=0.0,
            step=100000.0
        )

        equity_pct = st.number_input(
            "Equity Stake (%)",
            min_value=0.0,
            max_value=100.0,
            value=20.0,
            help="Example: 20 means investor holds 20% equity."
        )
        equity = equity_pct / 100.0

        multiple = st.number_input(
            "Exit EBITDA Multiple (×)",
            value=6.0,
            min_value=1.0,
            max_value=30.0,
            step=0.5,
            help="Typical range 5–10× for high-growth EdTech/Analytics."
        )

        discount_rate_pct = st.number_input(
            "Discount Rate for DCF (%)",
            min_value=0.0,
            max_value=50.0,
            value=12.0,
            help="Common range 10–14% in India for this risk profile."
        )
        discount_rate = discount_rate_pct / 100.0

        reinvest_proj_pct = st.number_input(
            "Reinvestment % in Projection (for FCF)",
            min_value=0.0,
            max_value=100.0,
            value=8.0,
            help="Percent of revenue reinvested back each year."
        )
        reinvest_proj = reinvest_proj_pct / 100.0

    if st.button("Run Projection"):
        if base_rev <= 0:
            st.error("Base Revenue should be greater than zero for a meaningful projection.")
        else:
            years_proj = np.arange(1, int(projection_years) + 1)

            rev_list = []
            ebit_list = []
            ebit_margin_list = []
            fcf_list = []

            cur_rev = base_rev
            cur_margin = ebitda_start_proj

            for _ in years_proj:
                rev_list.append(cur_rev)
                ebit = cur_rev * cur_margin
                ebit_list.append(ebit)
                ebit_margin_list.append(cur_margin * 100)

                fcf_t = ebit - (cur_rev * reinvest_proj)
                fcf_list.append(fcf_t)

                cur_rev = cur_rev * (1 + growth)
                cur_margin = cur_margin * (1 + ebitda_growth_proj)

            proj = pd.DataFrame({
                "Year": years_proj,
                "Revenue (₹)": rev_list,
                "EBITDA (₹)": ebit_list,
                "EBITDA %": ebit_margin_list,
                "FCF (₹)": fcf_list
            })

            proj["Valuation (₹)"] = proj["EBITDA (₹)"] * multiple

            # DCF Valuation: discount FCF each year + discounted terminal value
            dcf_value = 0.0
            for i, row in proj.iterrows():
                year_index = int(row["Year"])
                fcf_t = row["FCF (₹)"]
                dcf_value += fcf_t / ((1 + discount_rate) ** year_index)

            terminal_value = proj["Valuation (₹)"].iloc[-1]
            dcf_value += terminal_value / ((1 + discount_rate) ** years_proj[-1])

            st.write("### Projection Table (Revenue, EBITDA, FCF, Valuation)")
            st.dataframe(
                proj.style.format({
                    "Revenue (₹)": "{:,.2f}",
                    "EBITDA (₹)": "{:,.2f}",
                    "EBITDA %": "{:,.2f}",
                    "FCF (₹)": "{:,.2f}",
                    "Valuation (₹)": "{:,.2f}"
                }),
                width="stretch"
            )

            # Projection chart: Revenue vs EBITDA%
            fig_proj = combo_chart_plotly(
                proj,
                x_col="Year",
                bar_col="Revenue (₹)",
                line_col="EBITDA %",
                title="Revenue + EBITDA% Projection (N Years)",
                line_suffix="%"
            )
            st.plotly_chart(fig_proj, width="stretch")

            # =====================================================
            # INVESTOR OUTCOME (TERMINAL VALUE, ROI, IRR, DCF)
            # =====================================================
            investor_payout = terminal_value * equity

            if invest > 0:
                roi = (investor_payout - invest) / invest
                try:
                    cash_flows = [-invest] + [0] * (len(years_proj) - 1) + [investor_payout]
                    irr_value = nf.irr(cash_flows)
                except Exception:
                    irr_value = np.nan
            else:
                roi = 0.0
                irr_value = np.nan

            st.markdown("<div class='section-title'>Investor Outcome</div>", unsafe_allow_html=True)
            k1, k2, k3, k4 = st.columns(4)
            k1.markdown(f"<div class='kpi'>Terminal Value<br/>₹{terminal_value:,.0f}</div>", unsafe_allow_html=True)
            k2.markdown(f"<div class='kpi'>Investor Payout<br/>₹{investor_payout:,.0f}</div>", unsafe_allow_html=True)
            k3.markdown(f"<div class='kpi'>ROI<br/>{roi*100:.2f}%</div>", unsafe_allow_html=True)

            if np.isnan(irr_value):
                irr_text = "N/A"
            else:
                irr_text = f"{irr_value*100:.2f}%"
            k4.markdown(f"<div class='kpi'>IRR<br/>{irr_text}</div>", unsafe_allow_html=True)

            st.markdown(
                f"<div class='kpi'>DCF Valuation<br/>₹{dcf_value:,.0f}</div>",
                unsafe_allow_html=True
            )

            # =====================================================
            # AUTOMATED INSIGHTS (DETAILED, INVESTOR-FRIENDLY)
            # =====================================================
            st.markdown("<div class='section-title'>Automated Insights</div>", unsafe_allow_html=True)

            insights = []

            avg_mom = monthly["MoM %"].mean() if len(monthly) > 1 else 0
            avg_yoy_local = yearly["YoY %"].mean() if len(yearly) > 1 else 0

            # 1) Revenue momentum (MoM)
            if len(monthly) > 3 and avg_mom > 0:
                insights.append(
                    f"Revenue momentum: Your average month-on-month growth is <b>{avg_mom:.1f}%</b>. "
                    f"This means revenue is compounding instead of staying flat. "
                    f"For example, if you are doing around <b>₹{base_rev:,.0f}</b> in Year 1, "
                    f"sustaining similar growth over <b>{int(projection_years)}</b> years can organically push revenue "
                    f"to multiple times the current level without changing the core model."
                )

            # 2) Annual growth vs expectations
            if len(yearly) > 1 and avg_yoy_local > 0:
                if avg_yoy_local >= 20:
                    insights.append(
                        f"Yearly growth: Your average year-on-year growth is <b>{avg_yoy_local:.1f}%</b>, "
                        f"which is strong for an EdTech / Analytics hybrid. For an investor, this signals that the business "
                        f"is not just stable but expanding at a healthy pace, making higher valuation multiples easier to defend."
                    )
                else:
                    insights.append(
                        f"Yearly growth: Your average year-on-year growth is <b>{avg_yoy_local:.1f}%</b>. "
                        f"This is moderate. It can still be attractive if margins and retention are strong, but investors may "
                        f"expect a clearer growth engine to push this closer to the 20–30% range."
                    )

            # 3) EBITDA quality and leverage
            if ebitda_start_pct_proj >= 20:
                insights.append(
                    f"EBITDA quality: You start your projection with an EBITDA margin of <b>{ebitda_start_pct_proj:.1f}%</b>. "
                    f"For an investor with no finance background, this simply means: for every ₹100 of revenue, "
                    f"your model expects about ₹{ebitda_start_pct_proj:.1f} to be left as operating profit before interest and tax."
                )

            if ebitda_growth_pct_proj > 0:
                insights.append(
                    f"Operational leverage: You assume EBITDA margin improves by <b>{ebitda_growth_pct_proj:.1f}%</b> each year. "
                    f"In simple terms, as the company grows, a larger share of revenue turns into profit. "
                    f"This is exactly the pattern investors look for in a scalable business, not one that just grows top-line and burns cash."
                )

            # 4) Revenue growth assumption check
            if growth_pct > 40:
                insights.append(
                    f"Growth assumption check: Revenue growth is modelled at <b>{growth_pct:.1f}%</b> per year. "
                    f"That is aggressive. For a non-finance investor, this roughly means revenue more than doubles every ~2 years. "
                    f"You will need a clear story about acquisition channels, pricing power, and expansion to justify this."
                )
            elif growth_pct > 0:
                insights.append(
                    f"Growth assumption: Revenue growth is set at <b>{growth_pct:.1f}%</b> per year. "
                    f"This is a realistic range for a disciplined EdTech–Analytics hybrid. "
                    f"It tells investors you are aiming for healthy growth without promising unrealistic hockey-stick numbers."
                )

            # 5) ROI & payout interpretation
            if invest > 0 and not np.isnan(irr_value):
                multiple_ret = investor_payout / invest if invest > 0 else 0
                insights.append(
                    f"Return on investment: For an investment of <b>₹{invest:,.0f}</b>, the projected payout at the end of Year "
                    f"<b>{int(projection_years)}</b> is about <b>₹{investor_payout:,.0f}</b>. "
                    f"That is roughly a <b>{multiple_ret:.2f}×</b> return on capital, with an internal rate of return (IRR) of "
                    f"<b>{irr_value*100:.2f}%</b>. "
                    f"In plain language: if someone puts this money in today and your plan works, their money grows by that factor "
                    f"over the projection period."
                )

            # 6) DCF interpretation
            insights.append(
                f"DCF valuation: Using a discount rate of <b>{discount_rate_pct:.1f}%</b>, the discounted cash-flow valuation "
                f"comes to about <b>₹{dcf_value:,.0f}</b>. This represents what the future free cash flows of the business are "
                f"worth in today's money, after accounting for time and risk."
            )

            # 7) Risk / warning cases
            if invest > 0 and roi < 1:
                insights.append(
                    f"Risk flag: The projected ROI is <b>{roi*100:.1f}%</b>, which is less than 100%. "
                    f"That means the investor does not even double their money over the full period. "
                    f"Most early-stage equity investors expect at least 2–3× potential, so this assumption set may feel conservative "
                    f"or unattractive unless there are strong strategic benefits."
                )

            if investor_payout < invest:
                insights.append(
                    f"Capital protection warning: The model currently shows an investor payout of "
                    f"<b>₹{investor_payout:,.0f}</b> against an investment of <b>₹{invest:,.0f}</b>. "
                    f"That means they get back less than what they put in. No financial investor will accept this unless the deal "
                    f"is structured more like debt or has guaranteed minimum returns."
                )

            if not insights:
                insights.append(
                    "The current assumptions look internally consistent. For an investor, this means the model does not show extreme "
                    "risk or unrealistic promises. You should still support this with real pipeline data, historical performance, "
                    "and a clear execution roadmap."
                )

            # Render insights as cards
            for idx, text in enumerate(insights, start=1):
                st.markdown(
                    f"<div class='card'><b>Insight {idx}.</b> {text}</div>",
                    unsafe_allow_html=True
                )
