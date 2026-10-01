"""
Enterprise Explainable Credit Risk Factory
Customer Digital Twin
"""

import numpy as np
import pandas as pd

# =====================================================
# CUSTOMER PROFILE
# =====================================================

class CustomerProfile:

    @staticmethod
    def build(
        customer_row
    ):

        profile = {

            "customer_id":
                customer_row.get(
                    "customer_id"
                ),

            "age":
                customer_row.get(
                    "age"
                ),

            "income":
                customer_row.get(
                    "income"
                ),

            "tenure_months":
                customer_row.get(
                    "tenure_months"
                ),

            "bureau_score":
                customer_row.get(
                    "bureau_score"
                ),

            "portfolio_type":
                customer_row.get(
                    "portfolio_type",
                    "Retail"
                )
        }

        return profile

# =====================================================
# RISK PROFILE
# =====================================================

class RiskProfile:

    @staticmethod
    def build(
        customer_row
    ):

        return {

            "predicted_pd":
                customer_row.get(
                    "predicted_pd"
                ),

            "credit_score":
                customer_row.get(
                    "credit_score"
                ),

            "risk_grade":
                customer_row.get(
                    "risk_grade"
                ),

            "default":
                customer_row.get(
                    "default"
                )
        }

# =====================================================
# BEHAVIOR PROFILE
# =====================================================

class BehaviorProfile:

    @staticmethod
    def build(
        customer_row
    ):

        return {

            "credit_utilization":
                customer_row.get(
                    "credit_utilization"
                ),

            "delinquencies":
                customer_row.get(
                    "delinquencies"
                ),

            "salary_volatility":
                customer_row.get(
                    "salary_volatility"
                ),

            "emi_ratio":
                customer_row.get(
                    "emi_ratio"
                )
        }

# =====================================================
# PROFITABILITY PROFILE
# =====================================================

class ProfitabilityProfile:

    @staticmethod
    def build(
        customer_row
    ):

        return {

            "ead":
                customer_row.get(
                    "ead",
                    0
                ),

            "lgd":
                customer_row.get(
                    "lgd",
                    0
                ),

            "ecl":
                customer_row.get(
                    "ecl",
                    0
                ),

            "clv":
                customer_row.get(
                    "clv",
                    0
                ),

            "risk_adjusted_clv":
                customer_row.get(
                    "risk_adjusted_clv",
                    0
                )
        }

# =====================================================
# IFRS9 PROFILE
# =====================================================

class IFRS9Profile:

    @staticmethod
    def build(
        customer_row
    ):

        return {

            "ifrs9_stage":
                customer_row.get(
                    "ifrs9_stage"
                ),

            "days_past_due":
                customer_row.get(
                    "days_past_due",
                    0
                )
        }

# =====================================================
# EARLY WARNING SIGNALS
# =====================================================

class EarlyWarningEngine:

    @staticmethod
    def detect(
        customer_row
    ):

        alerts = []

        if customer_row.get(
            "credit_utilization",
            0
        ) > 0.90:

            alerts.append(
                "Extreme Utilization"
            )

        if customer_row.get(
            "predicted_pd",
            0
        ) > 0.20:

            alerts.append(
                "High PD"
            )

        if customer_row.get(
            "delinquencies",
            0
        ) >= 3:

            alerts.append(
                "Repeat Delinquencies"
            )

        if customer_row.get(
            "salary_volatility",
            0
        ) > 0.80:

            alerts.append(
                "Income Instability"
            )

        return alerts

# =====================================================
# STRESS IMPACT
# =====================================================

class StressImpact:

    @staticmethod
    def calculate(
        customer_row
    ):

        pd_value = customer_row.get(
            "predicted_pd",
            0
        )

        return {

            "base_pd":
                round(
                    pd_value,
                    4
                ),

            "mild":
                round(
                    pd_value * 1.10,
                    4
                ),

            "moderate":
                round(
                    pd_value * 1.30,
                    4
                ),

            "severe":
                round(
                    pd_value * 1.60,
                    4
                )
        }

# =====================================================
# CUSTOMER TRAJECTORY
# =====================================================

class CustomerTrajectory:

    @staticmethod
    def forecast(
        customer_row
    ):

        current_pd = customer_row.get(
            "predicted_pd",
            0
        )

        months = []

        for m in range(1, 13):

            future_pd = (

                current_pd

                *

                np.random.uniform(
                    0.95,
                    1.10
                )

            )

            months.append({

                "month": m,

                "pd":
                    round(
                        future_pd,
                        4
                    )
            })

        return pd.DataFrame(
            months
        )

# =====================================================
# ACTION ENGINE
# =====================================================

class ActionRecommendationEngine:

    @staticmethod
    def recommend(
        customer_row
    ):

        actions = []

        if customer_row.get(
            "credit_utilization",
            0
        ) > 0.80:

            actions.append(
                "Reduce utilization below 50%"
            )

        if customer_row.get(
            "delinquencies",
            0
        ) >= 2:

            actions.append(
                "Monitor repayment behavior"
            )

        if customer_row.get(
            "salary_volatility",
            0
        ) > 0.70:

            actions.append(
                "Review income stability"
            )

        if customer_row.get(
            "predicted_pd",
            0
        ) > 0.15:

            actions.append(
                "Move to watchlist"
            )

        return actions

# =====================================================
# RELATIONSHIP SCORE
# =====================================================

class RelationshipScore:

    @staticmethod
    def calculate(
        customer_row
    ):

        score = 100

        score -= (
            customer_row.get(
                "predicted_pd",
                0
            ) * 100
        )

        score -= (
            customer_row.get(
                "delinquencies",
                0
            ) * 5
        )

        score += min(

            customer_row.get(
                "tenure_months",
                0
            ) / 12,

            20

        )

        return round(
            score,
            2
        )

# =====================================================
# DIGITAL TWIN BUILDER
# =====================================================

class DigitalTwinBuilder:

    def build(
        self,
        customer_row
    ):

        twin = {

            "profile":
                CustomerProfile.build(
                    customer_row
                ),

            "risk":
                RiskProfile.build(
                    customer_row
                ),

            "behavior":
                BehaviorProfile.build(
                    customer_row
                ),

            "profitability":
                ProfitabilityProfile.build(
                    customer_row
                ),

            "ifrs9":
                IFRS9Profile.build(
                    customer_row
                ),

            "stress":
                StressImpact.calculate(
                    customer_row
                ),

            "alerts":
                EarlyWarningEngine.detect(
                    customer_row
                ),

            "actions":
                ActionRecommendationEngine
                .recommend(
                    customer_row
                ),

            "relationship_score":
                RelationshipScore
                .calculate(
                    customer_row
                )
        }

        return twin

# =====================================================
# PORTFOLIO DIGITAL TWINS
# =====================================================

def build_portfolio_twins(
    df
):

    builder = DigitalTwinBuilder()

    twins = {}

    for _, row in df.iterrows():

        twins[
            row["customer_id"]
        ] = builder.build(
            row
        )

    return twins

# =====================================================
# EXECUTIVE SUMMARY
# =====================================================

def twin_summary(
    twin
):

    return {

        "customer_id":
            twin["profile"][
                "customer_id"
            ],

        "risk_grade":
            twin["risk"][
                "risk_grade"
            ],

        "pd":
            twin["risk"][
                "predicted_pd"
            ],

        "ifrs9":
            twin["ifrs9"][
                "ifrs9_stage"
            ],

        "alerts":
            len(
                twin["alerts"]
            ),

        "relationship_score":
            twin[
                "relationship_score"
            ]
    }