"""Duplicate rows once the id column is ignored.

The dataset repeats customers under new ids: some rows are exact copies,
others copies with one value changed. Rows are grouped when they are equal
on every column, or on every column but one. The validator checks the
counts, and the Data Scientist Crew keeps each group on one side of the
train/test split so the test set never holds a copy of a training row.
"""
from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd


def _row_keys(df: pd.DataFrame) -> np.ndarray:
    return pd.util.hash_pandas_object(df, index=False).to_numpy()


def duplicate_groups(df: pd.DataFrame, id_columns: list[str]) -> np.ndarray:
    """Group label per row: rows equal on all columns, or all but one, share a label."""
    data = df.drop(columns=id_columns).reset_index(drop=True)
    parent = np.arange(len(data))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for skip in [None, *data.columns]:
        keys = _row_keys(data if skip is None else data.drop(columns=[skip]))
        first: dict[int, int] = {}
        for i, k in enumerate(keys):
            if k in first:
                parent[find(i)] = find(first[k])
            else:
                first[k] = i
    return np.array([find(i) for i in range(len(data))])


def duplicate_counts(df: pd.DataFrame, id_columns: list[str]) -> dict[str, Any]:
    data = df.drop(columns=id_columns)
    sizes = pd.Series(duplicate_groups(df, id_columns)).value_counts()
    exact = data.duplicated(keep=False)
    counts = {
        # rows that repeat an earlier row exactly (the first copy is not counted)
        "duplicate_rows_ignoring_id": int(data.duplicated().sum()),
        "rows_with_an_exact_copy": int(exact.sum()),
        # groups of rows equal on all columns, or all but one
        "duplicate_groups": int((sizes > 1).sum()),
        "rows_in_duplicate_groups": int(sizes[sizes > 1].sum()),
        "largest_duplicate_group": int(sizes.max()),
    }
    # One sentence built in code, so agents quote it instead of combining the counts.
    counts["summary"] = (
        f"{counts['rows_with_an_exact_copy']:,} rows are exact copies of another row except for "
        f"their id ({counts['duplicate_rows_ignoring_id']:,} of them repeat an earlier row under a "
        f"new id). Counting copies with one value changed as well, "
        f"{counts['rows_in_duplicate_groups']:,} rows form {counts['duplicate_groups']:,} groups of "
        f"at most {counts['largest_duplicate_group']} rows, each row with its own id."
    )
    return counts
