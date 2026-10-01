import streamlit as st

from config import *

from services.session_manager import (
    initialize_session
)

from services.workflow_engine import (
    WorkflowEngine
)

from modules.data_factory import (
    generate_credit_data
)
from assets.theme import apply_bob_theme

from modules.model_governance import ModelInventory

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_bob_theme()

# =====================================================
# SESSION INIT
# =====================================================

initialize_session()

# =====================================================
# HEADER
# =====================================================

# st.title(
#     "🏦 Enterprise Explainable Credit Risk Factory"
# )

st.markdown(f"""
<div style="
background:linear-gradient(90deg,#703A00,#00509E);
padding:25px;
border-radius:15px;
margin-bottom:15px;
">
<h1 style="color:white;margin:0;">
🏦 Enterprise Explainable Credit Risk Factory
</h1>
<p style="color:#FFE7D6;">
{BANK_NAME} | Credit Risk Intelligence Platform
</p>
</div>
""", unsafe_allow_html=True)

def kpi_card(title,value):

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">
            {title}
        </div>
        <div class="metric-value">
            {value}
        </div>
    </div>
    """, unsafe_allow_html=True)

st.caption(
    f"{BANK_NAME} | Version {APP_VERSION}"
)

with st.expander("Credit Risk Operating System"):
    st.markdown(
    """
    ### Credit Risk Operating System

    An integrated AI platform for:

    - Scorecard Development
    - Probability of Default Modeling
    - Explainable AI
    - Reject Inference
    - Portfolio Monitoring
    - CLV / ECL Analytics
    - IFRS9 Staging
    - Stress Testing
    - Customer Digital Twin
    - AI Governance
    - Gemini Risk Copilot
    """
    )

# =====================================================
# SIDEBAR
# =====================================================

if "customers" not in st.session_state:
    st.session_state.customers = DEFAULT_CUSTOMERS
   
if "seed" not in st.session_state:
    st.session_state.seed = 42
    
if "selected_portfolio" not in st.session_state:
    st.session_state.selected_portfolio = "Retail"

with st.sidebar:

    st.header("Portfolio Generator")

    st.session_state.selected_portfolio = st.selectbox(
        "Portfolio Type",
        PORTFOLIO_TYPES,
        index=PORTFOLIO_TYPES.index(st.session_state.selected_portfolio)
    )

    st.session_state.customers = st.slider(
        "Customers",
        min_value=100,
        max_value=MAX_CUSTOMERS,
        value=st.session_state.customers,
        step=1
    )

    st.session_state.seed = st.number_input(
        "Random Seed",
        value=st.session_state.seed
    )

    # st.session_state.selected_portfolio = portfolio_type
    portfolio_type = st.session_state.selected_portfolio
    st.session_state.customer_count = st.session_state.customers
    customers = st.session_state.customers
    # st.session_state.seed = seed
    seed = st.session_state.seed

    st.divider()

    # =============================================
    # GENERATE PORTFOLIO
    # =============================================

    if st.button(
        "Generate Portfolio",
        use_container_width=True
    ):

        with st.spinner(
            "Generating synthetic portfolio..."
        ):

            df = generate_credit_data(
                n_customers=customers,
                seed=seed,
                portfolio_type=portfolio_type
            )
            
            df.index += 1

            st.session_state.portfolio_data = df

            # Reset downstream results

            st.session_state.pipeline_completed = False
            st.session_state.leaderboard = None
            st.session_state.champion_model = None
            st.session_state.champion_name = None
            st.session_state.digital_twins = {}
            st.session_state.portfolio_metrics = {}
            st.session_state.scorecard_report = None
            st.session_state.xai_results = {}

        st.success(
            f"{len(df):,} customers generated"
        )

    st.divider()

    # =============================================
    # PIPELINE
    # =============================================

    # if st.button(
    #     "🚀 Run Full ECRF Pipeline",
    #     type="primary",
    #     use_container_width=True
    # ):

    #     if st.session_state.portfolio_data is None:

    #         st.error(
    #             "Generate portfolio first."
    #         )

    #     else:

    #         with st.spinner(
    #             "Running Enterprise Risk Factory..."
    #         ):

    #             results = WorkflowEngine.run(
    #                 st.session_state.portfolio_data
    #             )

    #             st.session_state.portfolio_data = (
    #                 results["data"]
    #             )

    #             st.session_state.leaderboard = (
    #                 results.get("leaderboard")
    #             )
                
    #             st.session_state.leaderboard.index += 1

    #             st.session_state.champion_model = (
    #                 results.get("champion_model")
    #             )

    #             st.session_state.champion_name = (
    #                 results.get("champion_name")
    #             )

    #             st.session_state.digital_twins = (
    #                 results.get(
    #                     "digital_twins",
    #                     {}
    #                 )
    #             )

    #             st.session_state.portfolio_metrics = (
    #                 results.get(
    #                     "metrics",
    #                     {}
    #                 )
    #             )

    #             st.session_state.pipeline_completed = True

    #         st.success(
    #             "Pipeline Completed Successfully"
    #         )
    
    
    if st.button(
        "🚀 Run Full ECRF Pipeline",
        type="primary",
        use_container_width=True
    ):

        if st.session_state.portfolio_data is None:

            st.error(
                "Generate portfolio first."
            )

        else:

            with st.spinner(
                "Running Enterprise Risk Factory..."
            ):

                results = WorkflowEngine.run(
                    st.session_state.portfolio_data
                )

                # =========================
                # CORE OUTPUTS
                # =========================
                st.session_state.portfolio_data = results["data"]

                st.session_state.leaderboard = results.get("leaderboard")

                if st.session_state.leaderboard is not None:
                    st.session_state.leaderboard.index += 1

                st.session_state.champion_model = results.get("champion_model")
                st.session_state.champion_name = results.get("champion_name")

                st.session_state.digital_twins = results.get("digital_twins", {})
                st.session_state.portfolio_metrics = results.get("metrics", {})

                # =========================
                # ✅ MODEL INVENTORY FIX
                # =========================
                inventory = ModelInventory()

                inventory.register(
                    model_name=st.session_state.champion_name or "CreditScoreModel",
                    version="v1",
                    owner="RiskTeam",
                    purpose="Credit Risk Scoring",
                    champion=True
                )

                st.session_state.model_inventory = inventory.get_inventory()

                # =========================
                # PIPELINE FLAG
                # =========================
                st.session_state.pipeline_completed = True

            st.success(
                "Pipeline Completed Successfully"
            )

    st.divider()

    st.subheader(
        "Platform Status"
    )

    if st.session_state.pipeline_completed:

        st.success(
            "Pipeline Ready"
        )

    elif st.session_state.portfolio_data is not None:

        st.warning(
            "Portfolio Generated"
        )

    else:

        st.info(
            "Waiting For Data"
        )
        
        


# =====================================================
# WORKFLOW STAGE
# =====================================================

current_stage = (
    "Pipeline Complete"
    if st.session_state.pipeline_completed
    else "Data Generation"
)

st.info(
    f"Current Workflow Stage: {current_stage}"
)

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "Module Readiness",
        "Platform Capability Matrix & Executive Command Center",
        "Champion Challenger",
        "Portfolio Overview",
        "Open Modules & Recommended Workflow",
    ]
)


with tab2:
    st.subheader(
        "Platform Capability Matrix"
    )

    cap1, cap2, cap3 = st.columns(3)

    with cap1:

        st.markdown("""
        **Credit Risk**

        - Scorecards
        - PD Modeling
        - Reject Inference
        - Portfolio Monitoring
        """)

    with cap2:

        st.markdown("""
        **Explainability**

        - SHAP
        - LIME
        - STEDCAM
        - Governance
        """)

    with cap3:

        st.markdown("""
        **Intelligence**

        - Digital Twin
        - CLV / ECL
        - Gemini Copilot
        - Stress Testing
        """)

    # =====================================================
    # EXECUTIVE COMMAND CENTER
    # =====================================================

    if (
        st.session_state.pipeline_completed
        and
        st.session_state.portfolio_metrics
    ):

        metrics = (
            st.session_state.portfolio_metrics
        )

        st.subheader(
            "Executive Command Center"
        )

        avg_score = metrics.get(
            "avg_score",
            0
        )

        avg_pd = metrics.get(
            "avg_pd",
            0
        )

        default_rate = metrics.get(
            "default_rate",
            0
        )

        customers = metrics.get(
            "customers",
            0
        )

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "Customers",
                f"{customers:,}"
            )

        with c2:
            st.metric(
                "Average Score",
                round(avg_score,0)
            )

        with c3:
            st.metric(
                "Average PD",
                f"{avg_pd:.2%}"
            )

        with c4:
            st.metric(
                "Default Rate",
                f"{default_rate:.2%}"
            )

        st.divider()

        if avg_pd < 0.05:

            st.success(
                """
                Portfolio exhibits strong
                credit quality with limited
                risk concentration.
                """
            )

        elif avg_pd < 0.15:

            st.warning(
                """
                Moderate portfolio risk
                detected. Continued monitoring
                recommended.
                """
            )

        else:

            st.error(
                """
                Elevated portfolio risk.
                Management intervention may
                be required.
                """
            )

# =====================================================
# CHAMPION MODEL
# =====================================================

# if st.session_state.champion_model is not None:

#     st.success(
#         f"Champion Model : "
#         f"{st.session_state.champion_name}"
#     )

# =====================================================
# MODEL PERFORMANCE CENTER
# =====================================================

with tab3:
    if st.session_state.leaderboard is not None:

        st.subheader(
            "Champion Challenger Arena"
        )

        c1, c2 = st.columns([1,2])

        with c1:

            st.success(
                f"""
                Champion Model

                {st.session_state.champion_name}
                """
            )

        with c2:

            st.dataframe(
                st.session_state.leaderboard,
                use_container_width=True,
                hide_index=True
            )

# =====================================================
# PORTFOLIO PREVIEW
# =====================================================

with tab4:
    if st.session_state.portfolio_data is not None:

        df = st.session_state.portfolio_data

        st.subheader(
            "Portfolio Overview"
        )

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Records",
            len(df)
        )

        c2.metric(
            "Columns",
            len(df.columns)
        )

        if "default_flag" in df.columns:

            c3.metric(
                "Defaults",
                int(
                    df["default_flag"].sum()
                )
            )

        with st.expander(
            "Portfolio Data Preview"
        ):

            st.dataframe(
                df.head(20),
                use_container_width=True
            )

# =====================================================
# MODULE STATUS
# =====================================================

with tab1:
    st.subheader(
        "Module Readiness"
    )

    module_status = {

        "Data Factory":
            st.session_state.portfolio_data is not None,

        "Scorecard Factory":
            st.session_state.portfolio_data is not None,

        "PD Modeling":
            st.session_state.champion_model is not None,

        "XAI Lab":
            st.session_state.champion_model is not None,

        "Reject Inference":
            st.session_state.champion_model is not None,

        "Portfolio Monitor":
            st.session_state.pipeline_completed,

        "CLV / ECL":
            st.session_state.pipeline_completed,

        "Digital Twin":
            len(
                st.session_state.digital_twins
            ) > 0,

        "Gemini Copilot":
            st.session_state.pipeline_completed,

        "Model Governance":
            st.session_state.pipeline_completed
    }
    

    
    status_df = st.dataframe(
        {
            "Module": module_status.keys(),
            "Status": [
                "🟢 Ready"
                if v
                else "🔴 Not Ready"
                for v in module_status.values()
            ]
        }, hide_index=True
    )


# =====================================================
# NAVIGATION
# =====================================================

with tab5:
    st.subheader(
        "Open Modules"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.page_link(
            "pages/01_Data_Factory.py",
            label="📊 Data Factory"
        )

        st.page_link(
            "pages/02_Scorecard_Factory.py",
            label="🎯 Scorecard Factory"
        )

        st.page_link(
            "pages/03_PD_Modeling.py",
            label="📈 PD Modeling"
        )

        st.page_link(
            "pages/04_XAI_Lab.py",
            label="🧠 XAI Lab"
        )

        st.page_link(
            "pages/05_Reject_Inference.py",
            label="🚫 Reject Inference"
        )

    with col2:

        st.page_link(
            "pages/06_Portfolio_Monitor.py",
            label="📉 Portfolio Monitor"
        )

        st.page_link(
            "pages/07_CLV_ECL.py",
            label="💰 CLV / ECL"
        )

        st.page_link(
            "pages/08_Digital_Twin.py",
            label="👤 Digital Twin"
        )

        st.page_link(
            "pages/09_Gemini_Copilot.py",
            label="🤖 Gemini Copilot"
        )

        st.page_link(
            "pages/10_Model_Governance.py",
            label="🛡️ Model Governance"
        )

    # =====================================================
    # WORKFLOW
    # =====================================================

    with st.expander("Recommended Workflow"):
        st.subheader(
            "Recommended Workflow"
        )

        st.markdown(
        """
        1. Generate Portfolio

        2. Scorecard Factory

        3. PD Modeling

        4. XAI Lab

        5. Reject Inference

        6. Portfolio Monitoring

        7. CLV / ECL

        8. Digital Twin

        9. Gemini Copilot

        10. Model Governance
        """
        )

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Enterprise Explainable Credit Risk Factory (ECRF) | AI Risk Platform"
)

