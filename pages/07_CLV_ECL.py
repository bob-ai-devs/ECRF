import streamlit as st
import pandas as pd

from assets.theme import apply_bob_theme

from modules.clv_ecl_engine import (
    ecl_summary,
    StressScenarioEngine
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
💰 CLV / ECL Intelligence Center
</h2>
<p style="
color:#FFE7D6;
margin-top:5px;
margin-bottom:0;
">
IFRS9 Analytics • Expected Credit Loss • Customer Lifetime Value • Portfolio Profitability
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

summary = ecl_summary(df)

# =====================================================
# EXECUTIVE KPI RIBBON
# =====================================================

portfolio_size = len(df)

portfolio_ecl = (
    df["ecl"].sum()
    if "ecl" in df.columns
    else 0
)

avg_ecl = (
    df["ecl"].mean()
    if "ecl" in df.columns
    else 0
)

stage3_count = (
    (df["ifrs9_stage"] == "Stage 3").sum()
    if "ifrs9_stage" in df.columns
    else 0
)

avg_pd = None

for col in [
    "predicted_pd",
    "pd",
    "probability_default"
]:
    if col in df.columns:
        avg_pd = df[col].mean() * 100
        break

k1, k2, k3, k4, k5 = st.columns(5)

k1.metric(
    "Customers",
    f"{portfolio_size:,}"
)

k2.metric(
    "Portfolio ECL",
    f"₹{portfolio_ecl:,.0f}"
)

k3.metric(
    "Average ECL",
    f"₹{avg_ecl:,.0f}"
)

k4.metric(
    "Stage 3 Accounts",
    f"{stage3_count:,}"
)

k5.metric(
    "Average PD",
    f"{avg_pd:.2f}%"
    if avg_pd is not None
    else "N/A"
)

# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "Executive Dashboard",
        "IFRS9 Staging",
        "ECL Analytics",
        "Stress Testing",
        "Portfolio Explorer"
    ]
)

# =====================================================
# TAB 1
# =====================================================

with tab1:

    st.subheader(
        "Executive Credit Loss Dashboard"
    )

    c1, c2 = st.columns([2,1])

    with c1:

        if "ecl" in df.columns:

            ecl_dist = (
                df["ecl"]
                .describe()
                .reset_index()
            )

            st.dataframe(
                ecl_dist,
                use_container_width=True,
                hide_index=True
            )

    with c2:

        if "ifrs9_stage" in df.columns:

            stage_counts = (
                df["ifrs9_stage"]
                .value_counts()
            )

            st.bar_chart(
                stage_counts
            )

    st.divider()

    st.subheader(
        "Executive Summary"
    )

    st.dataframe(summary)

# =====================================================
# TAB 2
# =====================================================

with tab2:

    st.subheader(
        "IFRS9 Stage Distribution"
    )

    if "ifrs9_stage" in df.columns:

        stage_summary = (
            df["ifrs9_stage"]
            .value_counts()
            .reset_index()
        )

        stage_summary.columns = [
            "Stage",
            "Accounts"
        ]

        st.dataframe(
            stage_summary,
            use_container_width=True,
            hide_index=True
        )

        st.bar_chart(
            stage_summary.set_index(
                "Stage"
            )
        )

        stage3_df = df[
            df["ifrs9_stage"] == "Stage 3"
        ]

        st.subheader(
            "High Risk Accounts"
        )

        st.dataframe(
            stage3_df.head(100),
            use_container_width=True
        )

    else:

        st.info(
            "IFRS9 stages unavailable."
        )

# =====================================================
# TAB 3
# =====================================================

with tab3:

    st.subheader(
        "ECL Concentration Analytics"
    )

    if "ecl" in df.columns:

        top_ecl = (
            df.sort_values(
                "ecl",
                ascending=False
            )
            .head(20)
        )

        st.bar_chart(
            top_ecl["ecl"]
        )

        st.dataframe(
            top_ecl,
            use_container_width=True
        )

    else:

        st.info(
            "ECL values unavailable."
        )


with tab4:

    st.subheader(
        "Portfolio Stress Testing"
    )

    if "predicted_pd" in df.columns:

        base_ecl = (
            df["ecl"].sum()
            if "ecl" in df.columns
            else 0
        )

        mild_df = StressScenarioEngine.mild(df)
        moderate_df = StressScenarioEngine.moderate(df)
        severe_df = StressScenarioEngine.severe(df)

        stress_df = pd.DataFrame({

            "Scenario":[
                "Baseline",
                "Mild",
                "Moderate",
                "Severe"
            ],

            "PD Multiplier":[
                1.0,
                1.1,
                1.3,
                1.6
            ]
        })

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
        

with tab5:

    st.subheader(
        "Portfolio Explorer"
    )

    stage_filter = st.multiselect(

        "IFRS9 Stage",

        options=

        sorted(
            df["ifrs9_stage"]
            .dropna()
            .unique()
        )

        if "ifrs9_stage"
        in df.columns

        else []
    )

    filtered_df = df.copy()

    if stage_filter:

        filtered_df = filtered_df[

            filtered_df[
                "ifrs9_stage"
            ].isin(
                stage_filter
            )
        ]

    st.dataframe(
        filtered_df,
        use_container_width=True
    )
    
    
    

# =====================================================
# EXECUTIVE COMMENTARY
# =====================================================

st.divider()

st.subheader(
    "Executive Risk Commentary"
)

if avg_pd is not None:

    if avg_pd < 5:

        st.success(
            """
            Portfolio exhibits strong credit
            quality with limited expected
            credit loss exposure.
            """
        )

    elif avg_pd < 15:

        st.warning(
            """
            Moderate expected credit loss
            exposure detected. Enhanced
            monitoring recommended.
            """
        )

    else:

        st.error(
            """
            Elevated credit risk profile
            observed. Portfolio provisioning
            and collection strategies should
            be reviewed.
            """
        )

else:

    st.info(
        "PD metrics unavailable."
    )

# =====================================================
# EXPORT
# =====================================================

st.download_button(
    "📥 Download ECL Summary",
    data=str(summary),
    file_name="ecl_summary.csv"
)

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Bank of Baroda • Enterprise Explainable Credit Risk Factory • CLV / ECL"
)