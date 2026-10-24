import os

from crewai import LLM, Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, after_kickoff, agent, before_kickoff, crew, task

from churn_pipeline.crews.analyst_crew.outputs import ContractText
from churn_pipeline.tools.analyst_tools import (
    build_contract_tool,
    export_clean_data_tool,
    finalize_contract,
    profile_raw_data_tool,
    run_eda_tool,
)


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
            tools=[profile_raw_data_tool],
            max_iter=8,
            verbose=True,
        )

    @agent
    def data_preparation_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config["data_preparation_engineer"],  # type: ignore[index]
            llm=_llm(),
            tools=[export_clean_data_tool],
            max_iter=8,
            verbose=True,
        )

    @agent
    def eda_insights_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["eda_insights_analyst"],  # type: ignore[index]
            llm=_llm(),
            tools=[run_eda_tool],
            max_iter=8,
            verbose=True,
        )

    @agent
    def contract_steward(self) -> Agent:
        return Agent(
            config=self.agents_config["contract_steward"],  # type: ignore[index]
            llm=_llm(),
            tools=[build_contract_tool],
            max_iter=8,
            verbose=True,
        )

    @before_kickoff
    def remember_inputs(self, inputs: dict) -> dict:
        self._output_dir = inputs["output_dir"]
        return inputs

    @after_kickoff
    def publish_contract(self, result):
        """Merge the steward's text with the tool's numbers into dataset_contract.json.

        finalize_contract validates the merged contract against clean_data.csv
        and raises if they disagree, so the crew never hands over a bad contract.
        """
        text = result.pydantic
        if not isinstance(text, ContractText):
            raise ValueError("contract steward did not return ContractText")
        finalize_contract(
            self._output_dir,
            column_descriptions={c.name: c.description for c in text.column_descriptions},
            assumptions=text.assumptions,
            leakage_notes=text.leakage_notes,
        )
        return result

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
