"""
Enterprise Explainable Credit Risk Factory
PD Modeling Engine
"""

import os
import joblib
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.metrics import (
    roc_auc_score,
    roc_curve
)

from sklearn.linear_model import (
    LogisticRegression
)

from xgboost import XGBClassifier

from lightgbm import (
    LGBMClassifier
)

from catboost import (
    CatBoostClassifier
)

# ==========================================
# METRICS
# ==========================================

def calculate_ks(
    y_true,
    y_prob
):

    fpr, tpr, _ = roc_curve(
        y_true,
        y_prob
    )

    ks = np.max(
        np.abs(
            tpr - fpr
        )
    )

    return round(
        ks,
        4
    )


def calculate_gini(
    auc
):

    return round(
        (2 * auc) - 1,
        4
    )

# ==========================================
# SCORE SCALING
# ==========================================

def pd_to_score(
    pd_values,
    min_score=300,
    max_score=900
):

    score = (
        max_score
        -
        (
            pd_values
            *
            (
                max_score
                -
                min_score
            )
        )
    )

    return score.astype(int)

# ==========================================
# RISK GRADING
# ==========================================

def assign_risk_grade(
    score
):

    if score >= 850:
        return "A+"

    elif score >= 800:
        return "A"

    elif score >= 700:
        return "B"

    elif score >= 600:
        return "C"

    elif score >= 500:
        return "D"

    return "E"

# ==========================================
# MODEL WRAPPER
# ==========================================

class PDModel:

    def __init__(
        self,
        model_name
    ):

        self.model_name = model_name

        self.model = None

        self.metrics = {}

    # ======================================

    def create_model(self):

        if self.model_name == "Logistic Regression":

            self.model = LogisticRegression(
                max_iter=2000
            )

        elif self.model_name == "XGBoost":

            self.model = XGBClassifier(
                n_estimators=300,
                max_depth=5,
                learning_rate=0.05,
                eval_metric="logloss"
            )

        elif self.model_name == "LightGBM":

            self.model = LGBMClassifier(
                n_estimators=300,
                learning_rate=0.05
            )

        elif self.model_name == "CatBoost":

            self.model = CatBoostClassifier(
                verbose=0,
                iterations=300
            )

        else:

            raise ValueError(
                f"Unknown model: {self.model_name}"
            )

    # ======================================

    def fit(
        self,
        X_train,
        y_train
    ):

        self.create_model()

        self.model.fit(
            X_train,
            y_train
        )

    # ======================================

    def predict_pd(
        self,
        X
    ):

        return self.model.predict_proba(
            X
        )[:, 1]

    # ======================================

    def evaluate(
        self,
        X_test,
        y_test
    ):

        probs = self.predict_pd(
            X_test
        )

        auc = roc_auc_score(
            y_test,
            probs
        )

        ks = calculate_ks(
            y_test,
            probs
        )

        gini = calculate_gini(
            auc
        )

        self.metrics = {

            "auc":
                round(
                    auc,
                    4
                ),

            "ks":
                ks,

            "gini":
                gini
        }

        return self.metrics

# ==========================================
# CHAMPION CHALLENGER
# ==========================================

class ChampionChallenger:

    def __init__(self):

        self.models = {}

        self.results = []

        self.champion = None

    # ======================================

    def train_all(
        self,
        X_train,
        y_train,
        X_test,
        y_test
    ):

        candidates = [

            "Logistic Regression",
            "XGBoost",
            "LightGBM",
            "CatBoost"
        ]

        self.results = []

        for name in candidates:

            model = PDModel(
                name
            )

            model.fit(
                X_train,
                y_train
            )

            metrics = model.evaluate(
                X_test,
                y_test
            )

            self.models[
                name
            ] = model

            self.results.append({

                "model":
                    name,

                "auc":
                    metrics["auc"],

                "ks":
                    metrics["ks"],

                "gini":
                    metrics["gini"]
            })

        return pd.DataFrame(
            self.results
        )

    # ======================================

    def select_champion(
        self
    ):

        result_df = pd.DataFrame(
            self.results
        )

        champion_name = (

            result_df
            .sort_values(
                "auc",
                ascending=False
            )
            .iloc[0]["model"]

        )

        self.champion = self.models[
            champion_name
        ]

        return champion_name

# ==========================================
# MODEL REGISTRY
# ==========================================

class ModelRegistry:

    def __init__(
        self,
        model_dir="models"
    ):

        self.model_dir = model_dir

        os.makedirs(
            model_dir,
            exist_ok=True
        )

    # ======================================

    def save_model(
        self,
        model,
        model_name
    ):

        path = os.path.join(

            self.model_dir,

            f"{model_name}.pkl"

        )

        joblib.dump(
            model,
            path
        )

        return path

    # ======================================

    def load_model(
        self,
        model_name
    ):

        path = os.path.join(

            self.model_dir,

            f"{model_name}.pkl"

        )

        return joblib.load(
            path
        )

# ==========================================
# PD PIPELINE
# ==========================================

def train_pd_pipeline(
    df,
    target="default"
):

    features = [

        c for c in df.columns

        if c not in [

            target,
            "customer_id"
        ]
    ]

    X = df[
        features
    ].select_dtypes(
        include=np.number
    )

    y = df[
        target
    ]

    X_train, X_test, y_train, y_test = (

        train_test_split(

            X,
            y,

            test_size=0.2,

            random_state=42,

            stratify=y

        )

    )

    arena = ChampionChallenger()

    leaderboard = arena.train_all(

        X_train,
        y_train,

        X_test,
        y_test

    )

    champion_name = (

        arena.select_champion()

    )

    champion_model = (

        arena.champion

    )

    probs = champion_model.predict_pd(
        X
    )

    df["predicted_pd"] = probs

    df["credit_score"] = (

        pd_to_score(
            probs
        )

    )

    df["risk_grade"] = (

        df["credit_score"]

        .apply(
            assign_risk_grade
        )

    )

    return {

        "data": df,

        "leaderboard": leaderboard,

        "champion_name":
            champion_name,

        "champion_model":
            champion_model,

        "features":
            list(X.columns)
    }

# ==========================================
# PD BUCKETING
# ==========================================

def create_pd_buckets(
    df,
    pd_column="predicted_pd"
):

    bins = [

        0,
        0.02,
        0.05,
        0.10,
        0.20,
        1.0

    ]

    labels = [

        "Very Low",

        "Low",

        "Medium",

        "High",

        "Very High"

    ]

    return pd.cut(

        df[pd_column],

        bins=bins,

        labels=labels

    )

# ==========================================
# PORTFOLIO METRICS
# ==========================================

def portfolio_pd_summary(
    df
):

    return {

        "avg_pd":
            round(
                df["predicted_pd"].mean(),
                4
            ),

        "avg_score":
            round(
                df["credit_score"].mean(),
                0
            ),

        "default_rate":
            round(
                df["default"].mean(),
                4
            ),

        "high_risk_customers":

            len(

                df[
                    df[
                        "predicted_pd"
                    ] > 0.20
                ]

            )
    }