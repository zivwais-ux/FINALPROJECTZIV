import os

from crewai import LLM, Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task

from churn_pipeline.crews.analyst_crew.outputs import ContractText


def _llm() -> LLM:
    # temperature=0 keeps agent wording as repeatable as the model allows;
    # the numbers themselves always come from tools.
    return LLM(model=os.getenv("MODEL", "gpt-4.1-mini"), temperature=0)


@CrewBase
class AnalystCrew:
    """Data Analyst Crew: raw data -> clean_data.csv, EDA, insights, contract."""

    agents: list[BaseAgent]
    tasks: list[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def data_quality_inspector(self) -> Agent:
        return Agent(
            config=self.agents_config["data_quality_inspector"],  # type: ignore[index]
            llm=_llm(),
            max_iter=8,
            verbose=True,
        )

    @agent
    def data_preparation_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config["data_preparation_engineer"],  # type: ignore[index]
            llm=_llm(),
            max_iter=8,
            verbose=True,
        )

    @agent
    def eda_insights_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["eda_insights_analyst"],  # type: ignore[index]
            llm=_llm(),
            max_iter=8,
            verbose=True,
        )

    @agent
    def contract_steward(self) -> Agent:
        return Agent(
            config=self.agents_config["contract_steward"],  # type: ignore[index]
            llm=_llm(),
            max_iter=8,
            verbose=True,
        )

    # Tools are attached to the agents in step 3.4.

    @task
    def inspect_raw_data_task(self) -> Task:
        return Task(config=self.tasks_config["inspect_raw_data_task"])  # type: ignore[index]

    @task
    def prepare_clean_data_task(self) -> Task:
        return Task(config=self.tasks_config["prepare_clean_data_task"])  # type: ignore[index]

    @task
    def eda_task(self) -> Task:
        return Task(config=self.tasks_config["eda_task"])  # type: ignore[index]

    @task
    def publish_contract_task(self) -> Task:
        return Task(
            config=self.tasks_config["publish_contract_task"],  # type: ignore[index]
            output_pydantic=ContractText,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Data Analyst Crew."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
