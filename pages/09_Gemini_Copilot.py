import time
import streamlit as st

from assets.theme import apply_bob_theme

from modules.gemini_copilot import (

    portfolio_risk_review,
    model_validation_report,
    board_summary,
    stress_test_report,
    ifrs9_commentary,

    underwriting_summary,
    adverse_action_letter,
    next_best_action,
    collection_strategy,
    xai_summary

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
🤖 Gemini Risk Copilot
</h2>
<p style="
color:#FFE7D6;
margin-top:5px;
margin-bottom:0;
">
Executive Intelligence • Board Reporting • Risk Commentary • AI Copilot
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
# KPI SECTION
# =====================================================

metrics = st.session_state.portfolio_metrics

c1, c2, c3, c4, c5 = st.columns(5)

with c1:

    st.metric(
        "Customers",
        f"{metrics.get('customers',0):,}"
    )

with c2:

    st.metric(
        "Average Score",
        round(
            metrics.get(
                "avg_score",
                0
            ),
            0
        )
    )

with c3:

    st.metric(
        "Average PD",
        f"{metrics.get('avg_pd',0):.2%}"
    )

with c4:

    st.metric(
        "Default Rate",
        f"{metrics.get('default_rate',0):.2%}"
    )

with c5:

    st.metric(
        "Champion Model",
        st.session_state.champion_name
    )

# =====================================================
# AI COPILOT WORKBENCH
# =====================================================

st.subheader(
    "AI Copilot Workbench"
)

copilot_mode = st.radio(
    "Copilot Mode",
    [
        "Executive Reporting",
        "Customer Advisor"
    ],
    horizontal=True
)

if copilot_mode == "Customer Advisor":

    twins = st.session_state.digital_twins

    customer_id = st.selectbox(
        "Select Customer",
        list(twins.keys())
    )

    twin = twins[customer_id]

    advisor_tab1, advisor_tab2, advisor_tab3, advisor_tab4 = st.tabs(
        [
            "Underwriting",
            "Next Best Action",
            "Collections",
            "Adverse Action"
        ]
    )

    with advisor_tab1:

        if st.button(
            "Generate Underwriting Memo"
        ):

            report = underwriting_summary(
                twin
            )

            st.markdown(report)

    with advisor_tab2:

        if st.button(
            "Generate Relationship Plan"
        ):

            report = next_best_action(
                twin
            )

            st.markdown(report)

    with advisor_tab3:

        if st.button(
            "Generate Collection Strategy"
        ):

            report = collection_strategy(
                twin
            )

            st.markdown(report)

    with advisor_tab4:

        if st.button(
            "Generate Adverse Action Letter"
        ):

            report = adverse_action_letter(
                twin
            )

            st.markdown(report)

    st.stop()

# =====================================================
# REPORT MENU
# =====================================================

st.subheader(
    "Executive Report Generator"
)

selected_reports = st.multiselect(

    "Select Reports",

    [
        "Portfolio Risk Review",
        "Model Validation",
        "IFRS9 Commentary",
        "Stress Test Report",
        "Board Report",
        "XAI Summary"
    ],

    default=[

        "Portfolio Risk Review",
        "Board Report"

    ]

)

# =====================================================
# GENERATE REPORTS
# =====================================================

if st.button(
    "🚀 Generate Reports",
    use_container_width=True
):

    reports = {}

    progress = st.progress(0)

    status = st.empty()

    total_reports = len(
        selected_reports
    )

    current = 0

    # ==========================================
    # PORTFOLIO REVIEW
    # ==========================================

    if "Portfolio Risk Review" in selected_reports:

        status.info(
            "Generating Portfolio Risk Review..."
        )

        reports["Portfolio Risk Review"] = (

            portfolio_risk_review(
                st.session_state.portfolio_metrics
            )

        )

        current += 1

        progress.progress(
            int(
                current /
                total_reports *
                100
            )
        )

        time.sleep(1)

    # ==========================================
    # MODEL VALIDATION
    # ==========================================

    if "Model Validation" in selected_reports:

        status.info(
            "Generating Model Validation Report..."
        )

        reports["Model Validation"] = (

            model_validation_report(
                st.session_state.leaderboard
            )

        )

        current += 1

        progress.progress(
            int(
                current /
                total_reports *
                100
            )
        )

        time.sleep(1)

    # ==========================================
    # IFRS9
    # ==========================================

    if "IFRS9 Commentary" in selected_reports:

        status.info(
            "Generating IFRS9 Commentary..."
        )

        reports["IFRS9 Commentary"] = (

            ifrs9_commentary(
                st.session_state.portfolio_metrics
            )

        )

        current += 1

        progress.progress(
            int(
                current /
                total_reports *
                100
            )
        )

        time.sleep(1)

    # ==========================================
    # STRESS TEST
    # ==========================================

    if "Stress Test Report" in selected_reports:

        status.info(
            "Generating Stress Test Report..."
        )

        reports["Stress Test Report"] = (

            stress_test_report(
                st.session_state.portfolio_metrics
            )

        )

        current += 1

        progress.progress(
            int(
                current /
                total_reports *
                100
            )
        )

        time.sleep(1)

    # ==========================================
    # BOARD REPORT
    # ==========================================

    if "Board Report" in selected_reports:

        status.info(
            "Generating Board Summary..."
        )

        executive_payload = {

            "portfolio_metrics":
                st.session_state.portfolio_metrics,

            "champion_model":
                st.session_state.champion_name,

            "leaderboard":
                st.session_state.leaderboard
                .to_dict("records")

        }

        reports["Board Report"] = (

            board_summary(
                executive_payload
            )

        )

        current += 1

        progress.progress(
            int(
                current /
                total_reports *
                100
            )
        )

        time.sleep(1)
    
    # ==========================================
    # XAI Summary
    # ==========================================

    if "XAI Summary" in selected_reports:

        status.info(
            "Generating XAI Summary..."
        )

        xai_payload = {

            "champion_model":
                st.session_state.champion_name,

            "portfolio_metrics":
                st.session_state.portfolio_metrics

        }

        reports["XAI Summary"] = (

            xai_summary(
                xai_payload
            )

        )

        current += 1

        progress.progress(
            int(
                current /
                total_reports *
                100
            )
        )

        time.sleep(1)

    status.success(
        "All reports generated successfully."
    )

    st.session_state.copilot_reports = reports

# =====================================================
# DISPLAY REPORTS
# =====================================================

if st.session_state.copilot_reports != None:

    st.divider()

    st.subheader(
        "Generated Executive Reports"
    )

    reports = (
        st.session_state.copilot_reports
    )

    for title, report in reports.items():

        with st.expander(
            title,
            expanded=False
        ):

            st.markdown(report)

            st.download_button(

                f"📥 Download {title}",

                data=report,

                file_name=
                title.replace(
                    " ",
                    "_"
                ) + ".txt",

                key=title

            )

# =====================================================
# EXECUTIVE INSIGHT
# =====================================================

st.divider()

st.subheader(
    "AI Executive Insight"
)

avg_pd = metrics.get(
    "avg_pd",
    0
)

if avg_pd < 0.05:

    st.success(
        """
        Portfolio demonstrates
        strong credit quality and
        healthy risk-adjusted returns.
        """
    )

elif avg_pd < 0.15:

    st.warning(
        """
        Moderate risk concentration
        detected. Continue active
        monitoring and governance.
        """
    )

else:

    st.error(
        """
        Elevated portfolio risk.
        Management intervention
        recommended.
        """
    )

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Bank of Baroda • Enterprise Explainable Credit Risk Factory • Gemini Risk Copilot"
)