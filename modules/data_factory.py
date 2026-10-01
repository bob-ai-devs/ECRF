"""
Enterprise Explainable Credit Risk Factory
Data Factory Module
"""

import numpy as np
import pandas as pd

# =====================================================
# MASTER GENERATOR
# =====================================================

class SyntheticPortfolioFactory:

    def __init__(
        self,
        n_customers=5000,
        seed=42,
        portfolio_type="Retail"
    ):

        if n_customers <= 0:
            raise ValueError(
                "n_customers must be > 0"
            )

        self.n_customers = n_customers
        self.seed = seed
        self.portfolio_type = portfolio_type

        np.random.seed(seed)

    # =================================================
    # MAIN ENTRY
    # =================================================

    def generate(self):

        if self.portfolio_type == "Retail":
            return self._retail_portfolio()

        elif self.portfolio_type == "MSME":
            return self._msme_portfolio()

        elif self.portfolio_type == "Credit Card":
            return self._credit_card_portfolio()

        elif self.portfolio_type == "Mortgage":
            return self._mortgage_portfolio()

        elif self.portfolio_type == "Vehicle Loan":
            return self._vehicle_portfolio()

        elif self.portfolio_type == "Mixed":
            return self._mixed_portfolio()

        raise ValueError(
            f"Unsupported portfolio type: {self.portfolio_type}"
        )

    # =================================================
    # BASE CUSTOMER
    # =================================================

    def _base_customer_frame(self):

        df = pd.DataFrame()

        df["customer_id"] = np.arange(
            1,
            self.n_customers + 1
        )

        df["age"] = np.random.randint(
            21,
            70,
            self.n_customers
        )

        df["tenure_months"] = np.random.randint(
            1,
            240,
            self.n_customers
        )

        df["income"] = np.random.normal(
            800000,
            250000,
            self.n_customers
        ).clip(100000)

        df["employment_years"] = np.random.randint(
            0,
            35,
            self.n_customers
        )

        return df

    # =================================================
    # RETAIL
    # =================================================

    def _retail_portfolio(self):

        df = self._base_customer_frame()

        df["loan_amount"] = np.random.normal(
            500000,
            200000,
            len(df)
        ).clip(50000)

        df["credit_utilization"] = np.random.uniform(
            0,
            1,
            len(df)
        )

        df["account_balance"] = np.random.normal(
            150000,
            75000,
            len(df)
        ).clip(0)

        return self._create_target(df)

    # =================================================
    # MSME
    # =================================================

    def _msme_portfolio(self):

        df = self._base_customer_frame()

        df["annual_turnover"] = np.random.normal(
            5000000,
            2000000,
            len(df)
        ).clip(500000)

        df["business_age"] = np.random.randint(
            1,
            25,
            len(df)
        )

        df["working_capital_limit"] = np.random.normal(
            1000000,
            400000,
            len(df)
        ).clip(100000)

        return self._create_target(df)

    # =================================================
    # CREDIT CARD
    # =================================================

    def _credit_card_portfolio(self):

        df = self._base_customer_frame()

        df["card_limit"] = np.random.normal(
            200000,
            100000,
            len(df)
        ).clip(20000)

        df["credit_utilization"] = np.random.uniform(
            0,
            1,
            len(df)
        )

        df["cash_withdrawals"] = np.random.poisson(
            3,
            len(df)
        )

        df["monthly_spend"] = np.random.normal(
            35000,
            15000,
            len(df)
        ).clip(1000)

        return self._create_target(df)

    # =================================================
    # MORTGAGE
    # =================================================

    def _mortgage_portfolio(self):

        df = self._base_customer_frame()

        df["property_value"] = np.random.normal(
            6000000,
            1500000,
            len(df)
        ).clip(1000000)

        df["ltv"] = np.random.uniform(
            0.30,
            0.95,
            len(df)
        )

        df["loan_amount"] = (
            df["property_value"] *
            df["ltv"]
        )

        return self._create_target(df)

    # =================================================
    # VEHICLE LOAN
    # =================================================

    def _vehicle_portfolio(self):

        df = self._base_customer_frame()

        df["vehicle_value"] = np.random.normal(
            800000,
            300000,
            len(df)
        ).clip(200000)

        df["loan_amount"] = (
            df["vehicle_value"]
            *
            np.random.uniform(
                0.6,
                0.95,
                len(df)
            )
        )

        return self._create_target(df)

    # =================================================
    # MIXED PORTFOLIO
    # =================================================

    def _mixed_portfolio(self):

        portfolio_types = [
            "Retail",
            "MSME",
            "Credit Card",
            "Mortgage",
            "Vehicle Loan"
        ]

        base = (
            self.n_customers //
            len(portfolio_types)
        )

        splits = [base] * len(portfolio_types)

        splits[-1] += (
            self.n_customers -
            sum(splits)
        )

        chunks = []

        for p, size in zip(
            portfolio_types,
            splits
        ):

            temp = SyntheticPortfolioFactory(
                n_customers=size,
                seed=self.seed,
                portfolio_type=p
            ).generate()

            temp["portfolio_type"] = p

            chunks.append(temp)

        # df = pd.concat(
        #     chunks,
        #     ignore_index=True
        # )
        
        df = pd.concat(
            chunks,
            ignore_index=True,
            sort=False
        )

        # Numeric columns
        numeric_cols = df.select_dtypes(
            include=np.number
        ).columns

        df[numeric_cols] = df[numeric_cols].fillna(0)

        # Object / category columns
        for col in df.columns:

            if str(df[col].dtype) == "category":

                df[col] = (
                    df[col]
                    .cat.add_categories(["Unknown"])
                    .fillna("Unknown")
                )

            elif df[col].dtype == "object":

                df[col] = df[col].fillna("Unknown")

        df["customer_id"] = np.arange(
            1,
            len(df) + 1
        )

        return df

    # =================================================
    # TARGET CREATION
    # =================================================

    def _create_target(self, df):

        n = len(df)

        if "credit_utilization" not in df.columns:

            df["credit_utilization"] = np.random.uniform(
                0,
                1,
                n
            )

        df["delinquencies"] = np.random.poisson(
            1,
            n
        )

        df["bureau_score"] = np.random.normal(
            720,
            60,
            n
        ).clip(
            300,
            900
        )

        df["salary_volatility"] = np.random.uniform(
            0,
            1,
            n
        )

        df["emi_ratio"] = np.random.uniform(
            0.05,
            0.75,
            n
        )

        df["missed_payments"] = np.random.poisson(
            0.5,
            n
        )

        # ==========================================
        # RISK MODEL
        # ==========================================

        risk = (
              -4.5
            + 2.0 * df["credit_utilization"]
            + 1.5 * df["salary_volatility"]
            + 1.2 * df["emi_ratio"]
            + 0.8 * df["delinquencies"]
            + 0.5 * df["missed_payments"]
            - 0.01 * (
                df["bureau_score"] - 700
            )
        )

        pd_prob = (
            1 /
            (
                1 +
                np.exp(-risk)
            )
        )

        macro_multiplier = np.random.uniform(
            0.90,
            1.20,
            n
        )

        pd_prob *= macro_multiplier

        pd_prob = np.clip(
            pd_prob,
            0,
            1
        )

        # ==========================================
        # TARGET
        # ==========================================

        df["default"] = np.random.binomial(
            1,
            pd_prob
        )

        df["actual_pd"] = pd_prob

        # ==========================================
        # CREDIT SCORE
        # ==========================================

        df["credit_score"] = (
            900 -
            (
                pd_prob * 600
            )
        ).clip(
            300,
            900
        )

        # ==========================================
        # RISK BAND
        # ==========================================

        df["risk_band"] = pd.cut(
            df["bureau_score"],
            bins=[
                300,
                580,
                670,
                740,
                800,
                900
            ],
            labels=[
                "Very High Risk",
                "High Risk",
                "Medium Risk",
                "Low Risk",
                "Very Low Risk"
            ]
        )

        # ==========================================
        # CUSTOMER SEGMENT
        # ==========================================

        df["customer_segment"] = pd.cut(
            df["income"],
            bins=[
                0,
                300000,
                800000,
                1500000,
                np.inf
            ],
            labels=[
                "Mass",
                "Mass Affluent",
                "Affluent",
                "HNI"
            ]
        )

        # ==========================================
        # EAD
        # ==========================================

        if "loan_amount" in df.columns:

            df["ead"] = df["loan_amount"]

        elif "card_limit" in df.columns:

            df["ead"] = (
                df["card_limit"] *
                df["credit_utilization"]
            )

        else:

            df["ead"] = (
                df["income"] * 0.5
            )

        # ==========================================
        # LGD
        # ==========================================

        df["lgd"] = np.random.uniform(
            0.20,
            0.80,
            n
        )

        # ==========================================
        # EXPECTED LOSS
        # ==========================================

        df["expected_loss"] = (
            df["actual_pd"]
            *
            df["lgd"]
            *
            df["ead"]
        )

        # ==========================================
        # SNAPSHOT DATE
        # ==========================================

        df["snapshot_date"] = (
            pd.Timestamp.now()
        )

        return df


# =====================================================
# MACRO SCENARIO
# =====================================================

def generate_macroeconomic_scenario():

    return {

        "repo_rate":
            np.random.uniform(5.5, 8.5),

        "inflation":
            np.random.uniform(3, 9),

        "unemployment":
            np.random.uniform(2, 12),

        "gdp_growth":
            np.random.uniform(-2, 9)
    }


# =====================================================
# BEHAVIORAL SHIFT
# =====================================================

def simulate_behavioral_shift(
    df,
    months=6
):

    new_df = df.copy()

    new_df["credit_utilization"] *= (
        np.random.uniform(
            0.8,
            1.3,
            len(df)
        )
    )

    new_df["bureau_score"] += (
        np.random.normal(
            0,
            25,
            len(df)
        )
    )

    new_df["salary_volatility"] *= (
        np.random.uniform(
            0.9,
            1.2,
            len(df)
        )
    )

    return new_df


# =====================================================
# PORTFOLIO SUMMARY
# =====================================================

def portfolio_summary(df):

    return {

        "customers":
            len(df),

        "default_rate":
            round(
                df["default"].mean(),
                4
            ),

        "avg_income":
            round(
                df["income"].mean(),
                2
            ),

        "avg_bureau":
            round(
                df["bureau_score"].mean(),
                2
            ),

        "avg_utilization":
            round(
                df["credit_utilization"].mean(),
                2
            ),

        "total_ead":
            round(
                df["ead"].sum(),
                2
            ),

        "total_expected_loss":
            round(
                df["expected_loss"].sum(),
                2
            )
    }


# =====================================================
# PUBLIC API
# =====================================================

def generate_credit_data(
    n_customers=5000,
    seed=42,
    portfolio_type="Retail"
):

    return SyntheticPortfolioFactory(
        n_customers=n_customers,
        seed=seed,
        portfolio_type=portfolio_type
    ).generate()