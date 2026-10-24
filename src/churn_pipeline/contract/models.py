"""Pydantic schema for dataset_contract.json.

The contract is the only interface between the Data Analyst Crew and the
Data Scientist Crew: it describes clean_data.csv column by column.
"""
from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, model_validator

Role = Literal["id", "target", "feature"]
DType = Literal["int", "float", "binary", "category"]
UnitSource = Literal["data_dict", "assumed"]


class NumericRange(BaseModel):
    min: float
    max: float

    @model_validator(mode="after")
    def _min_le_max(self) -> NumericRange:
        if self.min > self.max:
            raise ValueError(f"range min {self.min} is greater than max {self.max}")
        return self


class ColumnSpec(BaseModel):
    name: str
    role: Role
    dtype: DType
    description: str = ""
    unit: str | None = None
    unit_source: UnitSource | None = None
    expected_null_count: int = Field(default=0, ge=0)
    unique: bool = False
    range: NumericRange | None = None
    expected_mean: float | None = None
    expected_std: float | None = None
    allowed_values: list[str] | None = None

    @model_validator(mode="after")
    def _fields_match_dtype(self) -> ColumnSpec:
        if self.dtype == "category":
            if not self.allowed_values:
                raise ValueError(f"{self.name}: category column needs allowed_values")
            if self.range is not None or self.expected_mean is not None:
                raise ValueError(f"{self.name}: category column cannot have range or expected_mean")
        else:
            if self.allowed_values is not None:
                raise ValueError(f"{self.name}: numeric column cannot have allowed_values")
            if self.range is None:
                raise ValueError(f"{self.name}: numeric column needs a range")
        return self


class DatasetInfo(BaseModel):
    name: str
    file: str
    sha256: str | None = None
    row_count: int = Field(gt=0)


class TargetSpec(BaseModel):
    name: str
    positive_class: int = 1
    expected_rate: float = Field(ge=0, le=1)


class Tolerances(BaseModel):
    mean_rel: float = Field(default=0.01, gt=0)
    target_rate_rel: float = Field(default=0.01, gt=0)
    unit_change_factor: float = Field(default=10.0, gt=1)


class DatasetContract(BaseModel):
    contract_version: str
    dataset: DatasetInfo
    target: TargetSpec
    tolerances: Tolerances = Tolerances()
    columns: list[ColumnSpec]
    forbidden_features: list[str] = []
    assumptions: list[str] = []
    leakage_notes: list[str] = []

    @model_validator(mode="after")
    def _consistent(self) -> DatasetContract:
        names = [c.name for c in self.columns]
        dupes = sorted({n for n in names if names.count(n) > 1})
        if dupes:
            raise ValueError(f"duplicate column names in contract: {dupes}")
        by_name = {c.name: c for c in self.columns}
        target = by_name.get(self.target.name)
        if target is None or target.role != "target":
            raise ValueError(f"target {self.target.name!r} must be a column with role 'target'")
        missing = [f for f in self.forbidden_features if f not in by_name]
        if missing:
            raise ValueError(f"forbidden_features not in columns: {missing}")
        return self

    def column(self, name: str) -> ColumnSpec:
        return next(c for c in self.columns if c.name == name)

    @property
    def feature_names(self) -> list[str]:
        return [c.name for c in self.columns if c.role == "feature"]


def load_contract(path: str | Path) -> DatasetContract:
    return DatasetContract.model_validate_json(Path(path).read_text(encoding="utf-8"))
