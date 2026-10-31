import os
import re
from pathlib import Path

from crewai import LLM, Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, after_kickoff, agent, before_kickoff, crew, task

from churn_pipeline.crews.briefing_crew.outputs import BriefingNotes
from churn_pipeline.news import SEEN_ARTICLES, search_recent_news
from churn_pipeline.rag import search_internal_docs_tool
from churn_pipeline.retention_plan import all_citations
from churn_pipeline.tools.briefing_tools import (
    customer_risk_profile,
    customer_risk_profile_tool,
    search_recent_news_tool,
)

MAX_WORDS = 650  # about one printed page
MAX_WHY_WORDS = 25
MAX_SUMMARY_WORDS = 50
MAX_RELEVANCE_WORDS = 30
BAND_RULE = {"high": "0.70 or higher", "medium": "0.40 to 0.70", "low": "below 0.40"}
# An explanation must not walk back a decision; these phrases did in earlier,
# free-form briefings (scripts/audit_briefings.py).
CONTRADICTIONS = re.compile(r"no individual outreach|regular newsletter|"
                            r"(not be contacted|do not contact (this|the) customer)(?! more than)", re.I)
# Only these say whether to contact; the frequency note rightly says "not more than twice".
CONTACT_IDS = {"contact", "channel"}


def _llm() -> LLM:
    # temperature=0 keeps agent wording as repeatable as the model allows;
    # the numbers and the decisions always come from code.
    return LLM(model=os.getenv("MODEL", "gpt-4.1-mini"), temperature=0)


def _words(text: str) -> int:
    """Words a reader reads: a markdown link's target URL does not count."""
    return len(re.findall(r"\S+", re.sub(r"\]\([^)]*\)", "]", text)))


def check_notes(notes: BriefingNotes, profile: dict, articles: dict[str, dict]) -> list[str]:
    """Problems that make the agent's notes unusable; empty means the briefing may be rendered.

    The decisions themselves come from the plan, so this checks that the agent
    explained every one of them, explained nothing else, did not walk any back,
    and linked only articles the news search returned.
    """
    plan = profile["plan"]
    problems = []
    expected = [d["id"] for d in plan["decisions"]]
    given = [n.id for n in notes.decisions]
    missing, extra = [i for i in expected if i not in given], [i for i in given if i not in expected]
    if missing:
        problems.append(f"explain every decision in the plan; missing ids: {missing}")
    if extra:
        problems.append(f"these ids are not decisions in the plan: {extra}")
    for n in notes.decisions:
        if not n.why.strip():
            problems.append(f"the explanation for {n.id} is empty")
        elif _words(n.why) > MAX_WHY_WORDS:
            problems.append(f"the explanation for {n.id} is longer than {MAX_WHY_WORDS} words")
        if plan["contact"] and n.id in CONTACT_IDS and CONTRADICTIONS.search(n.why):
            problems.append(f"the explanation for {n.id} contradicts the plan: this customer must be contacted")
    if plan["contact"] and CONTRADICTIONS.search(notes.summary):
        problems.append("the summary contradicts the plan: this customer must be contacted")
    if _words(notes.summary) > MAX_SUMMARY_WORDS:
        problems.append(f"the summary is longer than {MAX_SUMMARY_WORDS} words")
    for m in notes.market:
        if _words(m.relevance) > MAX_RELEVANCE_WORDS:
            problems.append(f"a market relevance note is longer than {MAX_RELEVANCE_WORDS} words")
    invented = [m.url for m in notes.market if m.url not in articles]
    if invented:
        problems.append(f"these links did not come from search_recent_news: {invented[:3]}; "
                        "copy url exactly from the search result")
    if _words(render_briefing(profile, notes, articles)) > MAX_WORDS:
        problems.append(f"the briefing is longer than {MAX_WORDS} words; shorten the explanations")
    return problems


def render_briefing(profile: dict, notes: BriefingNotes, articles: dict[str, dict]) -> str:
    """The briefing in markdown. Facts, score and decisions come from code; the agent's
    text fills only the summary, the "why" of each decision and the news relevance."""
    plan = profile["plan"]
    why = {n.id: n.why.strip() for n in notes.decisions}
    band = profile["risk_band"]
    facts = " · ".join(f"{k} {'missing' if v is None else v}" for k, v in profile["key_facts"].items())
    lines = [f"# Retention briefing: customer {profile['customer_id']}", "", notes.summary.strip(), "",
             "## Customer snapshot", f"- {facts}",
             "", "## Churn risk",
             f"- Risk score: {profile['risk_score']:.2f} ({band} risk band: {BAND_RULE[band]}). "
             f"{profile['score_note'][0].upper()}{profile['score_note'][1:]}.",
             "", "## Plan (decided in code from the playbook and the discount policy)"]
    for d in plan["decisions"]:
        lines.append(f"- **{d['label']}:** {d['value']}. {why.get(d['id'], '')} {' '.join(d['cites'])}".rstrip())
    lines += ["", "## Do not"] + [f"- {n['value']} {' '.join(n['cites'])}" for n in plan["never"]]
    lines += ["", "## Market now (last 48 hours)"]
    items = [(articles[m.url], m.relevance.strip()) for m in notes.market if m.url in articles]
    if items:
        lines += [f"- [{a['title']}]({a['url']}), {a['source']}, {a['published']}. {rel}" for a, rel in items]
    else:
        lines.append("- No market news from the last 48 hours was available.")
    lines += ["", "## Sources", " · ".join(sorted(all_citations(plan)))]
    return "\n".join(lines) + "\n"


@CrewBase
class BriefingCrew:
    """Retention briefing: approved churn model + retention plan + internal documents (RAG) + news."""

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
            max_iter=10,
            verbose=True,
        )

    @before_kickoff
    def require_customer(self, inputs: dict) -> dict:
        """Score the customer and decide the plan in code first: no approved model or
        unknown customer, no briefing."""
        self._profile = customer_risk_profile(int(inputs["customer_id"]))
        # Searched here first so the news is known before the agent writes.
        search_recent_news(self._profile["news_query"])
        self._out = Path(inputs["output_dir"]) / f"customer_{inputs['customer_id']}.md"
        self._out.parent.mkdir(parents=True, exist_ok=True)
        return inputs

    def _guardrail(self, output):
        notes = output.pydantic
        if not isinstance(notes, BriefingNotes):
            return False, "return the structured BriefingNotes"
        problems = check_notes(notes, self._profile, SEEN_ARTICLES)
        return (False, "; ".join(problems)) if problems else (True, output)

    @after_kickoff
    def write_briefing(self, result):
        self._out.write_text(render_briefing(self._profile, result.pydantic, SEEN_ARTICLES), encoding="utf-8")
        return result

    @task
    def write_briefing_task(self) -> Task:
        return Task(
            config=self.tasks_config["write_briefing_task"],  # type: ignore[index]
            output_pydantic=BriefingNotes,
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
