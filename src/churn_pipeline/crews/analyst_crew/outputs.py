"""Structured output of the Contract Steward: text only, never numbers."""
from pydantic import BaseModel, Field


class ColumnDescription(BaseModel):
    name: str
    description: str


class ContractText(BaseModel):
    column_descriptions: list[ColumnDescription] = Field(min_length=1)
    assumptions: list[str] = Field(min_length=1)
    leakage_notes: list[str] = Field(min_length=1)
