"""
Enterprise Explainable Credit Risk Factory
Reject Inference Engine
"""

import numpy as np
import pandas as pd

# =====================================================
# CREATE APPROVED / REJECTED POPULATION
# =====================================================

def create_accept_reject_population(
    df,
    score_column="credit_score",
    cutoff_score=650
):

    work = df.copy()

    work["application_status"] = np.where(
        work[score_column] >= cutoff_score,
        "Approved",
        "Rejected"
    )

    return work


# =====================================================
# APPROVAL RATE
# =====================================================

def approval_rate(
    df
):

    approved = (
        df["application_status"] == "Approved"
    ).mean()

    return round(
        approved * 100,
        2
    )


# =====================================================
# PARCELING METHOD
# =====================================================

class ParcelingRejectInference:

    """
    Assigns inferred bad rates
    to rejected population.
    """

    def __init__(
        self,
        score_column="credit_score",
        target="default"
    ):

        self.score_column = score_column
        self.target = target

    # =========================================

    def infer(
        self,
        df,
        bins=10
    ):

        work = df.copy()

        work["score_bin"] = pd.qcut(
            work[self.score_column],
            q=bins,
            duplicates="drop"
        )

        approved = work[
            work["application_status"]
            == "Approved"
        ]

        bad_rates = (

            approved
            .groupby("score_bin")[self.target]
            .mean()

        )

        rejected_mask = (
            work["application_status"]
            == "Rejected"
        )

        for idx in work[
            rejected_mask
        ].index:

            score_bin = work.loc[
                idx,
                "score_bin"
            ]

            inferred_pd = bad_rates.get(
                score_bin,
                approved[self.target].mean()
            )

            work.loc[
                idx,
                "inferred_default"
            ] = np.random.binomial(
                1,
                inferred_pd
            )

        work["final_target"] = np.where(

            work["application_status"]
            == "Approved",

            work[self.target],

            work["inferred_default"]

        )

        return work


# =====================================================
# FUZZY AUGMENTATION
# =====================================================

class FuzzyAugmentation:

    """
    Uses PD predictions
    to infer rejected outcomes.
    """

    def __init__(
        self,
        pd_column="predicted_pd"
    ):

        self.pd_column = pd_column

    # =========================================

    def infer(
        self,
        df
    ):

        work = df.copy()

        rejected = (

            work["application_status"]
            == "Rejected"

        )

        work["fuzzy_target"] = np.nan

        work.loc[
            rejected,
            "fuzzy_target"
        ] = np.random.binomial(

            1,

            work.loc[
                rejected,
                self.pd_column
            ]

        )

        return work


# =====================================================
# PROFITABILITY SIMULATOR
# =====================================================

class ProfitabilitySimulator:

    def __init__(
        self,
        interest_rate=0.14,
        lgd=0.45
    ):

        self.interest_rate = interest_rate
        self.lgd = lgd

    # =========================================

    def expected_profit(
        self,
        loan_amount,
        pd
    ):

        income = (
            loan_amount
            *
            self.interest_rate
        )

        expected_loss = (

            loan_amount
            *
            pd
            *
            self.lgd

        )

        return income - expected_loss

    # =========================================

    def portfolio_profit(
        self,
        df,
        amount_column="loan_amount",
        pd_column="predicted_pd"
    ):

        profit = (

            df.apply(

                lambda row:

                self.expected_profit(

                    row[
                        amount_column
                    ],

                    row[
                        pd_column
                    ]

                ),

                axis=1

            )

        )

        return round(
            profit.sum(),
            2
        )


# =====================================================
# CUTOFF ANALYSIS
# =====================================================

class CutoffAnalyzer:

    def __init__(
        self,
        score_column="credit_score"
    ):

        self.score_column = score_column

    # =========================================

    def evaluate_cutoffs(
        self,
        df,
        cutoffs=range(
            500,
            851,
            25
        )
    ):

        results = []

        for cutoff in cutoffs:

            temp = create_accept_reject_population(
                df,
                self.score_column,
                cutoff
            )

            approved = temp[
                temp["application_status"]
                == "Approved"
            ]

            approval = (
                len(approved)
                /
                len(temp)
            )

            avg_pd = (
                approved[
                    "predicted_pd"
                ].mean()
            )

            avg_score = (
                approved[
                    self.score_column
                ].mean()
            )

            results.append({

                "cutoff":
                    cutoff,

                "approval_rate":
                    round(
                        approval,
                        4
                    ),

                "avg_pd":
                    round(
                        avg_pd,
                        4
                    ),

                "avg_score":
                    round(
                        avg_score,
                        0
                    )

            })

        return pd.DataFrame(
            results
        )


# =====================================================
# RISK APPETITE
# =====================================================

class RiskAppetiteSimulator:

    def recommend_cutoff(
        self,
        cutoff_df,
        max_pd=0.10
    ):

        valid = cutoff_df[

            cutoff_df["avg_pd"]
            <= max_pd

        ]

        if len(valid) == 0:

            return None

        best = valid.sort_values(

            "approval_rate",

            ascending=False

        ).iloc[0]

        return {

            "recommended_cutoff":
                int(best["cutoff"]),

            "approval_rate":
                float(
                    best[
                        "approval_rate"
                    ]
                ),

            "avg_pd":
                float(
                    best[
                        "avg_pd"
                    ]
                )

        }


# =====================================================
# SEGMENT ANALYSIS
# =====================================================

def segment_acceptance_analysis(
    df,
    segment_column
):

    result = (

        df.groupby(
            segment_column
        )

        .agg(

            customers=(
                "customer_id",
                "count"
            ),

            avg_score=(
                "credit_score",
                "mean"
            ),

            avg_pd=(
                "predicted_pd",
                "mean"
            )

        )

        .reset_index()

    )

    return result


# =====================================================
# EXPANSION OPPORTUNITY
# =====================================================

def expansion_opportunity(
    df,
    cutoff_score
):

    rejected = df[
        df["credit_score"]
        < cutoff_score
    ]

    near_prime = rejected[

        rejected["credit_score"]

        >=

        cutoff_score - 50

    ]

    return {

        "rejected":
            len(rejected),

        "near_prime":
            len(near_prime),

        "expansion_ratio":
            round(

                len(near_prime)

                /

                max(
                    len(rejected),
                    1
                ),

                4

            )
    }


# =====================================================
# EXECUTIVE SUMMARY
# =====================================================

def reject_inference_summary(
    df
):

    approved = (

        df["application_status"]
        == "Approved"

    ).sum()

    rejected = (

        df["application_status"]
        == "Rejected"

    ).sum()

    return {

        "approved":
            approved,

        "rejected":
            rejected,

        "approval_rate":
            round(

                approved
                /
                len(df),

                4

            )
    }