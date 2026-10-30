import os
import re
from pathlib import Path

from crewai import LLM, Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, before_kickoff, crew, task

from churn_pipeline.news import search_recent_news
from churn_pipeline.rag import default_index, search_internal_docs_tool
from churn_pipeline.tools.briefing_tools import (
    customer_risk_profile,
    customer_risk_profile_tool,
    search_recent_news_tool,
)

MAX_WORDS = 520  # about one printed page; the prompt asks for 450 to leave room


def _llm() -> LLM:
    # temperature=0 keeps agent wording as repeatable as the model allows;
    # the numbers themselves always come from tools.
    return LLM(model=os.getenv("MODEL", "gpt-4.1-mini"), temperature=0)


def check_briefing(text: str, profile: dict, citable: set[str], news_urls: set[str] | None = None) -> list[str]:
    """Problems that make a briefing unusable; empty means it may be published.

    citable holds every "file > section" in the internal documents, so a
    citation to a section that does not exist is caught. news_urls holds the
    links the news search returned, so an invented link is caught too.
    """
    problems = []
    words = len(re.findall(r"\S+", text))
    if words > MAX_WORDS:
        problems.append(f"the briefing has {words} words; keep it to {MAX_WORDS}")
    if f"{profile['risk_score']:.2f}" not in text:
        problems.append(f"quote the risk score exactly: {profile['risk_score']:.2f}")
    if profile["risk_band"] not in text.lower():
        problems.append(f"name the risk band: {profile['risk_band']}")
    cited = set(re.findall(r"\[([^\[\]]+\.md > [^\[\]]+)\]", text))
    if not cited:
        problems.append("cite at least one internal document as [file name > section]")
    unknown = sorted(cited - citable)
    if unknown:
        problems.append(f"these citations are not sections of the documents: {unknown}; "
                        "copy cite_as from the search results")
    invented = sorted(set(re.findall(r"https?://[^\s)\]>]+", text)) - (news_urls or set()))
    if invented:
        problems.append(f"these links did not come from search_recent_news: {invented[:3]}; "
                        "link only articles the search returned")
    for section in ("Churn risk", "Recommended action", "Market now", "Sources"):
        if section.lower() not in text.lower():
            problems.append(f"add the section {section}")
    return problems


@CrewBase
class BriefingCrew:
    """Retention briefing: approved churn model + internal documents (RAG) -> one-page briefing."""

    agents: list[BaseAgent]
    tasks: list[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def retention_briefing_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["retention_briefing_writer"],  # type: ignore[index]
            llm=_llm(),
            tools=[customer_risk_profile_tool, search_internal_docs_tool, search_recent_news_tool],
            max_iter=8,
            verbose=True,
        )

    @before_kickoff
    def require_customer(self, inputs: dict) -> dict:
        """Score the customer in code first: no approved model or unknown customer, no briefing."""
        self._profile = customer_risk_profile(int(inputs["customer_id"]))
        # Searched here first so the guardrail knows which links are real; the
        # agent's own call gets the same cached result.
        self._news = search_recent_news(self._profile["news_query"])
        Path(inputs["output_dir"]).mkdir(parents=True, exist_ok=True)
        return inputs

    def _guardrail(self, output):
        problems = check_briefing(output.raw, self._profile, default_index().citations(),
                                  {a["url"] for a in self._news["articles"]})
        return (False, "; ".join(problems)) if problems else (True, output)

    @task
    def write_briefing_task(self) -> Task:
        return Task(
            config=self.tasks_config["write_briefing_task"],  # type: ignore[index]
            output_file="{output_dir}/customer_{customer_id}.md",
            guardrail=self._guardrail,
            guardrail_max_retries=2,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Retention Briefing Crew."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
