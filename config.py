"""
Enterprise Explainable Credit Risk Factory
Global Configuration
"""

from pathlib import Path
import streamlit as st

# ==================================================
# PROJECT PATHS
# ==================================================

ROOT_DIR = Path(__file__).resolve().parent

DATA_DIR = ROOT_DIR / "data"
MODEL_DIR = ROOT_DIR / "models"
REPORT_DIR = ROOT_DIR / "reports"
ASSET_DIR = ROOT_DIR / "assets"
CACHE_DIR = ROOT_DIR / "cache"

for directory in [
    DATA_DIR,
    MODEL_DIR,
    REPORT_DIR,
    ASSET_DIR,
    CACHE_DIR
]:
    directory.mkdir(exist_ok=True)

# ==================================================
# APP INFO
# ==================================================

APP_NAME = "Enterprise Explainable Credit Risk Factory"

APP_VERSION = "1.0"

BANK_NAME = "Bank of Baroda"

# ==================================================
# MODEL SETTINGS
# ==================================================

RANDOM_STATE = 42

TEST_SIZE = 0.20

TARGET_COLUMN = "default"

# ==================================================
# SCORE SETTINGS
# ==================================================

MAX_SCORE = 900

MIN_SCORE = 300

# ==================================================
# RISK GRADES
# ==================================================

RISK_GRADES = {
    "A+": (850, 900),
    "A": (800, 849),
    "B": (700, 799),
    "C": (600, 699),
    "D": (500, 599),
    "E": (300, 499)
}

# ==================================================
# PSI THRESHOLDS
# ==================================================

PSI_THRESHOLDS = {
    "stable": 0.10,
    "warning": 0.25
}

# ==================================================
# PD THRESHOLDS
# ==================================================

PD_THRESHOLDS = {
    "low": 0.05,
    "medium": 0.15,
    "high": 0.30
}

# ==================================================
# XAI SETTINGS
# ==================================================

SHAP_SAMPLE_SIZE = 1000

LIME_SAMPLE_SIZE = 500

COUNTERFACTUAL_TOTAL = 5

# ==================================================
# GEMINI SETTINGS
# ==================================================

def get_gemini_key():

    try:
        return st.secrets["GEMINI_API_KEY"]
    except:
        return None

GEMINI_MODEL = "gemini-flash-lite-latest"

# ==================================================
# SYNTHETIC DATA SETTINGS
# ==================================================

DEFAULT_CUSTOMERS = 5000

MAX_CUSTOMERS = 100000

PORTFOLIO_TYPES = [
    "Retail",
    "Credit Card",
    "Vehicle Loan",
    "Mortgage",
    "MSME",
    "Mixed"
]

# ==================================================
# CHAMPION CHALLENGER
# ==================================================

AVAILABLE_MODELS = [
    "Logistic Regression",
    "XGBoost",
    "LightGBM",
    "CatBoost"
]

# ==================================================
# GOVERNANCE
# ==================================================

MODEL_OWNER = "AI Division"

VALIDATION_FREQUENCY = "Quarterly"

MONITORING_FREQUENCY = "Monthly"

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

GEMINI_MODEL = "gemini-flash-lite-latest"
