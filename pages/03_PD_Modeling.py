import streamlit as st
import pandas as pd

from assets.theme import apply_bob_theme

from modules.pd_models import (
    portfolio_pd_summary
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
📈 Probability of Default Modeling
</h2>
<p style="
color:#FFE7D6;
margin-top:5px;
margin-bottom:0;
">
Champion Challenger Framework • Model Performance • Portfolio PD Analytics
</p>
</div>
""",
unsafe_allow_html=True)

# =====================================================
# PIPELINE CHECK
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

leaderboard = (
    st.session_state.leaderboard
)

champion_name = (
    st.session_state.champion_name
)

summary = portfolio_pd_summary(df)

# =====================================================
# KPI SECTION
# =====================================================

avg_auc = None

if leaderboard is not None and "auc" in leaderboard.columns:
    avg_auc = leaderboard["auc"].max()

c1, c2, c3, c4, c5 = st.columns(5)

with c1:

    st.metric(
        "Customers",
        f"{len(df):,}"
    )

with c2:

    st.metric(
        "Features",
        len(df.columns)
    )

with c3:

    st.metric(
        "Champion",
        champion_name
        if champion_name
        else "N/A"
    )

with c4:

    if leaderboard is not None:

        st.metric(
            "Models Tested",
            len(leaderboard)
        )

    else:

        st.metric(
            "Models Tested",
            0
        )
        
with c5:

    st.metric(
        "Best AUC",
        f"{avg_auc:.4f}"
        if avg_auc is not None
        else "N/A"
    )

# =====================================================
# CHAMPION MODEL
# =====================================================

if champion_name:

    st.success(
        f"🏆 Champion Model Selected: {champion_name}"
    )

# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3 = st.tabs(
    [
        "Executive Summary",
        "Model Performance",
        "Risk Analytics"
    ]
)

# =====================================================
# TAB 1
# =====================================================

with tab1:

    st.subheader(
        "PD Portfolio Executive Summary"
    )

    summary_df = pd.DataFrame(
        [
            summary
        ]
    )

    st.dataframe(
        summary_df,
        use_container_width=True,
        hide_index=True
    )

    if "predicted_pd" in df.columns:

        c1, c2 = st.columns(2)

        with c1:

            st.metric(
                "Average PD",
                f"{df['predicted_pd'].mean():.2%}"
            )

        with c2:

            st.metric(
                "High Risk Customers",
                len(
                    df[
                        df[
                            "predicted_pd"
                        ] > 0.20
                    ]
                )
            )


# =====================================================
# TAB 2
# =====================================================

with tab2:

    st.subheader(
        "Model Performance Dashboard"
    )

    if leaderboard is not None:

        metric_cols = [

            c

            for c in leaderboard.columns

            if c in [
                "auc",
                "ks",
                "gini"
            ]
        ]

        if metric_cols:

            st.dataframe(
                leaderboard,
                use_container_width=True,
                hide_index=True
            )

            selected_metric = st.selectbox(
                "Metric",
                metric_cols,
                key="perf_metric"
            )

            model_col = leaderboard.columns[0]

            st.bar_chart(
                leaderboard.set_index(
                    model_col
                )[selected_metric]
            )

            st.subheader(
                "Champion Model Metrics"
            )

            champion_row = leaderboard[
                leaderboard[
                    model_col
                ] == champion_name
            ]

            st.dataframe(
                champion_row,
                use_container_width=True,
                hide_index=True
            )


# =====================================================
# TAB 3
# =====================================================

with tab3:

    st.subheader(
        "Portfolio Risk Analytics"
    )

    candidate_cols = [

        "predicted_pd",
        "pd",
        "probability_default"

    ]

    pd_col = None

    for col in candidate_cols:

        if col in df.columns:

            pd_col = col
            break

    if pd_col:

        st.write(
            f"Using PD Column: {pd_col}"
        )

        risk_bins = pd.cut(

            df[pd_col],

            bins=[
                0,
                0.05,
                0.15,
                0.30,
                1.0
            ],

            labels=[
                "Low Risk",
                "Medium Risk",
                "High Risk",
                "Very High Risk"
            ]

        )

        risk_summary = (
            risk_bins
            .value_counts()
            .reset_index()
        )

        risk_summary.columns = [
            "Risk Segment",
            "Customers"
        ]

        st.dataframe(
            risk_summary,
            use_container_width=True,
            hide_index=True
        )

        try:

            st.bar_chart(
                risk_summary.set_index(
                    "Risk Segment"
                )
            )

        except:

            pass

        st.metric(
            "Average PD",
            f"{df[pd_col].mean():.2%}"
        )

        st.metric(
            "Maximum PD",
            f"{df[pd_col].max():.2%}"
        )
        
        st.subheader(
            "Risk Grade Distribution"
        )

        if "risk_grade" in df.columns:

            risk_grade_summary = (

                df["risk_grade"]
                .value_counts()
                .sort_index()
            )

            st.bar_chart(
                risk_grade_summary
            )

            st.dataframe(
                risk_grade_summary
                .reset_index(),
                use_container_width=True,
                hide_index=True
            )

        st.subheader(
            "Credit Score Distribution"
        )

        if "credit_score" in df.columns:

            st.bar_chart(
                df["credit_score"]
            )

    else:

        st.info(
            "Predicted PD column not found."
        )

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Bank of Baroda • Enterprise Explainable Credit Risk Factory • PD Modeling"
)