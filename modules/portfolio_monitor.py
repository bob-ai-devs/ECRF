"""
Enterprise Explainable Credit Risk Factory
Portfolio Monitoring Module
"""

import numpy as np
import pandas as pd

# =====================================================
# PSI
# =====================================================

class PSIAnalyzer:

    @staticmethod
    def calculate(
        expected,
        actual,
        bins=10
    ):

        expected = np.array(expected)
        actual = np.array(actual)

        breakpoints = np.linspace(
            0,
            100,
            bins + 1
        )

        cuts = np.percentile(
            expected,
            breakpoints
        )

        expected_counts = np.histogram(
            expected,
            bins=cuts
        )[0]

        actual_counts = np.histogram(
            actual,
            bins=cuts
        )[0]

        expected_pct = (
            expected_counts
            /
            len(expected)
        )

        actual_pct = (
            actual_counts
            /
            len(actual)
        )

        expected_pct = np.where(
            expected_pct == 0,
            0.0001,
            expected_pct
        )

        actual_pct = np.where(
            actual_pct == 0,
            0.0001,
            actual_pct
        )

        psi = np.sum(
            (
                actual_pct
                -
                expected_pct
            )
            *
            np.log(
                actual_pct
                /
                expected_pct
            )
        )

        return round(
            psi,
            4
        )

    @staticmethod
    def status(
        psi
    ):

        if psi < 0.10:
            return "Stable"

        elif psi < 0.25:
            return "Warning"

        return "Critical"

# =====================================================
# CSI
# =====================================================

class CSIAnalyzer:

    @staticmethod
    def calculate(
        expected,
        actual,
        bins=10
    ):

        return PSIAnalyzer.calculate(
            expected,
            actual,
            bins
        )

# =====================================================
# FEATURE DRIFT
# =====================================================

class DriftAnalyzer:

    @staticmethod
    def feature_drift(
        baseline_df,
        current_df,
        features
    ):

        records = []

        for feature in features:

            try:

                psi = PSIAnalyzer.calculate(

                    baseline_df[
                        feature
                    ],

                    current_df[
                        feature
                    ]

                )

                records.append({

                    "feature":
                        feature,

                    "psi":
                        psi,

                    "status":
                        PSIAnalyzer.status(
                            psi
                        )

                })

            except Exception:

                continue

        return pd.DataFrame(
            records
        )

# =====================================================
# SCORE MIGRATION
# =====================================================

class ScoreMigration:

    @staticmethod
    def create_matrix(
        old_scores,
        new_scores
    ):

        old_band = pd.cut(

            old_scores,

            bins=[
                300,
                500,
                600,
                700,
                800,
                900
            ]

        )

        new_band = pd.cut(

            new_scores,

            bins=[
                300,
                500,
                600,
                700,
                800,
                900
            ]

        )

        matrix = pd.crosstab(

            old_band,

            new_band,

            normalize="index"

        )

        return matrix

# =====================================================
# PD MIGRATION
# =====================================================

class PDMigration:

    @staticmethod
    def migration_matrix(
        old_pd,
        new_pd
    ):

        labels = [

            "VL",
            "L",
            "M",
            "H",
            "VH"

        ]

        old_bucket = pd.cut(

            old_pd,

            bins=[
                0,
                0.02,
                0.05,
                0.10,
                0.20,
                1.0
            ],

            labels=labels

        )

        new_bucket = pd.cut(

            new_pd,

            bins=[
                0,
                0.02,
                0.05,
                0.10,
                0.20,
                1.0
            ],

            labels=labels

        )

        return pd.crosstab(

            old_bucket,

            new_bucket,

            normalize="index"

        )

# =====================================================
# VINTAGE ANALYSIS
# =====================================================

class VintageAnalysis:

    @staticmethod
    def build(
        df,
        mob_col="mob",
        target="default"
    ):

        vintage = (

            df.groupby(
                mob_col
            )[target]

            .mean()

            .reset_index()

        )

        vintage.columns = [

            "mob",

            "bad_rate"

        ]

        return vintage

# =====================================================
# RISK CONCENTRATION
# =====================================================

class RiskConcentration:

    @staticmethod
    def by_grade(
        df
    ):

        return (

            df.groupby(
                "risk_grade"
            )

            .agg(

                customers=(
                    "customer_id",
                    "count"
                ),

                avg_pd=(
                    "predicted_pd",
                    "mean"
                )

            )

            .reset_index()

        )

# =====================================================
# EARLY WARNING SIGNALS
# =====================================================

class EarlyWarningSignals:

    @staticmethod
    def detect(
        df
    ):

        alerts = []

        high_util = df[
            df[
                "credit_utilization"
            ] > 0.90
        ]

        if len(high_util) > 0:

            alerts.append({

                "alert":
                    "Extreme Utilization",

                "count":
                    len(high_util)

            })

        high_pd = df[
            df[
                "predicted_pd"
            ] > 0.20
        ]

        if len(high_pd) > 0:

            alerts.append({

                "alert":
                    "High PD",

                "count":
                    len(high_pd)

            })

        delinquent = df[
            df[
                "delinquencies"
            ] >= 3
        ]

        if len(delinquent) > 0:

            alerts.append({

                "alert":
                    "Repeat Delinquencies",

                "count":
                    len(delinquent)

            })

        return pd.DataFrame(
            alerts
        )

# =====================================================
# RISK HEATMAP
# =====================================================

class RiskHeatmap:

    @staticmethod
    def build(
        df
    ):

        heatmap = pd.pivot_table(

            df,

            index="risk_grade",

            values="predicted_pd",

            aggfunc=[
                np.mean,
                np.max,
                np.min
            ]

        )

        return heatmap

# =====================================================
# THRESHOLD BREACHES
# =====================================================

class ThresholdMonitor:

    @staticmethod
    def evaluate(
        metrics
    ):

        breaches = []

        if metrics["psi"] > 0.25:

            breaches.append(
                "PSI Breach"
            )

        if metrics["avg_pd"] > 0.15:

            breaches.append(
                "PD Breach"
            )

        if metrics["default_rate"] > 0.10:

            breaches.append(
                "Default Rate Breach"
            )

        return breaches

# =====================================================
# REGULATORY STATUS
# =====================================================

class RegulatoryMonitor:

    @staticmethod
    def rag(
        psi,
        avg_pd
    ):

        if psi > 0.25 or avg_pd > 0.20:

            return "RED"

        elif psi > 0.10:

            return "AMBER"

        return "GREEN"

# =====================================================
# EXECUTIVE SUMMARY
# =====================================================

def monitoring_summary(
    df
):

    return {

        "customers":
            len(df),

        "avg_score":
            round(
                df[
                    "credit_score"
                ].mean(),
                0
            ),

        "avg_pd":
            round(
                df[
                    "predicted_pd"
                ].mean(),
                4
            ),

        "default_rate":
            round(
                df[
                    "default"
                ].mean(),
                4
            )
    }