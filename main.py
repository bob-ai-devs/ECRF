import streamlit as st

pg = st.navigation({
    "🧭 Navigator": [
        st.Page(
            "app.py",
            title="Home",
            icon="🏦"
        ),

        st.Page(
            "pages/01_Data_Factory.py",
            title="Data Factory",
            icon="📊"
        ),

        st.Page(
            "pages/02_Scorecard_Factory.py",
            title="Scorecard Factory",
            icon="🎯"
        ),

        st.Page(
            "pages/03_PD_Modeling.py",
            title="PD Modeling",
            icon="📈"
        ),

        st.Page(
            "pages/04_XAI_Lab.py",
            title="XAI Lab",
            icon="🧠"
        ),

        st.Page(
            "pages/05_Reject_Inference.py",
            title="Reject Inference",
            icon="🚫"
        ),

        st.Page(
            "pages/06_Portfolio_Monitor.py",
            title="Portfolio Monitor",
            icon="📉"
        ),

        st.Page(
            "pages/07_CLV_ECL.py",
            title="CLV / ECL",
            icon="💰"
        ),

        st.Page(
            "pages/08_Digital_Twin.py",
            title="Digital Twin",
            icon="👤"
        ),

        st.Page(
            "pages/09_Gemini_Copilot.py",
            title="Gemini Copilot",
            icon="🤖"
        ),

        st.Page(
            "pages/10_Model_Governance.py",
            title="Model Governance",
            icon="🛡️"
        )
    ]
})

pg.run()