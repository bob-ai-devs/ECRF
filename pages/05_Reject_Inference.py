import streamlit as st
import pandas as pd
import numpy as np

from assets.theme import apply_bob_theme

from modules.reject_inference import (
    create_accept_reject_population,
    reject_inference_summary,
    ParcelingRejectInference,
    FuzzyAugmentation,
    ProfitabilitySimulator,
    CutoffAnalyzer,
    RiskAppetiteSimulator,
    expansion_opportunity
)

from config import *

# =====================================================
# THEME
# =====================================================

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_bob_theme()

# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div style="
background:linear-gradient(90deg,#703A00,#00509E);
padding:20px;
border-radius:15px;
margin-bottom:20px;
">
<h2 style="
color:white !important;
margin:0;
">
🚫 Reject Inference Lab
</h2>
<p style="
color:#FFE7D6;
margin-top:5px;
margin-bottom:0;
">
Portfolio Expansion • Approval Strategy • Risk Appetite Analytics
</p>
</div>
""",
unsafe_allow_html=True)

# =====================================================
# CHECK PIPELINE
# =====================================================

if not st.session_state.pipeline_completed:

    st.warning(
        "Run Full ECRF Pipeline first."
    )

    st.stop()

# =====================================================
# DATA
# =====================================================

df = st.session_state.portfolio_data

df = create_accept_reject_population(
    df
)

# =====================================================
# SUMMARY
# =====================================================

summary = reject_inference_summary(
    df
)

st.session_state.reject_inference_summary = (
    summary
)

expansion = expansion_opportunity(
    df,
    cutoff_score=650
)

near_prime = expansion["near_prime"]

expansion_ratio = (
    expansion["expansion_ratio"] * 100
)

# =====================================================
# KPI SECTION
# =====================================================

total_apps = len(df)

accepted = 0
rejected = 0

candidate_cols = [
    "application_status",
    "decision",
    "approved"
]

status_col = None

for col in candidate_cols:

    if col in df.columns:

        status_col = col
        break

if status_col:

    accepted = (
        df[status_col]
        .astype(str)
        .str.upper()
        .isin(
            [
                "APPROVED",
                "ACCEPTED",
                "YES",
                "1",
                "TRUE"
            ]
        )
        .sum()
    )

    rejected = total_apps - accepted
    
    approval_rate = (
        accepted / total_apps * 100
        if total_apps > 0
        else 0
    )

k1,k2,k3,k4,k5,k6 = st.columns(6)

with k1:
    st.metric(
        "Applications",
        f"{total_apps:,}"
    )

with k2:
    st.metric(
        "Accepted",
        f"{accepted:,}"
    )

with k3:
    st.metric(
        "Rejected",
        f"{rejected:,}"
    )

with k4:
    st.metric(
        "Approval Rate",
        f"{approval_rate:.1f}%"
    )

with k5:
    st.metric(
        "Near Prime",
        f"{near_prime:,}"
    )

with k6:
    st.metric(
        "Expansion %",
        f"{expansion_ratio:.1f}%"
    )

# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        "Executive Dashboard",
        "Cutoff Optimization",
        "Inference Engine",
        "Expansion Analytics",
        "Profitability Lab",
        "Raw Data"
    ]
)

# =====================================================
# TAB 1
# =====================================================

with tab1:

    st.subheader(
        "Executive Reject Inference Overview"
    )

    c1,c2 = st.columns(2)

    with c1:

        distribution = pd.Series(
            {
                "Approved":accepted,
                "Rejected":rejected
            }
        )

        st.bar_chart(
            distribution
        )

    with c2:

        st.metric(
            "Potential Recoverable Customers",
            near_prime
        )

        st.metric(
            "Expansion Opportunity",
            f"{expansion_ratio:.1f}%"
        )

    st.dataframe(
        pd.DataFrame([summary]),
        use_container_width=True,
        hide_index=True
    )

# =====================================================
# TAB 2
# =====================================================

with tab2:

    st.subheader(
        "Risk Appetite Simulator"
    )

    analyzer = CutoffAnalyzer()

    cutoff_df = (
        analyzer.evaluate_cutoffs(df)
    )

    st.dataframe(
        cutoff_df,
        use_container_width=True,
        hide_index=True
    )

    st.line_chart(
        cutoff_df.set_index(
            "cutoff"
        )[
            [
                "approval_rate",
                "avg_pd"
            ]
        ]
    )

    recommender = (
        RiskAppetiteSimulator()
    )

    recommendation = (
        recommender.recommend_cutoff(
            cutoff_df,
            max_pd=0.10
        )
    )

    if recommendation:

        st.success(
            f"""
            Recommended Cutoff:
            {recommendation['recommended_cutoff']}
            |
            Approval Rate:
            {recommendation['approval_rate']:.2%}
            |
            Avg PD:
            {recommendation['avg_pd']:.2%}
            """
        )

# =====================================================
# TAB 3
# =====================================================

with tab3:

    st.subheader(
        "Inference Method Comparison"
    )

    method = st.selectbox(
        "Method",
        [
            "Parceling",
            "Fuzzy Augmentation"
        ]
    )

    if method == "Parceling":

        parcel = (
            ParcelingRejectInference()
        )

        inferred = parcel.infer(df)

        st.dataframe(
            inferred.head(100),
            use_container_width=True
        )

    else:

        fuzzy = (
            FuzzyAugmentation()
        )

        inferred = fuzzy.infer(df)

        st.dataframe(
            inferred.head(100),
            use_container_width=True
        )    
    
# =====================================================
# TAB 4
# =====================================================

with tab4:

    st.subheader(
        "Portfolio Expansion Analysis"
    )

    exp_df = pd.DataFrame(
        {
            "Metric":[
                "Rejected",
                "Near Prime"
            ],
            "Count":[
                expansion["rejected"],
                expansion["near_prime"]
            ]
        }
    )

    st.dataframe(
        exp_df,
        use_container_width=True,
        hide_index=True
    )

    st.bar_chart(
        exp_df.set_index(
            "Metric"
        )
    )
    
# =====================================================
# TAB 5
# =====================================================

with tab5:

    st.subheader(
        "Portfolio Profitability"
    )

    simulator = (
        ProfitabilitySimulator()
    )

    amount_col = None

    for col in [
        "loan_amount",
        "sanction_amount",
        "amount"
    ]:

        if col in df.columns:

            amount_col = col
            break

    if (
        amount_col
        and
        "predicted_pd"
        in df.columns
    ):

        profit = (
            simulator.portfolio_profit(
                df,
                amount_column=amount_col
            )
        )

        st.metric(
            "Expected Portfolio Profit",
            f"₹ {profit:,.0f}"
        )

    else:

        st.info(
            "Loan amount column unavailable."
        )    
    
# =====================================================
# TAB 6
# =====================================================

with tab6:

    st.subheader(
        "Reject Inference Dataset"
    )

    st.dataframe(
        df,
        use_container_width=True,
        height=700
    )

# =====================================================
# EXECUTIVE INSIGHT
# =====================================================

st.divider()

st.subheader(
    "Executive Recommendation"
)

if expansion_ratio > 30:

    st.success(
        f"""
        Significant portfolio expansion
        opportunity detected.

        {near_prime:,} rejected customers
        fall within the near-prime segment.

        Consider revisiting the current
        score cutoff strategy.
        """
    )

elif expansion_ratio > 15:

    st.warning(
        """
        Moderate expansion opportunity
        exists with controlled risk.
        """
    )

else:

    st.info(
        """
        Current underwriting policy
        appears appropriately calibrated.
        """
    )

# =====================================================
# EXPORT
# =====================================================

st.download_button(
    "📥 Download Reject Inference Summary",
    data=str(summary),
    file_name="reject_inference_summary.csv"
)

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Bank of Baroda • Enterprise Explainable Credit Risk Factory • Reject Inference"
)