import streamlit as st
import pandas as pd

from assets.theme import apply_bob_theme

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
📊 Enterprise Data Factory
</h2>
<p style="
color:#FFE7D6;
margin-top:5px;
margin-bottom:0;
">
Portfolio Analytics • Data Quality • Synthetic Credit Data
</p>
</div>
""",
unsafe_allow_html=True)

# =====================================================
# CHECK DATA
# =====================================================

if st.session_state.portfolio_data is None:

    st.warning(
        "Generate portfolio from Home page first."
    )

    st.stop()

df = st.session_state.portfolio_data

# =====================================================
# KPI SECTION
# =====================================================

total_expected_loss = (
    df["expected_loss"].sum()
    if "expected_loss" in df.columns
    else 0
)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Customers",
        f"{len(df):,}"
    )

with col2:
    st.metric(
        "Features",
        len(df.columns)
    )

with col3:

    if "default_flag" in df.columns:

        st.metric(
            "Defaults",
            int(df["default_flag"].sum())
        )

    elif "default" in df.columns:

        st.metric(
            "Defaults",
            int(df["default"].sum())
        )

    else:

        st.metric(
            "Defaults",
            "N/A"
        )

with col4:

    completeness = (
        100 -
        (df.isna().mean().mean() * 100)
    )

    st.metric(
        "Completeness",
        f"{completeness:.1f}%"
    )
    
with col5:

    st.metric(
        "Expected Loss",
        f"₹{total_expected_loss:,.0f}"
    )

# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        "Portfolio Analytics",
        "Data Quality",
        "Risk Intelligence",
        "Customer Segments",
        "Scenario Lab",
        "Preview"
    ]
)

# =====================================================
# TAB 1
# =====================================================

with tab1:

    st.subheader(
        "Portfolio Analytics"
    )

    numeric_cols = (
        df.select_dtypes(
            include=["number"]
        )
        .columns
        .tolist()
    )

    if len(numeric_cols) > 0:

        selected_col = st.selectbox(
            "Select Numeric Variable",
            numeric_cols
        )

        st.write(
            f"Distribution of {selected_col}"
        )

        st.bar_chart(
            df[selected_col]
            .value_counts()
            .head(25)
        )

        st.write(
            df[selected_col]
            .describe()
        )

    else:

        st.info(
            "No numeric columns available."
        )

# =====================================================
# TAB 2
# =====================================================

with tab2:

    st.subheader(
        "Data Quality Dashboard"
    )

    quality = pd.DataFrame({

        "Column":
            df.columns,

        "Missing Count":
            df.isna().sum().values,

        "Missing %":
            (
                df.isna().mean()
                .values * 100
            ).round(2)

    })

    st.dataframe(
        quality,
        use_container_width=True,
        hide_index=True
    )

    st.metric(
        "Total Missing Values",
        int(df.isna().sum().sum())
    )

# =====================================================
# TAB 3
# =====================================================

with tab3:

    st.subheader(
        "Risk Intelligence"
    )

    if "risk_band" in df.columns:

        risk_summary = (
            df["risk_band"]
            .value_counts()
        )

        st.bar_chart(
            risk_summary
        )

        st.dataframe(
            risk_summary.reset_index(),
            use_container_width=True,
            hide_index=True
        )

    if "expected_loss" in df.columns:

        st.subheader(
            "Expected Loss Distribution"
        )

        st.bar_chart(
            df["expected_loss"]
        )

# =====================================================
# TAB 4
# =====================================================

with tab4:

    st.subheader(
        "Customer Segmentation"
    )

    if "customer_segment" in df.columns:

        segment_summary = (
            df["customer_segment"]
            .value_counts()
        )

        st.bar_chart(
            segment_summary
        )

        st.dataframe(
            segment_summary.reset_index(),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "Customer segments unavailable."
        )

# =====================================================
# TAB 5
# =====================================================

with tab5:

    st.subheader(
        "Macroeconomic Scenario Lab"
    )

    if st.button(
        "Generate Scenario"
    ):

        scenario = {

            "Repo Rate":
                round(
                    df["credit_utilization"].mean()
                    * 10,
                    2
                ),

            "Inflation":
                round(
                    df["salary_volatility"].mean()
                    * 10,
                    2
                )

            if "salary_volatility"
            in df.columns

            else "N/A"
        }

        st.dataframe(
            scenario
        )

    st.info(
        """
        Scenario generation capability
        is available in the Data Factory
        backend.
        """
    )
    
# =====================================================
# TAB 6
# =====================================================    
    
with tab6:

    st.subheader(
        "Data Explorer"
    )

    column = st.selectbox(
        "Choose Column",
        df.columns
    )

    st.write(
        f"Column Type: {df[column].dtype}"
    )

    st.write(
        df[column].describe(
            include="all"
        )
    )

    st.divider()

    st.subheader(
        "Portfolio Preview"
    )

    rows = st.slider(
        "Rows",
        min_value=10,
        max_value=min(
            len(df),
            500
        ),
        value=100
    )

    st.dataframe(
        df.head(rows),
        use_container_width=True
    )

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Bank of Baroda • Enterprise Explainable Credit Risk Factory"
)