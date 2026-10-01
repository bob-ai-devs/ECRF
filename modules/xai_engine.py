"""
Enterprise Explainable Credit Risk Factory
XAI Engine

Modules:
- SHAP
- LIME
- Counterfactuals
- Adverse Action Generator
- Decision Engine
- Customer Improvement Simulator
"""

import numpy as np
import pandas as pd

import shap

from lime.lime_tabular import LimeTabularExplainer

import dice_ml

# ====================================================
# GLOBAL SHAP
# ====================================================

class SHAPAnalyzer:

    def __init__(
        self,
        model,
        features
    ):

        self.model = model
        self.features = features

        self.explainer = shap.TreeExplainer(
            model.model
        )

    # ============================================

    def global_importance(
        self,
        X
    ):

        shap_values = self.explainer.shap_values(X)

        importance = pd.DataFrame({

            "feature":
                X.columns,

            "importance":
                np.abs(
                    shap_values
                ).mean(axis=0)

        })

        importance = (

            importance
            .sort_values(
                "importance",
                ascending=False
            )

        )

        return importance

    # ============================================

    def local_explanation(
        self,
        X,
        customer_index
    ):

        shap_values = (

            self.explainer.shap_values(
                X
            )

        )

        row = shap_values[
            customer_index
        ]

        result = pd.DataFrame({

            "feature":
                X.columns,

            "impact":
                row

        })

        result = result.sort_values(

            "impact",

            key=np.abs,

            ascending=False

        )

        return result


# ====================================================
# LIME
# ====================================================

class LIMEAnalyzer:

    def __init__(
        self,
        model,
        X_train
    ):

        self.model = model

        self.explainer = (

            LimeTabularExplainer(

                training_data=X_train.values,

                feature_names=
                list(X_train.columns),

                class_names=[
                    "Good",
                    "Bad"
                ],

                mode="classification"

            )

        )

    # ============================================

    def explain_customer(
        self,
        customer_row
    ):

        explanation = (

            self.explainer.explain_instance(

                customer_row.values,

                self.model.model.predict_proba,

                num_features=10

            )

        )

        return explanation.as_list()


# ====================================================
# DICE COUNTERFACTUAL
# ====================================================

class CounterfactualEngine:

    def __init__(
        self,
        model,
        df,
        target="default"
    ):

        self.model = model

        self.df = df

        self.target = target

    # ============================================

    def generate(
        self,
        customer_row,
        total_cf=3
    ):

        features = [

            c

            for c in self.df.columns

            if c not in [

                self.target,
                "customer_id"

            ]

        ]

        numerical = list(

            self.df[
                features
            ].select_dtypes(
                include=np.number
            ).columns

        )

        data_object = (

            dice_ml.Data(

                dataframe=self.df,

                continuous_features=numerical,

                outcome_name=self.target

            )

        )

        model_object = (

            dice_ml.Model(

                model=self.model.model,

                backend="sklearn"

            )

        )

        dice = dice_ml.Dice(

            data_object,

            model_object

        )

        cf = dice.generate_counterfactuals(

            customer_row,

            total_CFs=total_cf,

            desired_class="opposite"

        )

        return (

            cf.cf_examples_list[0]

            .final_cfs_df

        )


# ====================================================
# DECISION ENGINE
# ====================================================

class CreditDecisionEngine:

    def __init__(self):

        pass

    # ============================================

    def evaluate(
        self,
        pd_value,
        score
    ):

        if score >= 700 and pd_value < 0.10:

            return {

                "decision":
                    "APPROVE",

                "reason":
                    "Low Risk"

            }

        elif score >= 600:

            return {

                "decision":
                    "REVIEW",

                "reason":
                    "Moderate Risk"

            }

        else:

            return {

                "decision":
                    "REJECT",

                "reason":
                    "High Risk"

            }


# ====================================================
# ADVERSE ACTION
# ====================================================

class AdverseActionGenerator:

    def __init__(self):

        pass

    # ============================================

    def generate(
        self,
        shap_explanation
    ):

        negative = (

            shap_explanation[
                shap_explanation[
                    "impact"
                ] > 0
            ]

            .head(5)

        )

        reasons = []

        for _, row in negative.iterrows():

            reasons.append(

                f"{row['feature']} "
                f"increased risk"

            )

        return reasons


# ====================================================
# IMPROVEMENT SIMULATOR
# ====================================================

class CustomerImprovementSimulator:

    def __init__(
        self,
        model,
        features
    ):

        self.model = model

        self.features = features

    # ============================================

    def simulate(
        self,
        customer_row,
        changes
    ):

        modified = (

            customer_row.copy()

        )

        for key, value in changes.items():

            if key in modified:

                modified[key] = value

        pd_before = (

            self.model.predict_pd(

                customer_row
                .to_frame()
                .T

            )[0]

        )

        pd_after = (

            self.model.predict_pd(

                modified
                .to_frame()
                .T

            )[0]

        )

        return {

            "old_pd":
                round(
                    pd_before,
                    4
                ),

            "new_pd":
                round(
                    pd_after,
                    4
                ),

            "improvement":
                round(
                    pd_before
                    -
                    pd_after,
                    4
                )
        }


# ====================================================
# APPROVAL RESOLUTION
# ====================================================

def generate_resolution_payload(
    customer,
    decision,
    shap_df
):

    top_positive = (

        shap_df

        .sort_values(
            "impact",
            ascending=False
        )

        .head(5)

    )

    top_negative = (

        shap_df

        .sort_values(
            "impact",
            ascending=True
        )

        .head(5)

    )

    return {

        "customer_id":

            customer[
                "customer_id"
            ],

        "decision":

            decision[
                "decision"
            ],

        "reason":

            decision[
                "reason"
            ],

        "positive_drivers":

            top_negative[
                "feature"
            ].tolist(),

        "risk_drivers":

            top_positive[
                "feature"
            ].tolist()
    }


# ====================================================
# CUSTOMER STORY
# ====================================================

def build_customer_story(
    customer
):

    return f"""

Customer Risk Profile

Age:
{customer.get('age')}

Income:
{round(customer.get('income',0),2)}

Bureau Score:
{round(customer.get('bureau_score',0),2)}

Utilization:
{round(customer.get('credit_utilization',0),2)}

Delinquencies:
{customer.get('delinquencies')}

Predicted PD:
{round(customer.get('predicted_pd',0),4)}

Credit Score:
{customer.get('credit_score')}

Risk Grade:
{customer.get('risk_grade')}

"""