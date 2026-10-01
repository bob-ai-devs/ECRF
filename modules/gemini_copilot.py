"""
Enterprise Explainable Credit Risk Factory
Gemini Copilot
"""

import json

from google import genai

from datetime import date

from config import (
    GEMINI_API_KEY,
    GEMINI_MODEL
)

# ============================================
# CLIENT
# ============================================

class GeminiCopilot:

    def __init__(self):

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

    # ========================================

    def generate(
        self,
        prompt
    ):

        response = self.client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        return response.text

bank_name = "Bank of Baroda"

# ============================================
# CREDIT OFFICER
# ============================================

def underwriting_summary(
    customer_twin
):

    prompt = f"""
You are a Senior Credit Officer.

Analyze the customer profile.

Generate:

1. Executive Summary
2. Risk Assessment
3. Key Strengths
4. Key Weaknesses
5. Lending Recommendation

Customer Data:

{json.dumps(customer_twin, indent=2)}

Date: {date.today()}

Bank Name: {bank_name}

"""

    return GeminiCopilot().generate(
        prompt
    )

# ============================================
# ADVERSE ACTION
# ============================================

def adverse_action_letter(
    customer_twin
):

    prompt = f"""
You are a banking compliance officer.

Generate a customer-friendly
adverse action letter.

Customer Data:

{json.dumps(customer_twin, indent=2)}

Date: {date.today()}

Bank Name: {bank_name}

Requirements:

- Explain rejection
- Explain risk drivers
- Suggest improvements
- Avoid technical jargon
"""

    return GeminiCopilot().generate(
        prompt
    )

# ============================================
# XAI REPORT
# ============================================

def xai_summary(
    xai_payload
):

    prompt = f"""
Explain the AI decision.

Output:

1. Decision
2. Main Risk Drivers
3. Positive Drivers
4. Business Explanation
5. Recommended Actions

Data:

{json.dumps(xai_payload, indent=2)}

Date: {date.today()}

Bank Name: {bank_name}

"""

    return GeminiCopilot().generate(
        prompt
    )

# ============================================
# IFRS9 REPORT
# ============================================

def ifrs9_commentary(
    portfolio_summary
):

    prompt = f"""
You are an IFRS9 expert.

Generate:

1. Portfolio Summary
2. Stage Distribution
3. Expected Credit Loss Analysis
4. Regulatory Commentary

Data:

{json.dumps(
    portfolio_summary,
    indent=2
)}

Date: {date.today()}

Bank Name: {bank_name}

"""

    return GeminiCopilot().generate(
        prompt
    )

# ============================================
# STRESS TEST REPORT
# ============================================

def stress_test_report(
    stress_data
):

    prompt = f"""
You are a Chief Risk Officer.

Analyze stress test results.

Provide:

1. Executive Summary
2. Risk Impact
3. Portfolio Vulnerabilities
4. Recommendations

Data:

{json.dumps(
    stress_data,
    indent=2
)}

Date: {date.today()}

Bank Name: {bank_name}

"""

    return GeminiCopilot().generate(
        prompt
    )

# ============================================
# MODEL VALIDATION
# ============================================

def model_validation_report(
    leaderboard
):

    prompt = f"""
You are a Model Risk Validator.

Analyze model results.

Generate:

1. Champion Model Review
2. AUC Assessment
3. KS Assessment
4. Gini Assessment
5. Validation Opinion

Data:

{leaderboard.to_json()}

Date: {date.today()}

Bank Name: {bank_name}

"""

    return GeminiCopilot().generate(
        prompt
    )

# ============================================
# PORTFOLIO REVIEW
# ============================================

def portfolio_risk_review(
    portfolio_summary
):

    prompt = f"""
You are the Chief Risk Officer.

Analyze portfolio risk.

Generate:

1. Executive Summary
2. Portfolio Quality
3. Risk Concentration
4. Emerging Risks
5. Recommendations

Data:

{json.dumps(
    portfolio_summary,
    indent=2
)}

Date: {date.today()}

Bank Name: {bank_name}

"""

    return GeminiCopilot().generate(
        prompt
    )

# ============================================
# BOARD REPORT
# ============================================

def board_summary(
    executive_payload
):

    prompt = f"""
You are preparing a board report.

Create:

1. Executive Summary
2. Portfolio Health
3. Model Performance
4. IFRS9 Status
5. Key Risks
6. Recommended Actions

Data:

{json.dumps(
    executive_payload,
    indent=2
)}

Date: {date.today()}

Bank Name: {bank_name}

"""

    return GeminiCopilot().generate(
        prompt
    )

# ============================================
# NEXT BEST ACTION
# ============================================

def next_best_action(
    customer_twin
):

    prompt = f"""
You are a Relationship Manager.

Suggest:

1. Retention Strategy
2. Cross Sell Opportunity
3. Risk Mitigation
4. Customer Engagement Plan

Data:

{json.dumps(
    customer_twin,
    indent=2
)}

Date: {date.today()}

Bank Name: {bank_name}

"""

    return GeminiCopilot().generate(
        prompt
    )

# ============================================
# COLLECTION STRATEGY
# ============================================

def collection_strategy(
    customer_twin
):

    prompt = f"""
You are Head of Collections.

Generate:

1. Collection Priority
2. Recovery Probability
3. Suggested Action Plan
4. Escalation Need

Data:

{json.dumps(
    customer_twin,
    indent=2
)}

Date: {date.today()}

Bank Name: {bank_name}

"""

    return GeminiCopilot().generate(
        prompt
    )