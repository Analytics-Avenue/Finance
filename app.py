import streamlit as st
import pandas as pd
import numpy as np
import numpy_financial as nf
import matplotlib.pyplot as plt
import plotly.express as px

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(page_title="EdTech Financial Intelligence Dashboard", layout="wide")

# Hide default Streamlit sidebar nav (optional)
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

/* Variable box */
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
# COMBO CHART HELPER
# =========================================================
def combo_chart(df, x_col, bar_col, line_col, title,
                ylabel_bar="Value", ylabel_line="Percent"):
    fig, ax1 = plt.subplots(figsize=(11, 5))

    # Bar (left axis)
    ax1.bar(
        df[x_col],
        df[bar_col],
        color="#064b86",
        alpha=0.75,
        label=bar_col
    )
    ax1.set_xlabel(x_col)
    ax1.set_ylabel(ylabel_bar, color="#064b86")
    ax1.tick_params(axis='y', labelcolor="#064b86")
    ax1.grid(axis='y', alpha=0.25)

    # Line (right axis)
    ax2 = ax1.twinx()
    ax2.plot(
        df[x_col],
        df[line_col],
        color="red",
        linewidth=2.5,
        marker="o",
        label=line_col
    )
    ax2.set_ylabel(ylabel_line, color="red")
    ax2.tick_params(axis='y', labelcolor="red")

    plt.title(title)
    plt.xticks(rotation=45, ha="right")

    return fig


# =========================================================
# MAIN HEADER
# =========================================================
st.markdown("<div class='big-header'>EdTech Financial Intelligence Dashboard</div>", unsafe_allow_html=True)
st.write("Track revenue, growth, and investor outcomes for your EdTech / Analytics business.")

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
    This app helps you connect your student fee collection data to **financial insights**:
    revenue trends, MoM / QoQ / YoY growth, 5-year projections, and simple investor valuation.
    Use it to back your pitch decks, internal reviews, or to just see if the business isn't on fire.
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='section-title'>What You Can Do Here</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="card">
        • Upload revenue data from Google Sheets or CSV<br>
        • See monthly, quarterly, annual revenue splits<br>
        • Measure MoM, QoQ, YoY growth trends<br>
        • Run a 5-year investor model (revenue + EBITDA)<br>
        • Check basic investor outcomes: Terminal value, ROI, IRR<br>
        • Compare your assumptions vs static EdTech benchmarks
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='section-title'>Who Is This For</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="card">
        • Founders & co-founders in EdTech / Analytics<br>
        • Finance / strategy / growth teams<br>
        • Anyone building an investor deck with actual numbers<br>
        • People who are tired of badly formatted Excel sheets
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
        "total_fee": "Total fee agreed for that student/batch (optional for deal-size metrics).",
        "joined_or_not": "Whether the student actually joined (Yes/No or 1/0).",
        "pay_status": "Payment status (Paid / Partially Paid / Pending).",
        "campaign_name": "Campaign/source attribution for marketing & CAC analysis.",
        "lead_created_date": "Date when lead was created.",
        "batch": "Batch ID/name to identify cohorts.",
        "pending_amount": "Fee still pending from that student (₹).",
        "co_assignee": "Sales / coordinator responsible (for performance split)."
    }

    df_gloss = pd.DataFrame(
        [{"Field": k, "Description": v} for k, v in desc_map.items()]
    )
    st.dataframe(df_gloss, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='section-title'>Core Financial Metrics</div>", unsafe_allow_html=True)
        for m in [
            "Total Revenue",
            "Gross Profit & Gross Margin",
            "EBITDA & EBITDA Margin",
            "Net Profit & Net Margin",
            "MRR / ARR",
            "Free Cash Flow",
        ]:
            st.markdown(f"<div class='variable-box'>{m}</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='section-title'>Investor & Growth Metrics</div>", unsafe_allow_html=True)
        for m in [
            "MoM / QoQ / YoY Growth",
            "CAGR (Long-term growth)",
            "ROI (Return on Investment)",
            "IRR (Internal Rate of Return)",
            "Terminal Value (EBITDA × multiple)",
        ]:
            st.markdown(f"<div class='variable-box'>{m}</div>", unsafe_allow_html=True)

# =========================================================
# TAB 3 - APPLICATION (main logic)
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
                st.dataframe(df_tmp.head(), use_container_width=True)
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
            st.dataframe(raw.head(), use_container_width=True)

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
                    st.dataframe(df_rev.head(), use_container_width=True)

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
    st.dataframe(df.head(), use_container_width=True)

    # =========================================================
    # MONTHLY REVENUE + MoM
    # =========================================================
    st.markdown("<div class='section-title'>Monthly Revenue</div>", unsafe_allow_html=True)

    monthly = df.groupby("month_period")["collected_amount"].sum().reset_index()
    monthly.rename(columns={"collected_amount": "Revenue (₹)"}, inplace=True)

    st.write("### Monthly Revenue (Table)")
    st.dataframe(monthly.style.format({"Revenue (₹)": "{:,.2f}"}), use_container_width=True)

    monthly["MoM %"] = monthly["Revenue (₹)"].pct_change() * 100
    monthly["MoM %"] = monthly["MoM %"].fillna(0)

    fig_m = combo_chart(
        monthly,
        x_col="month_period",
        bar_col="Revenue (₹)",
        line_col="MoM %",
        title="Monthly Revenue + MoM Growth",
        ylabel_bar="Revenue (₹)",
        ylabel_line="MoM %"
    )
    st.pyplot(fig_m)

    # =========================================================
    # QUARTERLY REVENUE + QoQ
    # =========================================================
    st.markdown("<div class='section-title'>Quarterly Revenue</div>", unsafe_allow_html=True)

    quarterly = df.groupby("quarter_period")["collected_amount"].sum().reset_index()
    quarterly.rename(columns={"collected_amount": "Revenue (₹)"}, inplace=True)

    st.write("### Quarterly Revenue (Table)")
    st.dataframe(quarterly.style.format({"Revenue (₹)": "{:,.2f}"}), use_container_width=True)

    quarterly["QoQ %"] = quarterly["Revenue (₹)"].pct_change() * 100
    quarterly["QoQ %"] = quarterly["QoQ %"].fillna(0)

    fig_q = combo_chart(
        quarterly,
        x_col="quarter_period",
        bar_col="Revenue (₹)",
        line_col="QoQ %",
        title="Quarterly Revenue + QoQ Growth",
        ylabel_bar="Revenue (₹)",
        ylabel_line="QoQ %"
    )
    st.pyplot(fig_q)

    # =========================================================
    # ANNUAL REVENUE + YoY
    # =========================================================
    st.markdown("<div class='section-title'>Annual Revenue</div>", unsafe_allow_html=True)

    yearly = df.groupby("year")["collected_amount"].sum().reset_index()
    yearly.rename(columns={"collected_amount": "Revenue (₹)"}, inplace=True)

    st.write("### Annual Revenue (Table)")
    st.dataframe(yearly.style.format({"Revenue (₹)": "{:,.2f}"}), use_container_width=True)

    yearly["YoY %"] = yearly["Revenue (₹)"].pct_change() * 100
    yearly["YoY %"] = yearly["YoY %"].fillna(0)

    fig_y = combo_chart(
        yearly,
        x_col="year",
        bar_col="Revenue (₹)",
        line_col="YoY %",
        title="Annual Revenue + YoY Growth",
        ylabel_bar="Revenue (₹)",
        ylabel_line="YoY %"
    )
    st.pyplot(fig_y)

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
    # INVESTOR PROJECTION (5-YEAR) + COMBO CHART
    # =========================================================
    st.markdown("<div class='section-title'>Investor Model</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        base_rev = st.number_input("Base Revenue (₹)", value=float(total_rev), step=100000.0)
        growth = st.number_input("YoY Growth (0.25 = 25%)", value=0.25, min_value=0.0, max_value=1.0)
        ebitda_margin = st.number_input("EBITDA Margin (0.26 = 26%)", value=0.26, min_value=0.0, max_value=1.0)

    with c2:
        invest = st.number_input("Investment (₹)", value=1000000.0, step=100000.0)
        equity = st.number_input("Equity % (0.20 = 20%)", value=0.20, min_value=0.0, max_value=1.0)
        multiple = st.number_input("Exit Multiple (X)", value=6.0, min_value=1.0, max_value=20.0)

    if st.button("Run Projection"):

        years_proj = np.arange(1, 6)
        rev_list = []
        ebit_list = []
        cur = base_rev

        for _ in years_proj:
            rev_list.append(cur)
            ebit_list.append(cur * ebitda_margin)
            cur *= (1 + growth)

        proj = pd.DataFrame({
            "Year": years_proj,
            "Revenue (₹)": rev_list,
            "EBITDA (₹)": ebit_list
        })
        proj["Valuation (₹)"] = proj["EBITDA (₹)"] * multiple

        st.write("### 5-Year Projection (Table)")
        st.dataframe(proj.style.format("{:,.2f}"), use_container_width=True)

        fig_proj = combo_chart(
            proj,
            x_col="Year",
            bar_col="Revenue (₹)",
            line_col="EBITDA (₹)",
            title="Revenue + EBITDA Projection (5 Years)",
            ylabel_bar="Revenue (₹)",
            ylabel_line="EBITDA (₹)"
        )
        st.pyplot(fig_proj)

        terminal = proj["Valuation (₹)"].iloc[-1]
        payout = terminal * equity
        roi = (payout - invest) / invest if invest > 0 else 0
        irr = nf.irr([-invest, 0, 0, 0, payout]) if invest > 0 else 0

        st.markdown("<div class='section-title'>Investor Outcome</div>", unsafe_allow_html=True)
        k1, k2, k3, k4 = st.columns(4)
        k1.markdown(f"<div class='kpi'>Terminal Value<br/>₹{terminal:,.0f}</div>", unsafe_allow_html=True)
        k2.markdown(f"<div class='kpi'>Payout<br/>₹{payout:,.0f}</div>", unsafe_allow_html=True)
        k3.markdown(f"<div class='kpi'>ROI<br/>{roi*100:.2f}%</div>", unsafe_allow_html=True)
        k4.markdown(f"<div class='kpi'>IRR<br/>{irr*100:.2f}%</div>", unsafe_allow_html=True)

        # =====================================================
        # STATIC COMPETITOR COMPARISON
        # =====================================================
        st.markdown("<div class='section-title'>Competitor Comparison (Static Benchmarks)</div>", unsafe_allow_html=True)

        competitors = pd.DataFrame({
            "Company": ["Your Org", "Scaler", "UpGrad", "Simplilearn", "Great Learning"],
            "Revenue_Cr": [
                base_rev / 1e7,  # convert to Cr approx
                400, 1200, 600, 800
            ],
            "EBITDA_Margin": [
                ebitda_margin,
                0.14, 0.09, 0.11, 0.12
            ],
            "YoY_Growth": [
                growth,
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

        fig_comp = px.bar(
            competitors,
            x="Company",
            y="Revenue_Cr",
            title="Revenue Benchmark (₹ Cr)",
            text="Revenue_Cr"
        )
        fig_comp.update_traces(texttemplate="%{text:.1f}", textposition="outside")
        fig_comp.update_layout(yaxis_title="Revenue (₹ Cr)")
        st.plotly_chart(fig_comp, use_container_width=True)

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
            insights.append("EBITDA margin ≥ 25% indicates a lean cost structure and strong unit economics.")

        if growth > competitors["YoY_Growth"].median():
            insights.append("Your assumed growth rate is higher than key competitors, positioning you as a high-growth player.")

        if terminal < base_rev * 2:
            insights.append("Terminal value isn't very aggressive vs Year 1 revenue. Consider revisiting growth or multiples with investors.")

        if not insights:
            insights.append("No extreme risks or standout strengths detected. Your assumption set looks moderate and defensible.")

        for i in insights:
            st.markdown(f"<div class='card'>{i}</div>", unsafe_allow_html=True)
