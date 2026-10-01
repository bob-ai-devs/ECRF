import streamlit as st
import pandas as pd

from assets.theme import apply_bob_theme

from modules.digital_twin import (
    twin_summary,
    CustomerTrajectory
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
👤 Customer Digital Twin Center
</h2>
<p style="
color:#FFE7D6;
margin-top:5px;
margin-bottom:0;
">
Customer 360 • Risk Intelligence • Relationship Analytics • Next Best Action
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
# DIGITAL TWIN DATA
# =====================================================

twins = st.session_state.digital_twins

if len(twins) == 0:

    st.warning(
        "No Digital Twin data available."
    )

    st.stop()

# =====================================================
# KPI SECTION
# =====================================================

total_customers = len(twins)

avg_pd = sum(
    t["risk"]["predicted_pd"]
    for t in twins.values()
) / total_customers

avg_relationship = sum(
    t["relationship_score"]
    for t in twins.values()
) / total_customers

high_risk = sum(
    1
    for t in twins.values()
    if t["risk"]["predicted_pd"] > 0.20
)

alert_count = sum(
    len(t["alerts"])
    for t in twins.values()
)

c1, c2, c3, c4, c5 = st.columns(5)

with c1:

    st.metric(
        "Digital Twins",
        f"{total_customers:,}"
    )

with c2:

    st.metric(
        "Average PD",
        f"{avg_pd:.2%}"
    )

with c3:

    st.metric(
        "Relationship Score",
        f"{avg_relationship:.1f}"
    )

with c4:

    st.metric(
        "High Risk Customers",
        high_risk
    )

with c5:

    st.metric(
        "Active Alerts",
        alert_count
    )
    
# =====================================================
# VIEW SELECTION
# =====================================================

view = st.radio(
    "View",
    [
        "Single Customer",
        "Portfolio Overview"
    ],
    horizontal=True
)

# =====================================================
# SINGLE CUSTOMER
# =====================================================

if view == "Single Customer":

    customer_id = st.selectbox(
        "Select Customer",
        list(twins.keys())
    )

    twin = twins[customer_id]

    summary = twin_summary(
        twin
    )

    # ============================================
    # CUSTOMER KPIs
    # ============================================

    score = twin["risk"].get(
        "credit_score",
        0
    )

    pd_value = twin["risk"].get(
        "predicted_pd",
        0
    )

    relationship = twin.get(
        "relationship_score",
        0
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Credit Score",
            round(score, 0)
        )

    with c2:

        st.metric(
            "Predicted PD",
            f"{pd_value:.2%}"
        )

    with c3:

        st.metric(
            "Relationship Score",
            round(
                relationship,
                1
            )
        )

    # ============================================
    # TABS
    # ============================================

    # ============================================
    # DIGITAL TWIN WORKBENCH
    # ============================================

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        [
            "360 Profile",
            "Risk Intelligence",
            "Early Warnings",
            "Actions",
            "Stress Testing",
            "Trajectory"
        ]
    )

    # =====================================================
    # TAB 1
    # =====================================================

    with tab1:

        st.subheader(
            "Customer 360 Profile"
        )

        profile_df = pd.DataFrame(
            twin["profile"].items(),
            columns=[
                "Attribute",
                "Value"
            ]
        )

        st.dataframe(
            profile_df,
            use_container_width=True,
            hide_index=True
        )

        st.subheader(
            "Behavior Profile"
        )

        behavior_df = pd.DataFrame(
            twin["behavior"].items(),
            columns=[
                "Attribute",
                "Value"
            ]
        )

        st.dataframe(
            behavior_df,
            use_container_width=True,
            hide_index=True
        )

    # =====================================================
    # TAB 2
    # =====================================================

    with tab2:

        st.subheader(
            "Risk Intelligence"
        )

        risk_df = pd.DataFrame(
            twin["risk"].items(),
            columns=[
                "Attribute",
                "Value"
            ]
        )

        st.dataframe(
            risk_df,
            use_container_width=True,
            hide_index=True
        )

        st.subheader(
            "IFRS9 Profile"
        )

        ifrs_df = pd.DataFrame(
            twin["ifrs9"].items(),
            columns=[
                "Attribute",
                "Value"
            ]
        )

        st.dataframe(
            ifrs_df,
            use_container_width=True,
            hide_index=True
        )

    # =====================================================
    # TAB 3
    # =====================================================

    with tab3:

        st.subheader(
            "Early Warning Signals"
        )

        alerts = twin["alerts"]

        if alerts:

            for alert in alerts:

                st.warning(alert)

        else:

            st.success(
                "No active warning signals."
            )

    # =====================================================
    # TAB 4
    # =====================================================

    with tab4:

        st.subheader(
            "Recommended Actions"
        )

        actions = twin["actions"]

        if actions:

            for action in actions:

                st.info(action)

        else:

            st.success(
                "No actions required."
            )

    # =====================================================
    # TAB 5
    # =====================================================

    with tab5:

        st.subheader(
            "Stress Scenario Impact"
        )

        stress_df = pd.DataFrame(
            twin["stress"].items(),
            columns=[
                "Scenario",
                "PD"
            ]
        )

        st.dataframe(
            stress_df,
            use_container_width=True,
            hide_index=True
        )

        st.line_chart(
            stress_df.set_index(
                "Scenario"
            )
        )

    # =====================================================
    # TAB 6
    # =====================================================

    with tab6:

        st.subheader(
            "12-Month Risk Forecast"
        )

        forecast_df = (
            CustomerTrajectory.forecast(
                {
                    **twin["profile"],
                    **twin["risk"],
                    **twin["behavior"]
                }
            )
        )

        st.line_chart(
            forecast_df.set_index(
                "month"
            )
        )

        st.dataframe(
            forecast_df,
            use_container_width=True,
            hide_index=True
        )

# =====================================================
# PORTFOLIO VIEW
# =====================================================

else:

    st.subheader(
        "Portfolio Digital Twin Dashboard"
    )

    portfolio_summary = {

        "Total Customers":
            total_customers,

        "Average PD":
            round(
                avg_pd,
                4
            ),

        "Average Relationship Score":
            round(
                avg_relationship,
                2
            ),

        "High Risk Customers":
            high_risk

    }

    summary_df = pd.DataFrame(
        portfolio_summary.items(),
        columns=[
            "Metric",
            "Value"
        ]
    )

    st.dataframe(
        summary_df,
        use_container_width=True,
        hide_index=True
    )

    # ============================================
    # PD SEGMENTATION
    # ============================================

    pd_bucket = {

        "Low Risk": 0,
        "Medium Risk": 0,
        "High Risk": 0

    }

    for twin in twins.values():

        pd_val = twin["risk"][
            "predicted_pd"
        ]

        if pd_val < 0.05:

            pd_bucket[
                "Low Risk"
            ] += 1

        elif pd_val < 0.20:

            pd_bucket[
                "Medium Risk"
            ] += 1

        else:

            pd_bucket[
                "High Risk"
            ] += 1

    st.subheader(
        "Risk Segmentation"
    )

    st.bar_chart(
        pd.Series(pd_bucket)
    )
    
    st.subheader(
        "Relationship Score Distribution"
    )

    relationship_scores = [

        t["relationship_score"]

        for t in twins.values()

    ]

    relationship_df = pd.DataFrame(
        {
            "Relationship Score":
            relationship_scores
        }
    )

    st.bar_chart(
        relationship_df
    )

# =====================================================
# EXECUTIVE COMMENTARY
# =====================================================

st.divider()

st.subheader(
    "Executive Commentary"
)

if avg_pd < 0.05:

    st.success(
        """
        Digital Twin portfolio indicates
        strong customer quality and low
        expected risk exposure.
        """
    )

elif avg_pd < 0.15:

    st.warning(
        """
        Moderate portfolio risk observed.
        Proactive monitoring advised.
        """
    )

else:

    st.error(
        """
        Elevated portfolio risk detected.
        Consider enhanced customer actions
        and retention strategies.
        """
    )

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Bank of Baroda • Enterprise Explainable Credit Risk Factory • Digital Twin"
)