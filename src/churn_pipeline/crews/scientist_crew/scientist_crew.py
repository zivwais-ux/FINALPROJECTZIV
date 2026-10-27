import os
from pathlib import Path

import pandas as pd
from crewai import LLM, Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, before_kickoff, crew, task

from churn_pipeline.contract import load_contract, validate_against_contract
from churn_pipeline.tools.scientist_tools import (
    build_features_tool,
    read_model_facts_tool,
    review_contract_tool,
    train_and_evaluate_tool,
)


def _llm() -> LLM:
    # temperature=0 keeps agent wording as repeatable as the model allows;
    # the numbers themselves always come from tools.
    return LLM(model=os.getenv("MODEL", "gpt-4.1-mini"), temperature=0)


@CrewBase
class ScientistCrew:
    """Data Scientist Crew: clean_data.csv + dataset_contract.json -> features, model, card."""

    agents: list[BaseAgent]
    tasks: list[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def contract_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config["contract_reviewer"],  # type: ignore[index]
            llm=_llm(),
            tools=[review_contract_tool],
            max_iter=8,
            verbose=True,
        )

    @agent
    def feature_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config["feature_engineer"],  # type: ignore[index]
            llm=_llm(),
            tools=[build_features_tool],
            max_iter=8,
            verbose=True,
        )

    @agent
    def model_trainer_evaluator(self) -> Agent:
        return Agent(
            config=self.agents_config["model_trainer_evaluator"],  # type: ignore[index]
            llm=_llm(),
            tools=[train_and_evaluate_tool],
            max_iter=8,
            verbose=True,
        )

    @agent
    def model_card_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["model_card_writer"],  # type: ignore[index]
            llm=_llm(),
            tools=[read_model_facts_tool],
            max_iter=8,
            verbose=True,
        )

    @before_kickoff
    def require_contract(self, inputs: dict) -> dict:
        """Refuse to start when clean_data.csv does not match dataset_contract.json.

        This runs in code before any agent, so no LLM can talk the crew past a
        broken contract.
        """
        input_dir = Path(inputs["input_dir"])
        data = input_dir / "clean_data.csv"
        violations = validate_against_contract(
            pd.read_csv(data), load_contract(input_dir / "dataset_contract.json"), file_path=data)
        if violations:
            raise ValueError("clean_data.csv does not match dataset_contract.json: "
                             + "; ".join(v.message for v in violations))
        Path(inputs["output_dir"]).mkdir(parents=True, exist_ok=True)
        return inputs

    @task
    def review_contract_task(self) -> Task:
        return Task(config=self.tasks_config["review_contract_task"])  # type: ignore[index]

    @task
    def engineer_features_task(self) -> Task:
        return Task(config=self.tasks_config["engineer_features_task"])  # type: ignore[index]

    @task
    def train_evaluate_task(self) -> Task:
        return Task(config=self.tasks_config["train_evaluate_task"])  # type: ignore[index]

    @task
    def model_card_task(self) -> Task:
        return Task(config=self.tasks_config["model_card_task"])  # type: ignore[index]

    @crew
    def crew(self) -> Crew:
        """Creates the Data Scientist Crew."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
