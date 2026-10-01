import streamlit as st
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from xgboost import XGBClassifier

import shap

import plotly.express as px
import plotly.graph_objects as go

from scipy.stats import entropy

st.set_page_config(
    page_title="Enterprise Explainable Credit Risk Factory",
    layout="wide"
)

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("Synthetic Data Generator")

num_customers = st.sidebar.slider(
    "Number of Customers",
    1000,
    50000,
    5000,
    1000
)

seed = st.sidebar.number_input(
    "Random Seed",
    value=42
)

portfolio_type = st.sidebar.selectbox(
    "Portfolio Type",
    [
        "Retail",
        "MSME",
        "Credit Card",
        "Vehicle Loan",
        "Mixed"
    ]
)

generate = st.sidebar.button("Generate Portfolio")

# =====================================================
# DATA GENERATION
# =====================================================

def generate_synthetic_data(n, seed):

    np.random.seed(seed)

    df = pd.DataFrame()

    df["customer_id"] = np.arange(1, n + 1)

    df["age"] = np.random.randint(21, 70, n)

    df["income"] = np.random.normal(
        800000,
        250000,
        n
    ).clip(100000)

    df["utilization"] = np.random.uniform(
        0,
        1,
        n
    )

    df["delinquencies"] = np.random.poisson(
        1,
        n
    )

    df["loan_amount"] = np.random.normal(
        500000,
        200000,
        n
    ).clip(50000)

    df["account_balance"] = np.random.normal(
        150000,
        80000,
        n
    ).clip(0)

    df["salary_volatility"] = np.random.uniform(
        0,
        1,
        n
    )

    risk_score = (
        2.5 * df["utilization"]
        + 0.8 * df["delinquencies"]
        + 1.5 * df["salary_volatility"]
        - 0.000001 * df["income"]
    )

    prob_default = 1 / (
        1 + np.exp(-risk_score)
    )

    df["default"] = np.random.binomial(
        1,
        prob_default
    )

    return df


# =====================================================
# SESSION STATE
# =====================================================

if generate or "portfolio" not in st.session_state:

    st.session_state.portfolio = generate_synthetic_data(
        num_customers,
        seed
    )

# =====================================================
# DATA
# =====================================================

df = st.session_state.portfolio

# =====================================================
# MODEL TRAINING
# =====================================================

features = [
    "age",
    "income",
    "utilization",
    "delinquencies",
    "loan_amount",
    "account_balance",
    "salary_volatility"
]

X = df[features]
y = df["default"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = XGBClassifier(
    n_estimators=100,
    max_depth=4,
    learning_rate=0.05,
    eval_metric="logloss"
)

model.fit(X_train, y_train)

pred_prob = model.predict_proba(X)[:, 1]

df["pd"] = pred_prob

df["credit_score"] = (
    900 - (pred_prob * 600)
).astype(int)

# =====================================================
# RISK GRADE
# =====================================================

def grade(score):

    if score >= 800:
        return "A"

    elif score >= 700:
        return "B"

    elif score >= 600:
        return "C"

    return "D"


df["risk_grade"] = df["credit_score"].apply(
    grade
)

# =====================================================
# MAIN HEADER
# =====================================================

st.title(
    "Enterprise Explainable Credit Risk Factory (ECRF)"
)

# =====================================================
# KPI SECTION
# =====================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Customers",
    len(df)
)

col2.metric(
    "Avg Credit Score",
    round(df["credit_score"].mean())
)

col3.metric(
    "Avg PD",
    f"{df['pd'].mean()*100:.2f}%"
)

col4.metric(
    "Observed Default Rate",
    f"{df['default'].mean()*100:.2f}%"
)

# =====================================================
# TABS
# =====================================================

tabs = st.tabs([
    "Portfolio",
    "Risk Segmentation",
    "Explainability",
    "Migration",
    "PSI Monitor",
    "Customer Digital Twin"
])

# =====================================================
# TAB 1
# =====================================================

with tabs[0]:

    st.subheader("Portfolio Risk Distribution")

    fig = px.histogram(
        df,
        x="credit_score",
        nbins=40
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# TAB 2
# =====================================================

with tabs[1]:

    st.subheader("Risk Grades")

    grade_df = (
        df["risk_grade"]
        .value_counts()
        .reset_index()
    )

    fig = px.pie(
        grade_df,
        names="risk_grade",
        values="count"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# TAB 3
# =====================================================

with tabs[2]:

    st.subheader("SHAP Explainability")

    sample_size = min(
        500,
        len(X_test)
    )

    sample = X_test.sample(
        sample_size,
        random_state=42
    )

    explainer = shap.TreeExplainer(model)

    shap_values = explainer.shap_values(
        sample
    )

    importance = pd.DataFrame({
        "Feature": sample.columns,
        "Importance":
            np.abs(shap_values).mean(axis=0)
    })

    importance = importance.sort_values(
        "Importance",
        ascending=False
    )

    fig = px.bar(
        importance,
        x="Feature",
        y="Importance"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# TAB 4
# =====================================================

with tabs[3]:

    st.subheader("Score Migration")

    df["old_score"] = (
        df["credit_score"]
        + np.random.normal(
            30,
            50,
            len(df)
        )
    ).astype(int)

    migration = (
        df["credit_score"]
        - df["old_score"]
    )

    fig = px.histogram(
        migration,
        nbins=50,
        title="Score Change"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# TAB 5
# =====================================================

with tabs[4]:

    st.subheader("Population Stability Index")

    expected = (
        df["old_score"]
        .value_counts(normalize=True)
    )

    actual = (
        df["credit_score"]
        .value_counts(normalize=True)
    )

    bins = np.arange(
        300,
        901,
        50
    )

    expected_hist = np.histogram(
        df["old_score"],
        bins=bins
    )[0]

    actual_hist = np.histogram(
        df["credit_score"],
        bins=bins
    )[0]

    expected_pct = (
        expected_hist
        / expected_hist.sum()
        + 1e-6
    )

    actual_pct = (
        actual_hist
        / actual_hist.sum()
        + 1e-6
    )

    psi = np.sum(
        (
            actual_pct - expected_pct
        ) *
        np.log(
            actual_pct / expected_pct
        )
    )

    st.metric(
        "PSI",
        round(psi, 4)
    )

    if psi < 0.1:
        st.success("Stable Population")

    elif psi < 0.25:
        st.warning("Moderate Shift")

    else:
        st.error("Significant Drift")

# =====================================================
# TAB 6
# =====================================================

with tabs[5]:

    st.subheader("Customer Risk Digital Twin")

    cid = st.selectbox(
        "Customer",
        df["customer_id"]
    )

    row = df[
        df["customer_id"] == cid
    ].iloc[0]

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Credit Score",
        row["credit_score"]
    )

    c2.metric(
        "PD",
        f"{row['pd']*100:.2f}%"
    )

    c3.metric(
        "Risk Grade",
        row["risk_grade"]
    )

    st.dataframe(
        row.to_frame()
        .reset_index()
        .rename(
            columns={
                "index": "Attribute",
                0: "Value"
            }
        ),
        use_container_width=True
    )

# =====================================================
# MODEL PERFORMANCE
# =====================================================

auc = roc_auc_score(
    y_test,
    model.predict_proba(X_test)[:, 1]
)

st.sidebar.success(
    f"AUC = {auc:.4f}"
)