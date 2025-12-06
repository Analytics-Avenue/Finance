import streamlit as st
import pandas as pd
import numpy as np
import numpy_financial as nf
import plotly.express as px
import plotly.graph_objects as go

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="EdTech Financial Intelligence Dashboard",
    layout="wide"
)

# Hide default sidebar (optional)
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
    """
    df: DataFrame
    x_col: x-axis (category)
    bar_col: bar values (e.g. Revenue)
    line_col: line values (e.g. MoM %, QoQ %, YoY %)
    title: chart title
    line_suffix: "%" for percentages, "" for plain numbers
    """

    if df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No data",
            x=0.5, y=0.5,
            showarrow=False
        )
        fig.update_layout(title=title, template="plotly_white")
        return fig

    # Color bars green if trend positive, red if negative.
    # If line_col is all 0/NaN, default to blue bars.
    if df[line_col].notna().any():
        colors = [
            "#2ecc71" if v >= 0 else "#e74c3c"
            for v in df[line_col].fillna(0)
        ]
    else:
        colors = ["#3498db"] * len(df)

    fig = go.Figure()

    # --- Bar trace (Revenue or main metric) ---
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

    # --- Line trace (Growth %) ---
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
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0
        ),
        margin=dict(l=40, r=40, t=60, b=90),
        bargap=0.2
    )

    return fig

# =========================================================
# MAIN HEADER
# =========================================================
st.markdown("<div class='big-header'>EdTech Financial Intelligence Dashboard</div>", unsafe_allow_html=True)
st.write("Upload your revenue data, track growth, and simulate investor outcomes for your EdTech / Analytics business.")

# =========================================================
# TABS
# =========================================================
tab1, tab2, tab3 = st.tabs(["Overview", "Important Attributes", "Application"])

# =========================================================
# TAB 1 - OVERVIEW
# =========================================================
with tab1:
    st.markdown("<div class='section-title'>Overview</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="card">
    This app connects your student fee collection data to <b>financial insights</b>:
    revenue trends, MoM / QoQ / YoY growth, and a simple N-year investor model with EBITDA, ROI, and IRR.
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='section-title'>What You Can Do</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="card">
        • Load data from Google Sheets or CSV<br>
        • See monthly, quarterly, annual revenue splits<br>
        • Calculate MoM, QoQ, YoY growth %<br>
        • Run an N-year projection (Revenue + EBITDA)<br>
        • Calculate Terminal Value, ROI, IRR<br>
        • Compare against static EdTech assumptions
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='section-title'>Who It's For</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="card">
        • Founders and finance leads in EdTech<br>
        • Strategy & growth teams<br>
        • Anyone prepping for investor meetings<br>
        • People tired of 17 Excel sheets and no story
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Key KPIs</div>", unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)
    k1.markdown("<div class='kpi'>Revenue</div>", unsafe_allow_html=True)
    k2.markdown("<div class='kpi'>Growth %</div>", unsafe_allow_html=True)
    k3.markdown("<div class='kpi'>EBITDA</div>", unsafe_allow_html=True)
    k4.markdown("<div class='kpi'>IRR</div>", unsafe_allow_html=True)

# =========================================================
# TAB 2 - IMPORTANT ATTRIBUTES
# =========================================================
with tab2:
    st.markdown("<div class='section-title'>Required Columns in Dataset</div>", unsafe_allow_html=True)

    desc_map = {
        "first_payment_date": "First payment date from student (used for time-based grouping).",
        "collected_amount": "Amount actually collected from the student (₹).",
        "total_fee": "Total fee agreed for that student/batch.",
        "joined_or_not": "Whether the student actually joined (Yes/No or 1/0).",
        "pay_status": "Payment status (Paid / Partially Paid / Pending).",
        "campaign_name": "Campaign/source attribution for marketing & CAC analysis.",
        "lead_created_date": "Date when lead was created.",
        "batch": "Batch ID/name to identify cohorts.",
        "pending_amount": "Fee still pending from that student (₹).",
        "co_assignee": "Sales/coordinator responsible (for performance splits)."
    }

    df_gloss = pd.DataFrame(
        [{"Field": k, "Description": v} for k, v in desc_map.items()]
    )
    st.dataframe(df_gloss, width="stretch")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='section-title'>Core Financial Metrics</div>", unsafe_allow_html=True)
        for m in [
            "Total Revenue",
            "Gross Profit & Gross Margin",
            "EBITDA & EBITDA Margin",
            "Net Profit & Net Margin",
            "MRR / ARR",
            "Free Cash Flow"
        ]:
            st.markdown(f"<div class='variable-box'>{m}</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='section-title'>Investor & Growth Metrics</div>", unsafe_allow_html=True)
        for m in [
            "MoM / QoQ / YoY Growth",
            "CAGR (long-term growth)",
            "ROI (Return on Investment)",
            "IRR (Internal Rate of Return)",
            "Terminal Value (EBITDA × Multiple)"
        ]:
            st.markdown(f"<div class='variable-box'>{m}</div>", unsafe_allow_html=True)

# =========================================================
# TAB 3 - APPLICATION
# =========================================================
with tab3:

    st.markdown("<div class='section-title'>Step 1: Load Dataset</div>", unsafe_allow_html=True)

    df_rev = None
    REQUIRED_COLS = ["first_payment_date", "collected_amount"]

    mode = st.radio(
        "Choose data source:",
        ["Google Sheet link", "Upload CSV + Mapping"],
        horizontal=True
    )

    # -----------------------------
    # MODE 1: GOOGLE SHEET LINK
    # -----------------------------
    if mode == "Google Sheet link":
        link = st.text_input("Paste Google Sheet link:")

        if link:
            try:
                sheet_id = link.split("/d/")[1].split("/")[0]
                csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
                df_tmp = pd.read_csv(csv_url)
                df_tmp.columns = df_tmp.columns.str.strip().str.lower().str.replace(" ", "_")

                st.success("Google Sheet loaded.")
                st.dataframe(df_tmp.head(), width="stretch")
                df_rev = df_tmp.copy()

            except Exception as e:
                st.error(f"Failed to load: {e}")

    # -----------------------------
    # MODE 2: UPLOAD CSV + MAPPING
    # -----------------------------
    else:
        file = st.file_uploader("Upload CSV file", type=["csv"])

        if file:
            raw = pd.read_csv(file)
            raw.columns = raw.columns.str.strip().str.lower().str.replace(" ", "_")

            st.write("Preview of uploaded file:")
            st.dataframe(raw.head(), width="stretch")

            st.write("Map your columns to the required fields:")
            mapping = {}
            for col in REQUIRED_COLS:
                mapping[col] = st.selectbox(
                    f"Map to → {col}",
                    ["-- Select --"] + list(raw.columns),
                    key=f"map_{col}"
                )

            if st.button("Apply Mapping"):
                missing = [c for c, v in mapping.items() if v == "-- Select --"]
                if missing:
                    st.error("Please map all required fields before proceeding.")
                else:
                    inv = {v: k for k, v in mapping.items()}
                    mapped = raw.rename(columns=inv)
                    df_rev = mapped.copy()
                    st.success("Mapping applied.")
                    st.dataframe(df_rev.head(), width="stretch")

    # -----------------------------
    # BLOCK IF NO DATA
    # -----------------------------
    if df_rev is None:
        st.info("Load data first to see analytics.")
        st.stop()

    # =========================================================
    # PREPROCESS
    # =========================================================
    df = df_rev.copy()

    if "first_payment_date" not in df.columns or "collected_amount" not in df.columns:
        st.error("Dataset must contain 'first_payment_date' and 'collected_amount' columns (after mapping).")
        st.stop()

    df["first_payment_date"] = pd.to_datetime(df["first_payment_date"], errors="coerce")
    df = df.dropna(subset=["first_payment_date"])
    df["collected_amount"] = pd.to_numeric(df["collected_amount"], errors="coerce").fillna(0)

    df["year"] = df["first_payment_date"].dt.year
    df["month_period"] = df["first_payment_date"].dt.to_period("M").astype(str)
    df["quarter_period"] = df["first_payment_date"].dt.to_period("Q").astype(str)

    st.markdown("<div class='section-title'>Step 2: Data Snapshot</div>", unsafe_allow_html=True)
    st.dataframe(df.head(), width="stretch")

    # =========================================================
    # GLOBAL FILTERS (Month / Quarter / Year)
    # =========================================================
    st.markdown("<div class='section-title'>Filters</div>", unsafe_allow_html=True)

    df["month_num"] = df["first_payment_date"].dt.month
    df["quarter_num"] = df["first_payment_date"].dt.quarter
    df["year_num"] = df["first_payment_date"].dt.year

    min_month, max_month = int(df["month_num"].min()), int(df["month_num"].max())
    min_q, max_q = int(df["quarter_num"].min()), int(df["quarter_num"].max())
    min_y, max_y = int(df["year_num"].min()), int(df["year_num"].max())

    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        month_range = st.slider("Month range", min_month, max_month, (min_month, max_month))
    with col_f2:
        quarter_range = st.slider("Quarter range", min_q, max_q, (min_q, max_q))
    with col_f3:
        year_range = st.slider("Year range", min_y, max_y, (min_y, max_y))

    df = df[
        (df["month_num"].between(month_range[0], month_range[1])) &
        (df["quarter_num"].between(quarter_range[0], quarter_range[1])) &
        (df["year_num"].between(year_range[0], year_range[1]))
    ]

    # If filters removed everything
    if df.empty:
        st.warning("No data available for the selected filter range.")
        st.stop()

    # Recompute period columns after filtering (just to be safe)
    df["year"] = df["first_payment_date"].dt.year
    df["month_period"] = df["first_payment_date"].dt.to_period("M").astype(str)
    df["quarter_period"] = df["first_payment_date"].dt.to_period("Q").astype(str)

    # =========================================================
    # MONTHLY REVENUE + MoM
    # =========================================================
    st.markdown("<div class='section-title'>Monthly Revenue</div>", unsafe_allow_html=True)

    monthly = df.groupby("month_period")["collected_amount"].sum().reset_index()
    monthly.rename(columns={"collected_amount": "Revenue (₹)"}, inplace=True)

    st.write("### Table View")
    st.dataframe(monthly.style.format({"Revenue (₹)": "{:,.2f}"}), width="stretch")

    monthly["MoM %"] = monthly["Revenue (₹)"].pct_change() * 100
    monthly["MoM %"] = monthly["MoM %"].fillna(0)

    fig_m = combo_chart_plotly(
        monthly,
        x_col="month_period",
        bar_col="Revenue (₹)",
        line_col="MoM %",
        title="Monthly Revenue + MoM Growth",
        line_suffix="%"
    )
    st.plotly_chart(fig_m, width="stretch")

    # =========================================================
    # QUARTERLY REVENUE + QoQ
    # =========================================================
    st.markdown("<div class='section-title'>Quarterly Revenue</div>", unsafe_allow_html=True)

    quarterly = df.groupby("quarter_period")["collected_amount"].sum().reset_index()
    quarterly.rename(columns={"collected_amount": "Revenue (₹)"}, inplace=True)

    st.write("### Table View")
    st.dataframe(quarterly.style.format({"Revenue (₹)": "{:,.2f}"}), width="stretch")

    quarterly["QoQ %"] = quarterly["Revenue (₹)"].pct_change() * 100
    quarterly["QoQ %"] = quarterly["QoQ %"].fillna(0)

    fig_q = combo_chart_plotly(
        quarterly,
        x_col="quarter_period",
        bar_col="Revenue (₹)",
        line_col="QoQ %",
        title="Quarterly Revenue + QoQ Growth",
        line_suffix="%"
    )
    st.plotly_chart(fig_q, width="stretch")

    # =========================================================
    # ANNUAL REVENUE + YoY
    # =========================================================
    st.markdown("<div class='section-title'>Annual Revenue</div>", unsafe_allow_html=True)

    yearly = df.groupby("year")["collected_amount"].sum().reset_index()
    yearly.rename(columns={"collected_amount": "Revenue (₹)"}, inplace=True)

    st.write("### Table View")
    st.dataframe(yearly.style.format({"Revenue (₹)": "{:,.2f}"}), width="stretch")

    yearly["YoY %"] = yearly["Revenue (₹)"].pct_change() * 100
    yearly["YoY %"] = yearly["YoY %"].fillna(0)

    fig_y = combo_chart_plotly(
        yearly,
        x_col="year",
        bar_col="Revenue (₹)",
        line_col="YoY %",
        title="Annual Revenue + YoY Growth",
        line_suffix="%"
    )
    st.plotly_chart(fig_y, width="stretch")

    # =========================================================
    # CORE KPIs
    # =========================================================
    st.markdown("<div class='section-title'>Key Performance Indicators</div>", unsafe_allow_html=True)

    total_rev = df["collected_amount"].sum()
    avg_yoy = yearly["YoY %"].mean() if len(yearly) > 1 else 0.0

    k1, k2, k3 = st.columns(3)
    k1.markdown(f"<div class='kpi'>Total Revenue<br/>₹{total_rev:,.0f}</div>", unsafe_allow_html=True)
    k2.markdown(f"<div class='kpi'>Avg YoY Growth<br/>{avg_yoy:.2f}%</div>", unsafe_allow_html=True)
    k3.markdown(f"<div class='kpi'>Months of Data<br/>{len(monthly)}</div>", unsafe_allow_html=True)

    # =========================================================
    # INVESTOR PROJECTION (N-YEAR) + COMBO CHART
    # =========================================================
    st.markdown("<div class='section-title'>Investor Model</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        base_rev = st.number_input(
            "Base Revenue for Projection (₹)",
            value=float(total_rev),
            min_value=0.0,
            step=50000.0
        )
        growth_pct = st.number_input(
            "Expected YoY Growth (%)",
            min_value=-50.0,
            max_value=200.0,
            value=25.0
        )
        growth = growth_pct / 100.0

        ebitda_pct = st.number_input(
            "EBITDA Margin (%)",
            min_value=0.0,
            max_value=100.0,
            value=26.0
        )
        ebitda_margin = ebitda_pct / 100.0

        projection_years = st.number_input(
            "Number of Projection Years (N)",
            min_value=1,
            max_value=20,
            value=5,
            step=1
        )

    with c2:
        invest = st.number_input(
            "Investment (₹)",
            value=1000000.0,
            step=100000.0,
            min_value=0.0
        )
        equity_pct = st.number_input(
            "Equity Stake (%)",
            min_value=0.0,
            max_value=100.0,
            value=20.0
        )
        equity = equity_pct / 100.0

        multiple = st.number_input(
            "Exit EBITDA Multiple (X)",
            value=6.0,
            min_value=1.0,
            max_value=30.0,
            step=0.5
        )

    if st.button("Run Projection"):

        years_proj = np.arange(1, int(projection_years) + 1)
        rev_list = []
        ebit_list = []
        cur = base_rev

        for _ in years_proj:
            rev_list.append(cur)
            ebit_list.append(cur * ebitda_margin)
            cur = cur * (1 + growth)

        proj = pd.DataFrame({
            "Year": years_proj,
            "Revenue (₹)": rev_list,
            "EBITDA (₹)": ebit_list
        })
        proj["Valuation (₹)"] = proj["EBITDA (₹)"] * multiple

        st.write("### Projection Table")
        st.dataframe(proj.style.format("{:,.2f}"), width="stretch")

        # Build chart using EBITDA% as line
        proj_for_chart = proj.copy()
        proj_for_chart["EBITDA %"] = np.where(
            proj_for_chart["Revenue (₹)"] > 0,
            (proj_for_chart["EBITDA (₹)"] / proj_for_chart["Revenue (₹)"]) * 100,
            0
        )

        fig_proj = combo_chart_plotly(
            proj_for_chart,
            x_col="Year",
            bar_col="Revenue (₹)",
            line_col="EBITDA %",
            title="Revenue + EBITDA% Projection",
            line_suffix="%"
        )
        st.plotly_chart(fig_proj, width="stretch")

        terminal = proj["Valuation (₹)"].iloc[-1]
        payout = terminal * equity
        roi = (payout - invest) / invest if invest > 0 else 0
        try:
            irr = nf.irr([-invest] + [0] * (len(years_proj) - 1) + [payout]) if invest > 0 else 0
        except Exception:
            irr = 0

        st.markdown("<div class='section-title'>Investor Outcome</div>", unsafe_allow_html=True)
        k1, k2, k3, k4 = st.columns(4)
        k1.markdown(f"<div class='kpi'>Terminal Value<br/>₹{terminal:,.0f}</div>", unsafe_allow_html=True)
        k2.markdown(f"<div class='kpi'>Payout<br/>₹{payout:,.0f}</div>", unsafe_allow_html=True)
        k3.markdown(f"<div class='kpi'>ROI<br/>{roi*100:.2f}%</div>", unsafe_allow_html=True)
        k4.markdown(f"<div class='kpi'>IRR<br/>{irr*100:.2f}%</div>", unsafe_allow_html=True)

        # =====================================================
        # AUTOMATED INSIGHTS
        # =====================================================
        st.markdown("<div class='section-title'>Automated Insights</div>", unsafe_allow_html=True)

        insights = []

        if len(monthly) > 3 and monthly["MoM %"].mean() > 5:
            insights.append("Your average MoM growth suggests healthy short-term revenue momentum.")

        if len(yearly) > 1 and yearly["YoY %"].mean() > 20:
            insights.append("Your YoY growth is strong compared to typical EdTech benchmarks (>20%).")

        if ebitda_margin >= 0.25:
            insights.append("EBITDA margin ≥ 25% indicates a lean, high-margin operating model.")

        if growth > 0.35:
            insights.append("YoY growth assumption > 35% is very aggressive. Validate with pipeline + capacity.")

        if terminal < base_rev * 2:
            insights.append("Terminal value is not very aggressive vs Year-1 revenue. You may be under-selling upside.")

        if invest > 0 and roi < 1:
            insights.append("ROI < 100% suggests the equity + multiple combination may not be attractive enough for investors.")

        if not insights:
            insights.append("No major red flags. Your assumptions look moderate and defensible for a seed/early-stage pitch.")

        for i in insights:
            st.markdown(f"<div class='card'>{i}</div>", unsafe_allow_html=True)
