import streamlit as st
import pandas as pd

from assets.theme import apply_bob_theme

from modules.scorecard_factory import (
    variable_iv_ranking,
    scorecard_summary
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
🎯 Scorecard Factory
</h2>
<p style="
color:#FFE7D6;
margin-top:5px;
margin-bottom:0;
">
WOE • IV Analysis • Variable Selection • Credit Scorecard Development
</p>
</div>
""",
unsafe_allow_html=True)

# =====================================================
# CHECK DATA
# =====================================================

if st.session_state.portfolio_data is None:

    st.warning(
        "Generate portfolio first."
    )

    st.stop()

df = st.session_state.portfolio_data

# =====================================================
# TARGET DETECTION
# =====================================================

target = None

if "default" in df.columns:
    target = "default"

elif "default_flag" in df.columns:
    target = "default_flag"

if target is None:

    st.error(
        "Target column not found. Expected default or default_flag."
    )

    st.stop()

variables = [
    col
    for col in df.columns
    if col != target
]

# =====================================================
# KPI SECTION
# =====================================================

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "Variables",
        len(variables)
    )

with c2:

    st.metric(
        "Records",
        f"{len(df):,}"
    )

with c3:

    st.metric(
        "Target",
        target
    )

with c4:

    st.metric(
        "Defaults",
        int(df[target].sum())
    )

# =====================================================
# BUILD SCORECARD
# =====================================================

if st.button(
    "🚀 Build Scorecard",
    use_container_width=True
):

    with st.spinner(
        "Calculating WOE / IV..."
    ):

        try:

            iv_report = variable_iv_ranking(
                df,
                variables,
                target
            )

            scorecard_report = scorecard_summary(
                iv_report
            )

            st.session_state.iv_report = iv_report
            st.session_state.scorecard_report = scorecard_report

            st.success(
                "Scorecard successfully generated."
            )

        except Exception as e:

            st.error(
                f"Scorecard generation failed: {e}"
            )

# =====================================================
# DISPLAY RESULTS
# =====================================================

if st.session_state.get("iv_report") is not None:

    iv_report = (
        st.session_state.iv_report
    )

    scorecard_report = (
        st.session_state.scorecard_report
    )

    # =================================================
    # KPI ANALYTICS
    # =================================================

    strong_vars = 0

    if "iv" in iv_report.columns:

        strong_vars = (
            iv_report["iv"] > 0.30
        ).sum()
        
    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Variables Ranked",
        len(iv_report)
    )

    c2.metric(
        "Strong Predictors",
        int(strong_vars)
    )

    c3.metric(
        "Top Variables",
        min(
            len(iv_report),
            10
        )
    )

    # =================================================
    # TABS
    # =================================================

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "IV Ranking",
            "Scorecard Summary",
            "Variable Explorer",
            "Predictor Quality"
        ]
    )

    # =============================================
    # TAB 1
    # =============================================

    with tab1:

        st.subheader(
            "Information Value Ranking"
        )

        st.dataframe(
            iv_report,
            use_container_width=True,
            hide_index=True
        )

        if "iv" in iv_report.columns:

            chart_df = (
                iv_report
                .sort_values(
                    "iv",
                    ascending=False
                )
                .head(15)
            )

            st.subheader(
                "Top Predictive Variables"
            )

            st.bar_chart(
                chart_df.set_index(
                    chart_df.columns[0]
                )["iv"]
            )

    # =============================================
    # TAB 2
    # =============================================

    with tab2:

        st.subheader(
            "Executive Scorecard Dashboard"
        )

        summary_df = pd.DataFrame(
            [scorecard_report]
        )

        st.dataframe(
            summary_df,
            use_container_width=True,
            hide_index=True
        )

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Variables Tested",
            scorecard_report.get(
                "variables_tested",
                0
            )
        )

        c2.metric(
            "Strong Variables",
            scorecard_report.get(
                "strong_variables",
                0
            )
        )

        c3.metric(
            "Medium Variables",
            scorecard_report.get(
                "medium_variables",
                0
            )
        )

    # =============================================
    # TAB 3
    # =============================================

    with tab3:

        selected_variable = st.selectbox(
            "Select Variable",
            iv_report.iloc[:, 0]
        )

        filtered = iv_report[
            iv_report.iloc[:, 0]
            == selected_variable
        ]

        st.dataframe(
            filtered,
            use_container_width=True,
            hide_index=True
        )

        st.info(
            f"Detailed scorecard information for {selected_variable}"
        )

    # =============================================
    # TAB 4
    # =============================================
        
    with tab4:

        st.subheader(
            "Predictor Strength Distribution"
        )

        if "strength" in iv_report.columns:

            strength_summary = (
                iv_report["strength"]
                .value_counts()
            )

            st.bar_chart(
                strength_summary
            )

            st.dataframe(
                strength_summary
                .reset_index(),
                use_container_width=True,
                hide_index=True
            )

# =====================================================
# EMPTY STATE
# =====================================================

else:

    st.info(
        """
        Click 'Build Scorecard'
        to calculate Information Value,
        variable rankings and scorecard analytics.
        """
    )

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Bank of Baroda • Enterprise Explainable Credit Risk Factory • Scorecard Factory"
)