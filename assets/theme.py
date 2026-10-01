import streamlit as st

def apply_bob_theme():

    st.markdown("""
    <style>

    /* ==================================================
       BANK OF BARODA COLOR PALETTE
    ================================================== */

    :root{
        --bob-primary:#D04A02;
        --bob-primary-dark:#B53F00;
        --bob-accent:#F7A600;
        --bob-bg:#F8F9FB;
        --bob-card:#FFFFFF;
        --bob-text:#1F2937;
        --bob-border:#E5E7EB;
    }

    /* ==================================================
       GLOBAL
    ================================================== */

    .stApp{
        background-color:var(--bob-bg);
    }

    .main .block-container{
        max-width:95%;
        padding-top:1rem;
        padding-bottom:2rem;
    }

    /* ==================================================
       SIDEBAR
    ================================================== */

    [data-testid="stSidebar"]{
        background:linear-gradient(
            180deg,
            #004AD2 0%,
            #B53F00 100%
        );
    }

    /* Sidebar labels */

    [data-testid="stSidebar"] label{
        color:white !important;
        font-weight:600;
    }

    /* Sidebar text */

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4{
        color:white !important;
    }

    /* ==================================================
       SELECTBOX FIX
    ================================================== */

    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div{
        background:white !important;
        color:black !important;
        border-radius:8px;
    }

    [data-testid="stSidebar"] .stSelectbox span{
        color:black !important;
    }

    [data-testid="stSidebar"] .stNumberInput input{
        color:black !important;
        background:white !important;
    }

    [data-testid="stSidebar"] .stTextInput input{
        color:black !important;
        background:white !important;
    }

    div[role="listbox"]{
        background:white !important;
    }

    div[role="option"]{
        color:black !important;
    }

    div[role="option"]:hover{
        background:#D04A02 !important;
        color:white !important;
    }

    /* ==================================================
       HEADERS
    ================================================== */

    h1{
        color:#D04A02 !important;
        font-weight:800 !important;
    }

    h2,h3,h4{
        color:#D04A02 !important;
        font-weight:700 !important;
    }

    /* ==================================================
       BUTTONS
    ================================================== */

    .stButton > button{
        background:#004AD2 !important;
        color:white !important;
        border:none !important;
        border-radius:10px !important;
        font-weight:700 !important;
        width:100%;
    }

    .stButton > button:hover{
        background:#053FB0 !important;
        color:white !important;
    }

    /* ==================================================
       METRICS
    ================================================== */

    [data-testid="metric-container"]{
        background:white;
        border-left:6px solid #D04A02;
        border-radius:12px;
        padding:15px;
        box-shadow:0px 3px 10px rgba(0,0,0,0.08);
    }

    [data-testid="metric-container"] label{
        color:#D04A02 !important;
        font-weight:700 !important;
    }

    /* ==================================================
       DATAFRAMES
    ================================================== */

    .stDataFrame{
        background:white;
        border-radius:12px;
        border:1px solid #E5E7EB;
    }

    /* ==================================================
       TABS
    ================================================== */

    button[data-baseweb="tab"]{
        font-weight:700;
    }

    button[data-baseweb="tab"][aria-selected="true"]{
        color:#D04A02 !important;
        border-bottom:3px solid #D04A02 !important;
    }

    /* ==================================================
       EXPANDERS
    ================================================== */

    .streamlit-expanderHeader{
        color:#D04A02 !important;
        font-weight:700;
    }

    /* ==================================================
       ALERTS
    ================================================== */

    .stSuccess{
        border-left:6px solid #2E7D32;
    }

    .stWarning{
        border-left:6px solid #F7A600;
    }

    .stError{
        border-left:6px solid #C62828;
    }

    /* ==================================================
       CARDS
    ================================================== */

    .bob-card{
        background:white;
        border-radius:16px;
        padding:20px;
        box-shadow:0px 3px 12px rgba(0,0,0,0.08);
        margin-bottom:15px;
    }

    .bob-title{
        color:#6B7280;
        font-size:14px;
        font-weight:600;
    }

    .bob-value{
        color:#D04A02;
        font-size:30px;
        font-weight:800;
    }

    /* ==================================================
       INFO BOXES
    ================================================== */

    .stInfo{
        border-left:6px solid #004AD2;
    }

    /* ==================================================
       HR
    ================================================== */

    hr{
        border-top:2px solid #D04A02;
    }

    </style>
    """, unsafe_allow_html=True)