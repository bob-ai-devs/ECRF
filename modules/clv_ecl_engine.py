"""
Enterprise Explainable Credit Risk Factory
CLV + ECL + IFRS9 Engine
"""

import numpy as np
import pandas as pd

# =====================================================
# LGD ENGINE
# =====================================================

class LGDEngine:

    @staticmethod
    def estimate_lgd(
        collateral_ratio,
        unsecured=False
    ):

        if unsecured:
            return 0.75

        lgd = 1 - collateral_ratio

        lgd = max(
            0.05,
            min(
                lgd,
                0.90
            )
        )

        return round(
            lgd,
            4
        )

# =====================================================
# EAD ENGINE
# =====================================================

class EADEngine:

    @staticmethod
    def estimate_ead(
        outstanding_balance,
        undrawn_limit=0,
        ccf=0.75
    ):

        ead = (

            outstanding_balance

            +

            (
                undrawn_limit
                * ccf
            )

        )

        return round(
            ead,
            2
        )

# =====================================================
# ECL ENGINE
# =====================================================

class ECLEngine:

    @staticmethod
    def calculate_ecl(
        pd,
        lgd,
        ead
    ):

        return round(

            pd
            *
            lgd
            *
            ead,

            2

        )

    # =========================================

    @staticmethod
    def portfolio_ecl(
        df
    ):

        return round(

            df["ecl"]
            .sum(),

            2

        )

# =====================================================
# IFRS9 STAGING
# =====================================================

class IFRS9Stage:

    @staticmethod
    def assign(
        pd,
        delinquency
    ):

        if delinquency >= 90:

            return "Stage 3"

        elif pd > 0.15:

            return "Stage 2"

        return "Stage 1"

# =====================================================
# CLV ENGINE
# =====================================================

class CLVEngine:

    @staticmethod
    def calculate_clv(

        annual_revenue,

        retention_rate,

        discount_rate,

        years=5

    ):

        clv = 0

        for year in range(

            1,

            years + 1

        ):

            value = (

                annual_revenue

                *

                (
                    retention_rate
                    ** year
                )

            )

            discounted = (

                value

                /

                (
                    (
                        1
                        +
                        discount_rate
                    )
                    ** year
                )

            )

            clv += discounted

        return round(
            clv,
            2
        )

# =====================================================
# RISK ADJUSTED CLV
# =====================================================

class RiskAdjustedCLV:

    @staticmethod
    def calculate(
        clv,
        ecl
    ):

        return round(

            clv - ecl,

            2

        )

# =====================================================
# STRESS SCENARIOS
# =====================================================

class StressScenarioEngine:

    @staticmethod
    def mild(
        df
    ):

        stressed = df.copy()

        stressed["predicted_pd"] *= 1.10

        return stressed

    @staticmethod
    def moderate(
        df
    ):

        stressed = df.copy()

        stressed["predicted_pd"] *= 1.30

        return stressed

    @staticmethod
    def severe(
        df
    ):

        stressed = df.copy()

        stressed["predicted_pd"] *= 1.60

        return stressed

# =====================================================
# MACRO ADJUSTMENT
# =====================================================

class MacroAdjustment:

    @staticmethod
    def apply(

        pd_value,

        inflation,

        unemployment,

        gdp_growth

    ):

        multiplier = 1

        multiplier += (

            inflation - 5

        ) * 0.03

        multiplier += (

            unemployment - 5

        ) * 0.05

        multiplier -= (

            gdp_growth - 5

        ) * 0.04

        adjusted_pd = (

            pd_value
            *
            multiplier

        )

        return max(
            0,
            min(
                adjusted_pd,
                1
            )
        )

# =====================================================
# PORTFOLIO ECL BUILDER
# =====================================================

def build_ecl_portfolio(
    df
):

    work = df.copy()

    if "loan_amount" not in work.columns:

        work["loan_amount"] = 500000

    work["lgd"] = np.where(

        work["risk_grade"].isin(

            ["A+", "A"]

        ),

        0.25,

        np.where(

            work["risk_grade"].isin(

                ["B", "C"]

            ),

            0.45,

            0.70

        )

    )

    work["ead"] = (

        work["loan_amount"]

    )

    work["ecl"] = (

        work["predicted_pd"]

        *

        work["lgd"]

        *

        work["ead"]

    )

    return work

# =====================================================
# IFRS9 BUILDER
# =====================================================

def build_ifrs9(
    df
):

    work = df.copy()

    if "delinquencies" not in work.columns:

        work["delinquencies"] = 0

    work["days_past_due"] = (

        work["delinquencies"]

        * 30

    )

    work["ifrs9_stage"] = (

        work.apply(

            lambda row:

            IFRS9Stage.assign(

                row["predicted_pd"],

                row["days_past_due"]

            ),

            axis=1

        )

    )

    return work

# =====================================================
# PROFITABILITY
# =====================================================

class ProfitabilityEngine:

    @staticmethod
    def expected_profit(

        loan_amount,

        interest_rate,

        ecl

    ):

        income = (

            loan_amount

            *

            interest_rate

        )

        return round(

            income - ecl,

            2

        )

# =====================================================
# EXECUTIVE SUMMARY
# =====================================================

def ecl_summary(
    df
):

    return {

        "customers":

            len(df),

        "portfolio_ecl":

            round(
                df["ecl"].sum(),
                2
            ),

        "avg_ecl":

            round(
                df["ecl"].mean(),
                2
            ),

        "stage1":

            int(
                (
                    df["ifrs9_stage"]
                    ==
                    "Stage 1"
                ).sum()
            ),

        "stage2":

            int(
                (
                    df["ifrs9_stage"]
                    ==
                    "Stage 2"
                ).sum()
            ),

        "stage3":

            int(
                (
                    df["ifrs9_stage"]
                    ==
                    "Stage 3"
                ).sum()
            )
    }