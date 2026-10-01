import streamlit as st
import pandas as pd

from assets.theme import apply_bob_theme

from modules.xai_engine import (
    CreditDecisionEngine,
    build_customer_story,
    generate_resolution_payload,
    AdverseActionGenerator
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
💡 Explainable AI Lab
</h2>
<p style="
color:#FFE7D6;
margin-top:5px;
margin-bottom:0;
">
Customer Explainability • Credit Decision Intelligence • Adverse Action Analysis
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

st.success(
    f"Portfolio Loaded: {len(df):,} Customers"
)

# =====================================================
# CUSTOMER SELECTION
# =====================================================

customer_id = st.selectbox(
    "Select Customer",
    sorted(df["customer_id"].unique())
)

customer = df[
    df["customer_id"] == customer_id
].iloc[0]

# =====================================================
# CUSTOMER KPIs
# =====================================================

score = customer.get(
    "credit_score",
    650
)

pd_value = customer.get(
    "predicted_pd",
    customer.get(
        "pd",
        0.10
    )
)

# =====================================================
# DECISION ENGINE
# =====================================================

decision_engine = CreditDecisionEngine()

decision = decision_engine.evaluate(
    pd_value=pd_value,
    score=score
)

# =====================================================
# KPI ROW
# =====================================================

col1,col2,col3,col4,col5,col6 = st.columns(6)

with col1:
    st.metric(
        "Customer",
        customer_id
    )

with col2:
    st.metric(
        "Credit Score",
        round(score,0)
    )

with col3:
    st.metric(
        "Predicted PD",
        f"{pd_value:.2%}"
    )

with col4:
    st.metric(
        "Decision",
        decision["decision"]
    )

with col5:
    st.metric(
        "Risk Grade",
        customer.get(
            "risk_grade",
            "N/A"
        )
    )

with col6:
    st.metric(
        "Profile Fields",
        len(customer.index)
    )

# =====================================================
# DECISION BANNER
# =====================================================

if decision["decision"] == "APPROVE":

    st.success(
        f"✅ APPROVE | {decision['reason']}"
    )

elif decision["decision"] == "REVIEW":

    st.warning(
        f"⚠ REVIEW | {decision['reason']}"
    )

else:

    st.error(
        f"❌ REJECT | {decision['reason']}"
    )

if pd_value < 0.05:

    st.success(
        "Risk Category: LOW"
    )

elif pd_value < 0.15:

    st.warning(
        "Risk Category: MODERATE"
    )

else:

    st.error(
        "Risk Category: HIGH"
    )

# =====================================================
# BUILD RISK DRIVERS
# =====================================================

risk_features = []

candidate_cols = [
    "credit_utilization",
    "delinquencies",
    "bureau_score",
    "income",
    "loan_amount"
]

for col in candidate_cols:

    if col in customer.index:

        try:

            risk_features.append(
                {
                    "feature": col,
                    "impact": float(customer[col])
                }
            )

        except:
            pass

if len(risk_features) == 0:

    risk_features = [
        {
            "feature": "bureau_score",
            "impact": 1
        }
    ]

shap_df = pd.DataFrame(
    risk_features
)

display_shap_df = shap_df.rename(
    columns={
        "feature":"Feature",
        "impact":"Impact"
    }
)

# =====================================================
# ADVERSE ACTIONS
# =====================================================

adverse_engine = (
    AdverseActionGenerator()
)

adverse_actions = (
    adverse_engine.generate(
        shap_df
    )
)

# =====================================================
# RESOLUTION PAYLOAD
# =====================================================

resolution = (
    generate_resolution_payload(
        customer=customer,
        decision=decision,
        shap_df=shap_df
    )
)

resolution_df = pd.DataFrame(
    [resolution]
)

# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        "Customer 360",
        "Decision Analysis",
        "Risk Drivers",
        "Adverse Actions",
        "Recommendations",
        "Resolution Payload"
    ]
)

# =====================================================
# TAB 1
# =====================================================

with tab1:

    st.subheader(
        "Customer 360 View"
    )

    profile_df = pd.DataFrame(
        {
            "Attribute": customer.index,
            "Value": customer.values
        }
    )

    st.dataframe(
        profile_df,
        use_container_width=True,
        hide_index=True
    )

# =====================================================
# TAB 2
# =====================================================

with tab2:

    st.subheader(
        "Decision Analysis"
    )

    story = build_customer_story(
        customer.to_dict()
    )

    st.info(story)

    st.markdown(
        f"""
### Decision Summary

**Decision:** {decision['decision']}

**Reason:** {decision['reason']}

**Predicted PD:** {pd_value:.2%}

**Credit Score:** {score:.0f}
"""
    )

# =====================================================
# TAB 3
# =====================================================

with tab3:

    st.subheader(
        "Risk Driver Analysis"
    )

    st.dataframe(
        display_shap_df,
        use_container_width=True,
        hide_index=True
    )

    st.bar_chart(
        display_shap_df.set_index(
            "Feature"
        )
    )

# =====================================================
# TAB 4
# =====================================================

with tab4:

    st.subheader(
        "Adverse Action Analysis"
    )

    if len(adverse_actions):

        for item in adverse_actions:

            st.error(item)

    else:

        st.success(
            "No adverse factors detected."
        )

# =====================================================
# TAB 5
# =====================================================

with tab5:

    st.subheader(
        "Customer Action Plan"
    )

    recommendations = []

    if pd_value > 0.15:

        recommendations.append(
            "High risk profile requires review"
        )

    if (
        "credit_utilization"
        in customer.index
        and
        customer["credit_utilization"] > 0.50
    ):

        recommendations.append(
            "Reduce credit utilization"
        )

    if (
        "bureau_score"
        in customer.index
        and
        customer["bureau_score"] < 700
    ):

        recommendations.append(
            "Improve bureau score"
        )

    if len(recommendations) == 0:

        recommendations.append(
            "Customer profile is strong"
        )

    for rec in recommendations:

        st.success(rec)

# =====================================================
# TAB 6
# =====================================================

with tab6:

    st.subheader(
        "Resolution Payload"
    )

    st.dataframe(
        resolution_df,
        use_container_width=True,
        hide_index=True
    )

# =====================================================
# EXECUTIVE XAI ASSESSMENT
# =====================================================

st.divider()

st.subheader(
    "Executive XAI Assessment"
)

st.info(
    f"""
Customer {customer_id} has a predicted
probability of default of {pd_value:.2%}.

Decision Recommendation:
{decision['decision']}

Primary risk drivers are shown
in the Risk Driver Analysis section.

This explanation package supports
customer servicing, audit review,
and decision transparency.
"""
)

# =====================================================
# EXPORT
# =====================================================

st.divider()

st.subheader(
    "Export Explainability Report"
)

st.download_button(
    "📥 Download Resolution Report",
    data=resolution_df.to_csv(
        index=False
    ),
    file_name=f"xai_customer_{customer_id}.csv",
    mime="text/csv"
)

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Bank of Baroda • Enterprise Explainable Credit Risk Factory • Explainable AI Lab"
)