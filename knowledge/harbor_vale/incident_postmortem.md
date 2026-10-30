# Postmortem: Five Weeks of Wrong Churn Scores

> Synthetic internal document written for this course project. Harbor & Vale and every
> name, date and figure below are fictional.

Owner: Data Platform. Status: closed, actions completed.

## What happened
An upstream export changed the unit of an order value field from cents to dollars without
notice. The churn model kept running on the new numbers. For five weeks it produced scores that
looked normal but ranked customers almost at random, and the retention team spent its budget on
the wrong customers.

## Why nobody noticed
- The handoff file still had the same columns and the same row count.
- No step compared the data with an agreed description of what it should look like.
- The model's own metrics were computed on data with the same broken unit, so they looked fine.

## What we changed
1. Every handoff between the analytics team and the data science team now has a dataset
   contract: types, ranges, means, missing values, allowed values and units, checked in code.
2. The contract is locked: a new contract that differs in any number from the approved one stops
   the pipeline until a person approves the change.
3. The pipeline stops before modeling when any check fails and writes a validation report that
   says which column changed and how. A mean that moves by a factor of 10 or more is reported as
   a possible unit change.
4. The retention team only acts on scores from a run whose validation report says PASSED.

## Lessons
- A silent change is worse than messy data.
- Checks belong in code, not in someone's memory.
