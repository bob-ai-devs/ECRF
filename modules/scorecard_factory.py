"""
Enterprise Explainable Credit Risk Factory
Scorecard Factory

Siddiqi-based Scorecard Development
"""

import pandas as pd
import numpy as np

from sklearn.preprocessing import KBinsDiscretizer

# =====================================================
# INFORMATION VALUE INTERPRETATION
# =====================================================

def iv_strength(iv):

    if iv < 0.02:
        return "Not Predictive"

    elif iv < 0.1:
        return "Weak"

    elif iv < 0.3:
        return "Medium"

    elif iv < 0.5:
        return "Strong"

    return "Suspiciously Strong"


# =====================================================
# AUTO BINNING
# =====================================================

def create_bins(
    df,
    variable,
    bins=10
):

    temp = df[[variable]].copy()

    discretizer = KBinsDiscretizer(
        n_bins=bins,
        encode="ordinal",
        strategy="quantile"
    )

    temp["bin"] = discretizer.fit_transform(
        temp[[variable]]
    )

    return temp["bin"]


# =====================================================
# WOE TABLE
# =====================================================

def calculate_woe_iv(
    df,
    variable,
    target="default",
    bins=10
):

    work = df[[variable, target]].copy()

    work["bin"] = create_bins(
        work,
        variable,
        bins
    )

    grouped = (
        work
        .groupby("bin")
        .agg(
            good=(target,
                  lambda x: (x == 0).sum()),
            bad=(target,
                 lambda x: (x == 1).sum())
        )
        .reset_index()
    )

    grouped["good_pct"] = (
        grouped["good"]
        /
        grouped["good"].sum()
    )

    grouped["bad_pct"] = (
        grouped["bad"]
        /
        grouped["bad"].sum()
    )

    grouped["good_pct"] += 1e-6
    grouped["bad_pct"] += 1e-6

    grouped["woe"] = np.log(
        grouped["good_pct"]
        /
        grouped["bad_pct"]
    )

    grouped["iv"] = (
        grouped["good_pct"]
        -
        grouped["bad_pct"]
    ) * grouped["woe"]

    total_iv = grouped["iv"].sum()

    grouped["variable"] = variable

    return grouped, total_iv


# =====================================================
# VARIABLE SCREENING
# =====================================================

def variable_iv_ranking(
    df,
    variables,
    target="default"
):

    records = []

    for var in variables:

        try:

            _, iv = calculate_woe_iv(
                df,
                var,
                target
            )

            records.append({
                "variable": var,
                "iv": iv,
                "strength": iv_strength(iv)
            })

        except Exception:
            continue

    result = pd.DataFrame(records)

    result = result.sort_values(
        "iv",
        ascending=False
    )

    return result


# =====================================================
# MONOTONICITY CHECK
# =====================================================

def monotonicity_check(
    woe_table
):

    values = woe_table["woe"].values

    increasing = np.all(
        np.diff(values) >= 0
    )

    decreasing = np.all(
        np.diff(values) <= 0
    )

    return increasing or decreasing


# =====================================================
# SCORE SCALING
# =====================================================

class ScoreScaler:

    def __init__(
        self,
        min_score=300,
        max_score=900
    ):

        self.min_score = min_score
        self.max_score = max_score

    def scale_probability(
        self,
        pd_values
    ):

        scores = (
            self.max_score
            -
            (
                pd_values
                *
                (
                    self.max_score
                    -
                    self.min_score
                )
            )
        )

        return scores.astype(int)


# =====================================================
# SCORECARD GENERATOR
# =====================================================

class ScorecardFactory:

    def __init__(
        self,
        target="default"
    ):

        self.target = target

        self.variable_report = None

    # ==============================================

    def build_variable_report(
        self,
        df,
        variables
    ):

        report = variable_iv_ranking(
            df,
            variables,
            self.target
        )

        self.variable_report = report

        return report

    # ==============================================

    def select_variables(
        self,
        min_iv=0.02
    ):

        selected = self.variable_report[
            self.variable_report["iv"]
            >= min_iv
        ]

        return selected

# =====================================================
# RISK GRADES
# =====================================================

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


# =====================================================
# SCORE DISTRIBUTION
# =====================================================

def build_score_distribution(
    scores
):

    return pd.cut(
        scores,
        bins=[
            300,
            500,
            600,
            700,
            800,
            850,
            900
        ]
    ).value_counts()


# =====================================================
# CHARACTERISTIC CONTRIBUTION
# =====================================================

def characteristic_contribution(
    row,
    selected_features
):

    contributions = {}

    total = 0

    for col in selected_features:

        value = row[col]

        contributions[col] = value

        total += abs(value)

    for col in contributions:

        contributions[col] = round(
            (
                abs(contributions[col])
                /
                total
            )
            * 100,
            2
        )

    return contributions


# =====================================================
# SCORE DECOMPOSITION
# =====================================================

def explain_score(
    row,
    selected_features
):

    contrib = characteristic_contribution(
        row,
        selected_features
    )

    ranked = sorted(
        contrib.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return ranked


# =====================================================
# DEVELOPMENT REPORT
# =====================================================

def scorecard_summary(
    iv_report
):

    return {

        "variables_tested":
            len(iv_report),

        "strong_variables":
            len(
                iv_report[
                    iv_report["iv"] >= 0.3
                ]
            ),

        "medium_variables":
            len(
                iv_report[
                    (
                        iv_report["iv"] >= 0.1
                    )
                    &
                    (
                        iv_report["iv"] < 0.3
                    )
                ]
            ),

        "weak_variables":
            len(
                iv_report[
                    iv_report["iv"] < 0.1
                ]
            )
    }