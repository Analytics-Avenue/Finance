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
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No data", x=0.5, y=0.5, showarrow=False)
        fig.update_layout(title=title, template="plotly_white")
        return fig

    if df[line_col].notna().any():
        colors = ["#2ecc71" if v >= 0 else "#e74c3c" for v in df[line_col].fillna(0)]
    else:
        colors = ["#3498db"] * len(df)

    fig = go.Figure()

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
st.write("Upload revenue data, apply filters, track growth trends, and generate investor projections.")

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
    This dashboard converts your fee collection data into insights:
    revenue trends, growth KPIs, and long-term investor valuation.
    </div>
    """, unsafe_allow_html=True)

    colA, colB = st.columns(2)
    with colA:
        st.markdown("<div class='section-title'>Capabilities</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="card">
        • Monthly / Quarterly / Annual Revenue<br>
        • MoM / QoQ / YoY Growth<br>
        • CAGR Calculation<br>
        • 5–15 Year Projection<br>
        • Rising EBITDA Margin Model<br>
        • IRR / ROI / Terminal Value<br>
        </div>
        """, unsafe_allow_html=True)

    with colB:
        st.markdown("<div class='section-title'>Ideal For</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="card">
        • Founders preparing investor decks<br>
        • EdTech & Analytics finance teams<br>
        • Strategy & growth roles<br>
        • Anyone sick of Excel chaos<br>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Key KPIs</div>", unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)
    k1.markdown("<div class='kpi'>Revenue</div>", unsafe_allow_html=True)
    k2.markdown("<div class='kpi'>Growth %</div>", unsafe_allow_html=True)
    k3.markdown("<div class='kpi'>EBITDA</div>", unsafe_allow_html=True)
    k4.markdown("<div class='kpi'>IRR</div>", unsafe_allow_html=True)

# =========================================================
# TAB 2 — IMPORTANT ATTRIBUTES
# =========================================================
with tab2:
    st.markdown("<div class='section-title'>Required Columns</div>", unsafe_allow_html=True)

    desc_map = {
        "first_payment_date": "Date of first payment.",
        "collected_amount": "Total fee collected (₹).",
        "total_fee": "Full fee.",
        "joined_or_not": "Whether student joined.",
        "pay_status": "Payment status.",
        "campaign_name": "Marketing source.",
        "lead_created_date": "Lead creation date.",
        "batch": "Batch identification.",
        "pending_amount": "Remaining unpaid fee.",
        "co_assignee": "Sales/coordinator owner."
    }

    df_gloss = pd.DataFrame([{"Field": k, "Description": v} for k, v in desc_map.items()])
    st.dataframe(df_gloss, width="stretch")

    colA, colB = st.columns(2)
    with colA:
        st.markdown("<div class='section-title'>Financial Metrics</div>", unsafe_allow_html=True)
        for m in ["Gross Profit", "EBITDA", "Net Profit", "MRR", "ARR", "FCF"]:
            st.markdown(f"<div class='variable-box'>{m}</div>", unsafe_allow_html=True)

    with colB:
        st.markdown("<div class='section-title'>Growth Metrics</div>", unsafe_allow_html=True)
        for m in ["MoM", "QoQ", "YoY", "ROI", "IRR", "Terminal Value"]:
            st.markdown(f"<div class='variable-box'>{m}</div>", unsafe_allow_html=True)

# =========================================================
# TAB 3 — APPLICATION
# =========================================================
with tab3:

    st.markdown("<div class='section-title'>Step 1: Load Dataset</div>", unsafe_allow_html=True)

    df_rev = None
    REQUIRED_COLS = ["first_payment_date", "collected_amount"]

    mode = st.radio(
        "Choose Data Source:",
        ["Google Sheet link", "Upload CSV + Mapping"],
        horizontal=True
    )

    # =========================================================
    # MODE 1: GOOGLE SHEET LINK
    # =========================================================
    if mode == "Google Sheet link":
        link = st.text_input("Paste Google Sheet link:")

        if link:
            try:
                sheet_id = link.split("/d/")[1].split("/")[0]
                csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

                df_tmp = pd.read_csv(csv_url)
                df_tmp.columns = (
                    df_tmp.columns.str.strip()
                    .str.lower()
                    .str.replace(" ", "_")
                )

                st.success("Google Sheet loaded successfully.")
                st.dataframe(df_tmp.head(), width="stretch")
                df_rev = df_tmp.copy()

            except Exception as e:
                st.error(f"Failed to fetch Google Sheet: {e}")

    # =========================================================
    # MODE 2: CSV UPLOAD + COLUMN MAPPING
    # =========================================================
    else:
        file = st.file_uploader("Upload CSV", type=["csv"])

        if file:
            raw = pd.read_csv(file)
            raw.columns = (
                raw.columns.str.strip()
                .str.lower()
                .str.replace(" ", "_")
            )

            st.write("Preview:")
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

    # Stop if no data
    if df_rev is None:
        st.info("Please load a dataset to proceed.")
        st.stop()

    # =========================================================
    # PREPROCESSING
    # =========================================================
    df = df_rev.copy()

    if any(col not in df.columns for col in REQUIRED_COLS):
        st.error("Dataset must contain first_payment_date & collected_amount.")
        st.stop()

    df["first_payment_date"] = pd.to_datetime(df["first_payment_date"], errors="coerce")
    df = df.dropna(subset=["first_payment_date"])

    df["collected_amount"] = pd.to_numeric(df["collected_amount"], errors="coerce").fillna(0)

    df["year"] = df["first_payment_date"].dt.year
    df["month"] = df["first_payment_date"].dt.month
    df["month_period"] = df["first_payment_date"].dt.to_period("M").astype(str)
    df["quarter_period"] = df["first_payment_date"].dt.to_period("Q").astype(str)

    # =========================================================
    # STEP 2 — FILTERS
    # =========================================================
    st.markdown("<div class='section-title'>Step 2: Filters</div>", unsafe_allow_html=True)

    all_years = sorted(df["year"].unique())
    selected_years = st.slider(
        "Select Year Range:",
        min_value=int(min(all_years)),
        max_value=int(max(all_years)),
        value=(int(min(all_years)), int(max(all_years)))
    )

    df = df[(df["year"] >= selected_years[0]) & (df["year"] <= selected_years[1])]

    st.success(f"Filtered rows: {len(df)}")
    st.dataframe(df.head(), width="stretch")

    # =========================================================
    # STEP 3 — MONTHLY REVENUE + MoM
    # =========================================================
    st.markdown("<div class='section-title'>Monthly Revenue</div>", unsafe_allow_html=True)

    monthly = (
        df.groupby("month_period")["collected_amount"]
        .sum()
        .reset_index()
        .sort_values("month_period")
    )
    monthly.rename(columns={"collected_amount": "Revenue (₹)"}, inplace=True)

    st.write("### Table: Monthly Revenue")
    st.dataframe(monthly.style.format({"Revenue (₹)": "{:,.2f}"}), width="stretch")

    monthly["MoM %"] = monthly["Revenue (₹)"].pct_change() * 100
    monthly["MoM %"].fillna(0, inplace=True)

    fig_m = combo_chart_plotly(
        monthly, "month_period", "Revenue (₹)", "MoM %",
        "Monthly Revenue + MoM Growth", "%"
    )
    st.plotly_chart(fig_m, width="stretch")

    # =========================================================
    # QUARTER REVENUE + QoQ
    # =========================================================
    st.markdown("<div class='section-title'>Quarterly Revenue</div>", unsafe_allow_html=True)

    quarterly = (
        df.groupby("quarter_period")["collected_amount"]
        .sum()
        .reset_index()
        .sort_values("quarter_period")
    )
    quarterly.rename(columns={"collected_amount": "Revenue (₹)"}, inplace=True)

    st.write("### Table: Quarterly Revenue")
    st.dataframe(quarterly.style.format({"Revenue (₹)": "{:,.2f}"}), width="stretch")

    quarterly["QoQ %"] = quarterly["Revenue (₹)"].pct_change() * 100
    quarterly["QoQ %"].fillna(0, inplace=True)

    fig_q = combo_chart_plotly(
        quarterly, "quarter_period", "Revenue (₹)", "QoQ %",
        "Quarterly Revenue + QoQ Growth", "%"
    )
    st.plotly_chart(fig_q, width="stretch")

    # =========================================================
    # YEARLY REVENUE + YoY
    # =========================================================
    st.markdown("<div class='section-title'>Annual Revenue</div>", unsafe_allow_html=True)

    yearly = (
        df.groupby("year")["collected_amount"]
        .sum()
        .reset_index()
        .sort_values("year")
    )
    yearly.rename(columns={"collected_amount": "Revenue (₹)"}, inplace=True)

    st.write("### Table: Annual Revenue")
    st.dataframe(yearly.style.format({"Revenue (₹)": "{:,.2f}"}), width="stretch")

    yearly["YoY %"] = yearly["Revenue (₹)"].pct_change() * 100
    yearly["YoY %"].fillna(0, inplace=True)

    fig_y = combo_chart_plotly(
        yearly, "year", "Revenue (₹)", "YoY %",
        "Yearly Revenue + YoY Growth", "%"
    )
    st.plotly_chart(fig_y, width="stretch")

    # =========================================================
    # STEP 4 — KPI SUMMARY
    # =========================================================
    st.markdown("<div class='section-title'>Key KPIs</div>", unsafe_allow_html=True)

    total_rev = df["collected_amount"].sum()
    avg_yoy = yearly["YoY %"].mean() if len(yearly) > 1 else 0.0

    k1, k2, k3 = st.columns(3)
    k1.markdown(f"<div class='kpi'>Total Revenue<br/>₹{total_rev:,.0f}</div>", unsafe_allow_html=True)
    k2.markdown(f"<div class='kpi'>Avg YoY Growth<br/>{avg_yoy:.2f}%</div>", unsafe_allow_html=True)
    k3.markdown(f"<div class='kpi'>Months Tracked<br/>{len(monthly)}</div>", unsafe_allow_html=True)


    # =========================================================
    # STEP 5 — INVESTOR PROJECTION (N-YEAR, RISING EBITDA%)
    # =========================================================
    st.markdown("<div class='section-title'>Investor Projection Model</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        base_rev = st.number_input(
            "Base Revenue for Projection (₹)",
            value=float(total_rev),
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

        ebitda_start_pct = st.number_input(
            "Starting EBITDA Margin (%)",
            min_value=-50.0,
            max_value=100.0,
            value=26.0,
            help="EBITDA margin in Year 1. Example: 26 means 26%."
        )
        ebitda_start = ebitda_start_pct / 100.0

        ebitda_growth_pct = st.number_input(
            "EBITDA Margin YoY Improvement (%)",
            min_value=-50.0,
            max_value=100.0,
            value=4.0,
            help="Example: 4 means EBITDA margin grows 4% per year (compounded)."
        )
        ebitda_growth = ebitda_growth_pct / 100.0

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

    if st.button("Run Projection"):
        if base_rev <= 0:
            st.error("Base Revenue should be greater than zero for a meaningful projection.")
        else:
            years_proj = np.arange(1, int(projection_years) + 1)

            rev_list = []
            ebit_list = []
            ebit_margin_list = []

            cur_rev = base_rev
            cur_margin = ebitda_start

            for _ in years_proj:
                rev_list.append(cur_rev)
                ebit_list.append(cur_rev * cur_margin)
                ebit_margin_list.append(cur_margin * 100)

                cur_rev = cur_rev * (1 + growth)
                cur_margin = cur_margin * (1 + ebitda_growth)

            proj = pd.DataFrame({
                "Year": years_proj,
                "Revenue (₹)": rev_list,
                "EBITDA (₹)": ebit_list,
                "EBITDA %": ebit_margin_list
            })

            proj["Valuation (₹)"] = proj["EBITDA (₹)"] * multiple

            st.write("### Projection Table (Revenue, EBITDA, Valuation)")
            st.dataframe(
                proj.style.format({
                    "Revenue (₹)": "{:,.2f}",
                    "EBITDA (₹)": "{:,.2f}",
                    "EBITDA %": "{:,.2f}",
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
            # INVESTOR OUTCOME (TERMINAL VALUE, ROI, IRR)
            # =====================================================
            terminal_value = proj["Valuation (₹)"].iloc[-1]
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


            # =====================================================
            # AUTOMATED INSIGHTS (DETAILED, INVESTOR-FRIENDLY)
            # =====================================================
            st.markdown("<div class='section-title'>Automated Insights</div>", unsafe_allow_html=True)

            insights = []

            avg_mom = monthly["MoM %"].mean() if len(monthly) > 1 else 0
            avg_yoy = yearly["YoY %"].mean() if len(yearly) > 1 else 0

            # 1) Revenue momentum (MoM)
            if len(monthly) > 3 and avg_mom > 0:
                insights.append(
                    f"Revenue momentum: Your average month-on-month growth is <b>{avg_mom:.1f}%</b>. "
                    f"This means revenue is compounding instead of staying flat. "
                    f"For example, if you are doing around <b>₹{base_rev:,.0f}</b> in Year 1, "
                    f"sustaining similar growth over <b>{int(projection_years)}</b> years can organically push revenue "
                    f"to several times the current level without drastically changing your model."
                )

            # 2) Annual growth vs typical expectations
            if len(yearly) > 1 and avg_yoy > 0:
                if avg_yoy >= 20:
                    insights.append(
                        f"Yearly growth: Your average year-on-year growth is <b>{avg_yoy:.1f}%</b>, "
                        f"which is strong for an EdTech / Analytics hybrid. "
                        f"For investors, this signals that the business is not just stable but expanding at a healthy pace, "
                        f"making it easier to justify higher valuation multiples."
                    )
                else:
                    insights.append(
                        f"Yearly growth: Your average year-on-year growth is <b>{avg_yoy:.1f}%</b>. "
                        f"This is moderate and can still be attractive if combined with high margins and strong retention, "
                        f"but investors may expect a clearer growth plan to push this closer to 20–30%."
                    )

            # 3) EBITDA quality and leverage
            if ebitda_start_pct >= 20:
                insights.append(
                    f"EBITDA quality: You start with an EBITDA margin of <b>{ebitda_start_pct:.1f}%</b>, "
                    f"which is already healthy for your stage. "
                    f"This tells an investor that the business makes solid operating profit on every rupee of revenue, "
                    f"and is not over-dependent on subsidies or heavy discounting."
                )

            if ebitda_growth_pct > 0:
                insights.append(
                    f"Operational leverage: You are assuming EBITDA margin improves by <b>{ebitda_growth_pct:.1f}%</b> each year. "
                    f"In simple terms, this means as the company grows, a larger share of revenue turns into profit. "
                    f"That is exactly what investors like to see: scale making the business more efficient instead of more fragile."
                )

            # 4) Revenue growth assumption check
            if growth_pct > 40:
                insights.append(
                    f"Growth assumption check: You have modelled revenue growth at <b>{growth_pct:.1f}%</b> per year. "
                    f"This is an aggressive assumption. For an investor with no finance background, "
                    f"this means revenue is expected to more than double roughly every 2 years. "
                    f"You should be ready to explain the engine behind this growth: "
                    f"new markets, higher pricing, better sales conversion, or larger batch sizes."
                )
            elif growth_pct > 0:
                insights.append(
                    f"Growth assumption: You have modelled revenue growth at <b>{growth_pct:.1f}%</b> per year. "
                    f"This is a reasonable range for a growing EdTech-Analytics company. "
                    f"To an investor, it says: 'We are not promising miracles, but we are growing steadily and can scale with more capital.'"
                )

            # 5) ROI & payout interpretation
            if invest > 0 and not np.isnan(irr_value):
                multiple = investor_payout / invest if invest > 0 else 0
                insights.append(
                    f"Return on investment: For an investment of <b>₹{invest:,.0f}</b>, the projected payout at the end of Year "
                    f"<b>{int(projection_years)}</b> is about <b>₹{investor_payout:,.0f}</b>. "
                    f"This is roughly a <b>{multiple:.2f}×</b> return on capital, or an internal rate of return (IRR) of <b>{irr_value*100:.2f}%</b>. "
                    f"In simple language: if an investor puts this money in today and your plan works as modelled, "
                    f"their money could grow by that multiple over the projection period."
                )

            # 6) Risk / warning cases
            if invest > 0 and roi < 1:
                insights.append(
                    f"Risk flag: The projected ROI is <b>{roi*100:.1f}%</b>, which is less than 100%. "
                    f"That means the investor does not even double their money over the full period. "
                    f"For most early-stage investors, this will feel weak unless there are other strategic benefits "
                    f"(brand, ecosystem access, or follow-on rounds at higher valuations)."
                )

            if investor_payout < invest:
                insights.append(
                    f"Capital protection warning: The model currently shows an investor payout of "
                    f"<b>₹{investor_payout:,.0f}</b> against an investment of <b>₹{invest:,.0f}</b>. "
                    f"That means they get back less than what they put in. "
                    f"No financial investor will accept this unless the deal is structured as debt instead of equity."
                )

            # 7) Fallback if nothing else triggered
            if not insights:
                insights.append(
                    "The current assumptions look internally consistent. For an investor, this means the model does not show "
                    "extreme risk or unrealistic promises, but you should still support it with pipeline data, historical trends, "
                    "and a clear execution roadmap."
                )

            # Render insights as separate cards with numbering
            for idx, text in enumerate(insights, start=1):
                st.markdown(
                    f"<div class='card'><b>Insight {idx}.</b> {text}</div>",
                    unsafe_allow_html=True
                )


