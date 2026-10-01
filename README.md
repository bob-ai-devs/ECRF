# 🏦 Enterprise Explainable Credit Risk Factory

## AI-Powered Credit Risk Intelligence Platform

The **Enterprise Explainable Credit Risk Factory (ECRF)** is a Streamlit-based AI platform designed to provide an integrated environment for **credit risk modeling, explainability, portfolio analytics, customer intelligence, stress testing, and model governance**.

The platform provides an end-to-end credit risk workflow starting from synthetic portfolio generation and progressing through model development, champion-challenger analysis, explainability, portfolio monitoring, customer digital twins, Gemini-based risk intelligence, and model governance.

---

# 🟣 Platform Overview

The Enterprise Explainable Credit Risk Factory integrates multiple credit-risk capabilities into a single platform:

* 📊 Data Factory
* 🎯 Scorecard Factory
* 📈 Probability of Default (PD) Modeling
* 🧠 Explainable AI (XAI)
* 🚫 Reject Inference
* 📉 Portfolio Monitoring
* 💰 CLV / ECL Analytics
* 👤 Customer Digital Twin
* 🤖 Gemini Risk Copilot
* 🛡️ Model Governance
* ⚠️ Stress Testing

The platform is designed around a controlled workflow where portfolio data is generated first and downstream risk modules become progressively available as processing is completed.

---

# 🎯 Key Objectives

The platform aims to provide a unified environment for:

* Credit risk data generation
* Credit scorecard development
* Probability of Default modeling
* Model comparison
* Champion-challenger analysis
* Explainable AI
* Reject inference
* Portfolio-level risk monitoring
* Expected Credit Loss analytics
* Customer-level intelligence
* AI-assisted risk analysis
* Model inventory and governance

---

# 🏗️ Platform Architecture

The application follows a modular architecture.

```text
                         🏦 ECRF
                           │
             ┌─────────────┴─────────────┐
             │                           │
       Data Generation             Risk Workflow
             │                           │
             ▼                           ▼
      Portfolio Data            Workflow Engine
                                         │
              ┌──────────────────────────┼─────────────────────────┐
              │                          │                         │
              ▼                          ▼                         ▼
       Scorecard Factory          PD Modeling                 XAI Lab
              │                          │                         │
              └──────────────────────────┼─────────────────────────┘
                                         │
                    ┌────────────────────┼────────────────────┐
                    │                    │                    │
                    ▼                    ▼                    ▼
             Reject Inference      Portfolio Monitor      CLV / ECL
                    │                    │                    │
                    └────────────────────┼────────────────────┘
                                         │
                          ┌──────────────┴──────────────┐
                          │                             │
                          ▼                             ▼
                  Digital Twin                  Gemini Copilot
                          │                             │
                          └──────────────┬──────────────┘
                                         ▼
                                  Model Governance
```

---

# 📊 Core Platform Modules

## 1. 📊 Data Factory

The Data Factory generates synthetic credit portfolio data.

Users can configure:

* Portfolio type
* Number of customers
* Random seed

The generated portfolio is stored in the Streamlit session and becomes the input for downstream modules.

The application supports portfolio generation through the `generate_credit_data()` function.

---

# 🎯 2. Scorecard Factory

The Scorecard Factory is designed for credit scorecard development.

It forms part of the platform's core credit-risk capability matrix and is intended to support scorecard-based credit risk assessment.

---

# 📈 3. Probability of Default Modeling

The PD Modeling module supports development and evaluation of Probability of Default models.

The workflow engine returns:

* Model leaderboard
* Champion model
* Champion model name
* Portfolio metrics
* Digital twins

The selected champion model is subsequently registered in the model inventory.

---

# 🧠 4. XAI Lab

The Explainable AI module provides model interpretability capabilities.

The platform capability matrix identifies:

* SHAP
* LIME
* STEDCAM
* Governance

as part of the explainability layer.

---

# 🚫 5. Reject Inference

Reject Inference is included as a dedicated credit-risk module.

It becomes available after the required model-processing stage has been completed.

---

# 📉 6. Portfolio Monitor

The Portfolio Monitor provides portfolio-level risk analysis.

It is activated after successful completion of the main ECRF pipeline.

Portfolio monitoring is part of the platform's defined credit-risk operating system.

---

# 💰 7. CLV / ECL Analytics

The platform includes **Customer Lifetime Value (CLV)** and **Expected Credit Loss (ECL)** analytics.

These capabilities support customer-level and portfolio-level financial risk analysis.

---

# 👤 8. Customer Digital Twin

The Digital Twin module maintains customer-level analytical representations.

The workflow engine returns digital twin information as part of the ECRF pipeline results.

The platform tracks whether digital twin information has been successfully generated before marking the module as ready.

---

# 🤖 9. Gemini Risk Copilot

The Gemini Copilot is an AI-assisted risk intelligence module.

It is included in the platform's intelligence layer together with:

* Digital Twin
* CLV / ECL
* Stress Testing

The Copilot becomes available after completion of the core ECRF pipeline.

---

# 🛡️ 10. Model Governance

The platform includes a dedicated Model Governance module.

After the ECRF pipeline completes, the champion model is registered using the model inventory.

The current implementation registers:

```text
Model Name
Version
Owner
Purpose
Champion Status
```

Example configuration:

```text
Version: v1
Owner: RiskTeam
Purpose: Credit Risk Scoring
Champion: True
```

This inventory mechanism is implemented through the `ModelInventory` component.

---

# 🧪 Champion-Challenger Framework

The platform includes a **Champion Challenger Arena** for comparing model performance.

Once model results are available, the application displays:

* Champion model
* Model leaderboard
* Comparative model results

The leaderboard is displayed in the Champion Challenger section of the application.

---

# 📊 Executive Command Center

After successful pipeline execution, the platform provides an Executive Command Center.

The dashboard displays:

| KPI              | Description                          |
| ---------------- | ------------------------------------ |
| 👥 Customers     | Number of customers in the portfolio |
| 🎯 Average Score | Average portfolio credit score       |
| 📈 Average PD    | Average Probability of Default       |
| ⚠️ Default Rate  | Portfolio default rate               |

These metrics are obtained from the portfolio metrics generated by the workflow engine.

---

# ⚠️ Portfolio Risk Indicators

The Executive Command Center provides portfolio-level risk messaging based on average PD.

The application categorizes the portfolio into:

```text
Average PD < 5%
        │
        ▼
Strong Credit Quality

Average PD < 15%
        │
        ▼
Moderate Portfolio Risk

Average PD >= 15%
        │
        ▼
Elevated Portfolio Risk
```

These thresholds are implemented directly in the current application logic.

---

# 📋 Portfolio Overview

The Portfolio Overview provides a summary of the generated or processed portfolio.

The dashboard displays:

* Number of records
* Number of columns
* Number of defaults

A preview of the first 20 portfolio records is also available.

---

# 🟢 Module Readiness

The application provides a dedicated **Module Readiness** dashboard.

Each module is assigned a status:

```text
🟢 Ready
🔴 Not Ready
```

Current readiness is determined by the availability of the corresponding portfolio/model/pipeline outputs.

The readiness matrix includes:

| Module            | Readiness Dependency     |
| ----------------- | ------------------------ |
| Data Factory      | Portfolio generated      |
| Scorecard Factory | Portfolio generated      |
| PD Modeling       | Champion model available |
| XAI Lab           | Champion model available |
| Reject Inference  | Champion model available |
| Portfolio Monitor | Pipeline completed       |
| CLV / ECL         | Pipeline completed       |
| Digital Twin      | Digital twin generated   |
| Gemini Copilot    | Pipeline completed       |
| Model Governance  | Pipeline completed       |

This readiness logic is implemented in the main application.

---

# 🔄 ECRF Workflow

The recommended workflow is:

```text
1. Generate Portfolio
        ↓
2. Scorecard Factory
        ↓
3. PD Modeling
        ↓
4. XAI Lab
        ↓
5. Reject Inference
        ↓
6. Portfolio Monitoring
        ↓
7. CLV / ECL
        ↓
8. Digital Twin
        ↓
9. Gemini Copilot
        ↓
10. Model Governance
```

This workflow is also exposed directly within the application under **Recommended Workflow**.

---

# 🖥️ Application Interface

The application contains five primary tabs:

```text
📋 Module Readiness
📊 Platform Capability Matrix & Executive Command Center
🏆 Champion Challenger
📈 Portfolio Overview
🧭 Open Modules & Recommended Workflow
```

These tabs provide centralized navigation across platform status, analytics, model comparison, portfolio information, and module access.

---

# 🧭 Open Modules

The application provides direct navigation to the individual Streamlit pages.

```text
📊 Data Factory
🎯 Scorecard Factory
📈 PD Modeling
🧠 XAI Lab
🚫 Reject Inference
📉 Portfolio Monitor
💰 CLV / ECL
👤 Digital Twin
🤖 Gemini Copilot
🛡️ Model Governance
```

These modules are exposed through Streamlit page navigation.

---

# 🗂️ Project Structure

The application follows a modular project structure similar to:

```text
ECRF/
│
├── app.py
├── config.py
│
├── assets/
│   └── theme.py
│
├── modules/
│   ├── data_factory.py
│   └── model_governance.py
│
├── services/
│   ├── session_manager.py
│   └── workflow_engine.py
│
└── pages/
    ├── 01_Data_Factory.py
    ├── 02_Scorecard_Factory.py
    ├── 03_PD_Modeling.py
    ├── 04_XAI_Lab.py
    ├── 05_Reject_Inference.py
    ├── 06_Portfolio_Monitor.py
    ├── 07_CLV_ECL.py
    ├── 08_Digital_Twin.py
    ├── 09_Gemini_Copilot.py
    └── 10_Model_Governance.py
```

The main application imports configuration, session management, workflow processing, data generation, theming, and model governance as separate components.

---

# 🧠 Session Management

The application uses Streamlit session state to maintain the state of:

* Generated portfolio
* Customer count
* Random seed
* Selected portfolio type
* Pipeline status
* Model leaderboard
* Champion model
* Champion model name
* Digital twins
* Portfolio metrics
* Scorecard results
* XAI results
* Model inventory

The session is initialized through the `initialize_session()` service.

---

# ⚙️ Portfolio Generation

The sidebar provides configuration controls for:

### Portfolio Type

The portfolio type is selected from the configured portfolio types.

### Customers

The number of customers can be selected using a slider.

### Random Seed

A random seed can be specified to support reproducible synthetic portfolio generation.

The application then calls:

```python
generate_credit_data(
    n_customers=customers,
    seed=seed,
    portfolio_type=portfolio_type
)
```

The resulting dataset becomes the platform portfolio.

---

# 🚀 Running the ECRF Pipeline

After generating a portfolio, users can execute:

```text
🚀 Run Full ECRF Pipeline
```

The pipeline passes the portfolio to:

```python
WorkflowEngine.run(
    st.session_state.portfolio_data
)
```

The returned results populate the major ECRF outputs, including the processed portfolio, model leaderboard, champion model, digital twins, and portfolio metrics.

---

# 📦 Technology Stack

The application is built using:

```text
Python
│
├── Streamlit
├── Pandas
├── NumPy
├── Machine Learning Models
├── Explainable AI
├── Gemini AI
└── Custom ECRF Services & Modules
```

The exact dependencies required by individual modules should be maintained in the project's `requirements.txt`.

---

# ▶️ Running the Application

Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit application:

```bash
streamlit run app.py
```

The application will open in the Streamlit web interface.

---

# 🔐 Governance and Risk Controls

The platform is designed with governance as an explicit component rather than treating model development as the final stage.

The overall workflow includes:

```text
Data
 ↓
Model Development
 ↓
Model Comparison
 ↓
Explainability
 ↓
Portfolio Analysis
 ↓
AI-Assisted Intelligence
 ↓
Model Governance
```

This allows model outputs to be connected with explainability, portfolio analytics, and governance processes.

---

# 🎨 User Interface

The application uses a Bank-oriented visual identity.

The main header presents:

```text
🏦 Enterprise Explainable Credit Risk Factory
Bank of Baroda | Credit Risk Intelligence Platform
```

The interface uses a wide Streamlit layout with an expanded sidebar and a customized BOB theme.

---

# 📌 Platform Status

The application tracks three primary platform states:

```text
⏳ Waiting For Data
        ↓
📊 Portfolio Generated
        ↓
🟢 Pipeline Ready
```

The displayed status changes according to whether portfolio data has been generated and whether the complete ECRF pipeline has successfully executed.

---

# 🎯 Intended Use

The ECRF platform can serve as a foundation for:

* Credit risk PoCs
* Model development
* Model validation workflows
* Portfolio risk analysis
* Explainable AI demonstrations
* AI governance demonstrations
* Credit risk research
* Enterprise risk dashboards
* AI-assisted risk management

---

# ⚠️ Important Note

This application is a **credit-risk intelligence and modeling platform/PoC**. Its outputs should be appropriately validated, governed, and reviewed before being used for production credit decisions.

Synthetic portfolio generation and model outputs should not automatically be interpreted as production-grade credit decisions.

---

# 🏦 Enterprise Explainable Credit Risk Factory

```text
        🏦 ECRF
          │
          ▼
   Generate Portfolio
          │
          ▼
   Credit Risk Models
          │
          ▼
 Champion / Challenger
          │
          ▼
   Explainable AI
          │
          ▼
 Portfolio Intelligence
          │
          ▼
 Customer Intelligence
          │
          ▼
   Gemini Risk Copilot
          │
          ▼
 Model Governance
```

**Enterprise Explainable Credit Risk Factory (ECRF)**
**AI Risk Platform**
