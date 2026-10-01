"""
Enterprise Explainable Credit Risk Factory
Model Governance & AI Risk Management
"""

import uuid
import pandas as pd
from datetime import datetime

# =====================================================
# MODEL INVENTORY
# =====================================================

class ModelInventory:

    def __init__(self):

        self.inventory = []

    def register(
        self,
        model_name,
        version,
        owner,
        purpose,
        champion=False
    ):

        record = {

            "model_id":
                str(uuid.uuid4()),

            "model_name":
                model_name,

            "version":
                version,

            "owner":
                owner,

            "purpose":
                purpose,

            "champion":
                champion,

            "registration_date":
                datetime.now(),

            "status":
                "Development"
        }

        self.inventory.append(
            record
        )

        return record

    def get_inventory(self):

        return pd.DataFrame(
            self.inventory
        )

# =====================================================
# MODEL LIFECYCLE
# =====================================================

class ModelLifecycle:

    VALID_STATES = [

        "Development",
        "Validation",
        "Approved",
        "Production",
        "Retired"
    ]

    @staticmethod
    def transition(
        record,
        new_state
    ):

        if new_state not in (
            ModelLifecycle.VALID_STATES
        ):

            raise ValueError(
                "Invalid State"
            )

        record["status"] = new_state

        return record

# =====================================================
# VALIDATION TRACKING
# =====================================================

class ValidationTracker:

    @staticmethod
    def create_record(

        model_name,

        auc,

        ks,

        gini,

        validator

    ):

        return {

            "model_name":
                model_name,

            "auc":
                auc,

            "ks":
                ks,

            "gini":
                gini,

            "validator":
                validator,

            "validation_date":
                datetime.now(),

            "approved":
                auc >= 0.70
        }

# =====================================================
# FAIRNESS ANALYZER
# =====================================================

class FairnessAnalyzer:

    @staticmethod
    def demographic_parity(

        df,

        prediction_col,

        group_col

    ):

        result = (

            df.groupby(
                group_col
            )[prediction_col]

            .mean()

            .reset_index()

        )

        result.columns = [

            group_col,

            "approval_rate"

        ]

        return result

    @staticmethod
    def disparate_impact(

        df,

        prediction_col,

        group_col

    ):

        rates = (

            df.groupby(
                group_col
            )[prediction_col]

            .mean()

        )

        if len(rates) < 2:

            return None

        return round(

            rates.min()
            /
            rates.max(),

            4

        )

# =====================================================
# EXPLAINABILITY COMPLIANCE
# =====================================================

class ExplainabilityCompliance:

    @staticmethod
    def evaluate(
        shap_enabled,
        lime_enabled,
        counterfactual_enabled
    ):

        score = 0

        if shap_enabled:
            score += 1

        if lime_enabled:
            score += 1

        if counterfactual_enabled:
            score += 1

        return {

            "score":
                score,

            "max_score":
                3,

            "compliant":
                score >= 2
        }

# =====================================================
# AI RISK CLASSIFICATION
# =====================================================

class AIRiskClassification:

    @staticmethod
    def classify(
        use_case
    ):

        high_risk = [

            "credit_scoring",

            "loan_approval",

            "fraud_detection",

            "ifrs9",

            "collections"

        ]

        if use_case.lower() in high_risk:

            return "HIGH"

        return "MEDIUM"

# =====================================================
# AUDIT TRAIL
# =====================================================

class AuditTrail:

    def __init__(self):

        self.logs = []

    def log(

        self,

        user,

        action,

        details

    ):

        self.logs.append({

            "timestamp":
                datetime.now(),

            "user":
                user,

            "action":
                action,

            "details":
                details

        })

    def get_logs(self):

        return pd.DataFrame(
            self.logs
        )

# =====================================================
# CHANGE MANAGEMENT
# =====================================================

class ChangeManagement:

    @staticmethod
    def record_change(

        model_name,

        old_version,

        new_version,

        reason

    ):

        return {

            "model_name":
                model_name,

            "old_version":
                old_version,

            "new_version":
                new_version,

            "reason":
                reason,

            "change_date":
                datetime.now()
        }

# =====================================================
# REGULATORY CHECKLIST
# =====================================================

class RegulatoryChecklist:

    @staticmethod
    def generate():

        checklist = [

            "Business Justification",

            "Training Dataset Documented",

            "Validation Completed",

            "Bias Assessment Completed",

            "Explainability Available",

            "Audit Trail Enabled",

            "Monitoring Framework Active",

            "Stress Testing Available",

            "Governance Approval Obtained"

        ]

        return pd.DataFrame({

            "requirement":
                checklist,

            "status":
                "Pending"
        })

# =====================================================
# COMPLIANCE SCORE
# =====================================================

class ComplianceScore:

    @staticmethod
    def calculate(
        checklist_df
    ):

        completed = (

            checklist_df[
                "status"
            ] == "Completed"

        ).sum()

        total = len(
            checklist_df
        )

        return round(

            completed
            /
            total
            * 100,

            2

        )

# =====================================================
# MODEL RISK RATING
# =====================================================

class ModelRiskRating:

    @staticmethod
    def assign(

        psi,

        auc,

        fairness_score

    ):

        risk = 0

        if psi > 0.25:
            risk += 1

        if auc < 0.70:
            risk += 1

        if fairness_score < 0.80:
            risk += 1

        if risk == 0:
            return "LOW"

        elif risk == 1:
            return "MEDIUM"

        return "HIGH"

# =====================================================
# GOVERNANCE SUMMARY
# =====================================================

def governance_summary(

    inventory_df,

    compliance_score

):

    return {

        "models":
            len(inventory_df),

        "production_models":

            (
                inventory_df[
                    "status"
                ]

                ==
                "Production"

            ).sum(),

        "compliance_score":
            compliance_score
    }