import streamlit as st

def initialize_session():

    defaults = {

        "portfolio_data": None,

        "scorecard_report": None,

        "pd_results": None,

        "leaderboard": None,

        "champion_model": None,

        "selected_features": None,

        "xai_results": {},

        "reject_results": None,

        "monitoring_results": None,

        "ecl_results": None,

        "digital_twins": {},

        "governance_results": None,

        "portfolio_metrics": {},

        "risk_twin": {},

        "pipeline_completed": False,
        
        "copilot_reports": None,
    }

    for k, v in defaults.items():

        if k not in st.session_state:
            st.session_state[k] = v