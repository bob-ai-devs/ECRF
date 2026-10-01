import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from assets.theme import apply_bob_theme

from modules.portfolio_monitor import (
    monitoring_summary,
    RiskConcentration,
    EarlyWarningSignals,
    RiskHeatmap,
    ThresholdMonitor,
    RegulatoryMonitor,
    VintageAnalysis
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
📉 Portfolio Monitoring Center
</h2>
<p style="
color:#FFE7D6;
margin-top:5px;
margin-bottom:0;
">
Portfolio Health • Drift Detection • Risk Surveillance • Early Warning Monitoring
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

summary = monitoring_summary(df)

# =====================================================
# KPI SECTION
# =====================================================

total_customers = len(df)

avg_score = None
avg_pd = None

candidate_score_cols = [
    "credit_score",
    "score",
    "risk_score"
]

for col in candidate_score_cols:

    if col in df.columns:

        avg_score = round(
            df[col].mean(),
            0
        )

        break

candidate_pd_cols = [
    "predicted_pd",
    "pd",
    "probability_default"
]

for col in candidate_pd_cols:

    if col in df.columns:

        avg_pd = (
            df[col].mean() * 100
        )

        break

k1,k2,k3,k4,k5,k6 = st.columns(6)

with k1:
    st.metric("Customers", f"{len(df):,}")

with k2:
    st.metric("Features", len(df.columns))

with k3:
    st.metric("Avg Score", avg_score)

with k4:
    st.metric("Avg PD", f"{avg_pd:.2f}%")

with k5:
    st.metric(
        "Default Rate",
        f"{summary['default_rate']*100:.2f}%"
    )

with k6:
    status = RegulatoryMonitor.rag(
        0.05,
        summary["avg_pd"]
    )

    st.metric(
        "Reg Status",
        status
    )

# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Executive Dashboard",
    "Drift Monitoring",
    "Migration Analysis",
    "Risk Surveillance",
    "Governance",
    "Raw Data"
])

# =====================================================
# TAB 1
# =====================================================

with tab1:

    st.subheader("Portfolio Health Overview")

    health_score = max(
        0,
        min(
            100,
            100 - (avg_pd * 2)
        )
    )

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=health_score,
            title={"text":"Portfolio Health"},
            gauge={
                "axis":{"range":[0,100]},
                "bar": {"color": "#224488"},
                "steps":[
                    {"range":[0,50],"color":"red"},
                    {"range":[50,75],"color":"orange"},
                    {"range":[75,100],"color":"green"}
                ]
            }
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
    
    score_col = "credit_score"

    fig = px.histogram(
        df,
        x=score_col,
        nbins=25,
        title="Credit Score Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
    
    fig = px.histogram(
        df,
        x="predicted_pd",
        nbins=20,
        title="Probability of Default Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# TAB 2
# =====================================================

with tab2:

    st.subheader(
        "Portfolio Stability Monitoring"
    )

    st.info(
        "Connect baseline dataset to activate full PSI/CSI monitoring."
    )

    drift_df = pd.DataFrame({
        "Feature":[
            "Income",
            "Utilization",
            "Age",
            "DTI"
        ],
        "PSI":[
            0.03,
            0.08,
            0.14,
            0.28
        ]
    })

    st.dataframe(
        drift_df,
        use_container_width=True,
        hide_index=True
    )

    fig = px.bar(
        drift_df,
        x="Feature",
        y="PSI",
        title="Top Drifted Features"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# TAB 3
# =====================================================

with tab3:

    st.subheader(
        "Credit Migration Analytics"
    )

    migration = pd.DataFrame(
        np.random.rand(5,5),
        columns=[
            "VL",
            "L",
            "M",
            "H",
            "VH"
        ]
    )

    fig = px.imshow(
        migration,
        text_auto=True,
        title="Migration Matrix"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
    
    
# =====================================================
# TAB 4
# =====================================================

with tab4:

    if "risk_grade" in df.columns:

        concentration = (
            RiskConcentration.by_grade(df)
        )

        st.dataframe(
            concentration,
            use_container_width=True,
            hide_index=True
        )

        fig = px.bar(
            concentration,
            x="risk_grade",
            y="customers",
            color="avg_pd"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
        
        alerts = EarlyWarningSignals.detect(df)

        if len(alerts):

            st.subheader(
                "Early Warning Signals"
            )

            st.dataframe(
                alerts,
                use_container_width=True,
                hide_index=True
            )
            
        if "mob" in df.columns:

            vintage = VintageAnalysis.build(df)

            fig = px.line(
                vintage,
                x="mob",
                y="bad_rate",
                markers=True,
                title="Vintage Curve"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )
            
            
                     
# =====================================================
# TAB 5
# =====================================================

with tab5:

    status = RegulatoryMonitor.rag(
        psi=0.05,
        avg_pd=summary["avg_pd"]
    )

    if status == "GREEN":
        st.success(
            "Portfolio within approved thresholds."
        )

    elif status == "AMBER":
        st.warning(
            "Portfolio requires closer monitoring."
        )

    else:
        st.error(
            "Immediate review recommended."
        )
        
    breaches = ThresholdMonitor.evaluate({
        "psi":0.05,
        "avg_pd":summary["avg_pd"],
        "default_rate":summary["default_rate"]
    })

    if breaches:

        for item in breaches:
            st.error(item)

    else:
        st.success(
            "No threshold breaches."
        )
            
                     
# =====================================================
# TAB 6
# =====================================================

with tab6:

    st.subheader(
        "Portfolio Dataset Explorer"
    )

    search = st.text_input(
        "Search Column"
    )

    display_df = df.copy()

    if search:

        cols = [
            c for c in df.columns
            if search.lower() in c.lower()
        ]

        if cols:
            display_df = df[cols]

    st.dataframe(
        display_df,
        use_container_width=True,
        height=700
    )


# =====================================================
# EXECUTIVE VIEW
# =====================================================

st.divider()

st.subheader(
    "Executive Portfolio Assessment"
)

if avg_pd is not None:

    if avg_pd < 5:

        st.success(
            """
            Portfolio currently demonstrates
            strong credit quality and low
            default risk exposure.
            """
        )

    elif avg_pd < 15:

        st.warning(
            """
            Portfolio exhibits moderate
            risk concentration and should
            be monitored closely.
            """
        )

    else:

        st.error(
            """
            Elevated portfolio risk detected.
            Immediate monitoring and
            remediation recommended.
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
    "📥 Download Monitoring Summary",
    data=str(summary),
    file_name="portfolio_monitoring_summary.csv"
)

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Bank of Baroda • Enterprise Explainable Credit Risk Factory • Portfolio Monitoring"
)