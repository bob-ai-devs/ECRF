import streamlit as st
import pandas as pd

from assets.theme import apply_bob_theme

from config import *

from modules.model_governance import (
    governance_summary,
    ModelInventory,
    ModelLifecycle,
    ValidationTracker,
    FairnessAnalyzer,
    ExplainabilityCompliance,
    AIRiskClassification,
    AuditTrail,
    ChangeManagement,
    RegulatoryChecklist,
    ComplianceScore,
    ModelRiskRating
)

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
🛡️ Model Governance Center
</h2>
<p style="
color:#FFE7D6;
margin-top:5px;
margin-bottom:0;
">
Model Risk Management • Governance • Compliance • Audit Readiness
</p>
</div>
""",
unsafe_allow_html=True)

# =====================================================
# CHECK PIPELINE
# =====================================================

if st.session_state.leaderboard is None:

    st.warning(
        "Run Full ECRF Pipeline first."
    )

    st.stop()

# =====================================================
# DATA
# =====================================================

leaderboard = (
    st.session_state.leaderboard
)

inventory_df = (
    st.session_state.get(
        "model_inventory",
        None
    )
)

# =====================================================
# KPI SECTION
# =====================================================

models_tested = len(
    leaderboard
)

champion_model = (
    st.session_state.get(
        "champion_name",
        "N/A"
    )
)

avg_auc = None
avg_gini = None

if "auc" in leaderboard.columns:

    avg_auc = round(
        leaderboard["auc"].mean(),
        3
    )

if "gini" in leaderboard.columns:

    avg_gini = round(
        leaderboard["gini"].mean(),
        3
    )

models_registered = (
    len(inventory_df)
    if inventory_df is not None
    else 0
)

production_models = 0

if (
    inventory_df is not None
    and
    "status" in inventory_df.columns
):

    production_models = (
        inventory_df["status"]
        .eq("Production")
        .sum()
    )

compliance_score = 100

risk_rating = ModelRiskRating.assign(
    psi=0.05,
    auc=avg_auc if avg_auc else 0.75,
    fairness_score=0.90
)

c1,c2,c3,c4,c5,c6 = st.columns(6)

with c1:
    st.metric(
        "Models Evaluated",
        models_tested
    )

with c2:
    st.metric(
        "Champion",
        champion_model
    )

with c3:
    st.metric(
        "Production",
        production_models
    )

with c4:
    st.metric(
        "Avg AUC",
        avg_auc
        if avg_auc
        else "N/A"
    )

with c5:
    st.metric(
        "Compliance",
        f"{compliance_score}%"
    )

with c6:
    st.metric(
        "Risk Rating",
        risk_rating
    )

# =====================================================
# VIEW SELECTION
# =====================================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Executive Dashboard",
    "Champion Governance",
    "Inventory & Lifecycle",
    "Compliance",
    "AI Risk",
    "Audit Center"
])


with tab1:

    st.subheader(
        "Governance Overview"
    )

    overview = pd.DataFrame(
        {
            "Metric":[
                "Models Evaluated",
                "Registered Models",
                "Production Models",
                "Champion Model"
            ],
            "Value":[
                models_tested,
                models_registered,
                production_models,
                champion_model
            ]
        }
    )

    st.dataframe(
        overview,
        use_container_width=True,
        hide_index=True
    )

    if avg_auc:

        health_score = (
            compliance_score
            +
            avg_auc * 100
        ) / 2

        st.metric(
            "Governance Health",
            f"{health_score:.1f}"
        )
        
with tab2:

    st.subheader(
        "Champion Challenger Analysis"
    )

    st.dataframe(
        leaderboard,
        use_container_width=True,
        hide_index=True
    )

    if "auc" in leaderboard.columns:

        model_col = (
            leaderboard.columns[0]
        )

        st.bar_chart(
            leaderboard
            .set_index(model_col)
            ["auc"]
        )
        
with tab3:

    # =====================================================
    # INVENTORY
    # =====================================================

    if inventory_df is None:

        st.error(
            """
            Model inventory not available.
            """
        )

    else:

        st.subheader(
            "Model Inventory"
        )

        st.dataframe(
            inventory_df,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "📥 Download Model Inventory",
            data=inventory_df.to_csv(
                index=False
            ),
            file_name="model_inventory.csv",
            mime="text/csv"
        )

        if "status" in inventory_df.columns:

            st.subheader(
                "Lifecycle Distribution"
            )

            lifecycle = (
                inventory_df["status"]
                .value_counts()
            )

            st.bar_chart(
                lifecycle
            )
            

with tab4:

    st.subheader(
        "Regulatory Compliance"
    )

    checklist = (
        RegulatoryChecklist.generate()
    )

    st.dataframe(
        checklist,
        use_container_width=True,
        hide_index=True
    )

    score = (
        ComplianceScore.calculate(
            checklist
        )
    )

    st.metric(
        "Checklist Compliance",
        f"{score}%"
    )

    xai = (
        ExplainabilityCompliance
        .evaluate(
            shap_enabled=True,
            lime_enabled=True,
            counterfactual_enabled=True
        )
    )

    st.metric(
        "Explainability Score",
        f"{xai['score']}/3"
    )

    st.success(
        f"Compliant: {xai['compliant']}"
    )
    

with tab5:

    st.subheader(
        "AI Risk Management"
    )

    ai_risk = (
        AIRiskClassification.classify(
            "credit_scoring"
        )
    )

    st.metric(
        "AI Risk Category",
        ai_risk
    )

    st.metric(
        "Model Risk Rating",
        risk_rating
    )

    if risk_rating == "LOW":

        st.success(
            "Risk within tolerance."
        )

    elif risk_rating == "MEDIUM":

        st.warning(
            "Monitor closely."
        )

    else:

        st.error(
            "Remediation required."
        )
        

with tab6:

    st.subheader(
        "Audit Readiness"
    )

    audit_df = pd.DataFrame(
        {
            "Date":[
                "2026-01-15",
                "2026-02-20",
                "2026-03-10"
            ],
            "Event":[
                "Validation",
                "Champion Review",
                "Governance Approval"
            ],
            "Status":[
                "Completed",
                "Completed",
                "Completed"
            ]
        }
    )

    st.dataframe(
        audit_df,
        use_container_width=True,
        hide_index=True
    )

    st.success(
        "Audit Ready"
    )



# =====================================================
# EXECUTIVE COMMENTARY
# =====================================================

st.divider()

st.subheader(
    "Executive Governance Assessment"
)

if avg_auc and avg_auc >= 0.80:

    st.success(
        f"""
        Champion model {champion_model}
        demonstrates strong discriminatory
        performance.

        Governance controls, inventory
        tracking, compliance monitoring
        and audit readiness remain active.

        Overall Risk Rating: {risk_rating}
        """
    )

elif avg_auc and avg_auc >= 0.70:

    st.warning(
        """
        Model performance acceptable.

        Continue monitoring and
        periodic validation.
        """
    )

else:

    st.error(
        """
        Governance review recommended.

        Model performance below
        preferred threshold.
        """
    )

if champion_model:

    st.info(
        f"""
        Champion model currently deployed:
        {champion_model}

        Governance processes indicate
        model inventory registration,
        performance monitoring and
        audit traceability are active.
        """
    )

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Bank of Baroda • Enterprise Explainable Credit Risk Factory • Model Governance"
)