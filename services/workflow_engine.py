from modules.pd_models import train_pd_pipeline

from modules.clv_ecl_engine import (
    build_ecl_portfolio,
    build_ifrs9
)

from modules.digital_twin import (
    build_portfolio_twins
)

from modules.portfolio_monitor import (
    monitoring_summary
)


class WorkflowEngine:

    @staticmethod
    def run(df):

        pd_output = train_pd_pipeline(df)

        scored_df = pd_output["data"]

        scored_df = build_ecl_portfolio(
            scored_df
        )

        scored_df = build_ifrs9(
            scored_df
        )

        twins = build_portfolio_twins(
            scored_df
        )

        metrics = monitoring_summary(
            scored_df
        )

        return {

            "data": scored_df,

            "leaderboard":
                pd_output["leaderboard"],

            "champion_model":
                pd_output["champion_model"],

            "champion_name":
                pd_output["champion_name"],

            "digital_twins":
                twins,

            "metrics":
                metrics
        }