"""Structured output of the Retention Briefing Writer: explanations only, never decisions."""
from pydantic import BaseModel, Field


class DecisionNote(BaseModel):
    id: str = Field(description="The id of one decision in the profile's plan, copied exactly")
    why: str = Field(description="One sentence on why this applies to this customer, from the documents")


class MarketItem(BaseModel):
    url: str = Field(description="An article url exactly as search_recent_news returned it")
    relevance: str = Field(description="One sentence on what it may mean for this customer's retention")


class BriefingNotes(BaseModel):
    summary: str = Field(description="Two sentences: who the customer is and what matters most")
    decisions: list[DecisionNote]
    market: list[MarketItem] = Field(default_factory=list, max_length=3)
