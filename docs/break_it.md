# שלב 6: תרחישי שבירה (`scripts/break_it.py`)

כל תרחיש מעתיק את התוצרים של Crew 1 ל-`artifacts/broken/<scenario>/`, שובר את העותק ומריץ עליו את ה-Flow.
התוצרים האמיתיים ב-`artifacts/latest/` לא משתנים. כל תרחיש משאיר בתיקייה שלו `validation_report.md` ו-`pipeline.log`.

```bash
uv run python scripts/break_it.py                  # חמשת תרחישי המעבר, בלי LLM, כ-10 שניות לתרחיש
uv run python scripts/break_it.py unit_change      # תרחיש אחד
uv run python scripts/break_it.py raw_unit_change  # הרצה מלאה עם Crew 1, צריך OPENAI_API_KEY
```
הסקריפט מסתיים עם exit 0 רק אם ה-Flow תפס כל תרחיש שהורץ, ו-Crew 2 לא רץ באף אחד מהם.

## תרחישי מעבר (`--from-gate`)
הנתונים משתנים **אחרי** ש-Crew 1 כתב את החוזה, כמו בתקרית של Harbor & Vale. הסיכום המלא נמצא ב-`artifacts/broken/summary.md`.

| תרחיש | השבירה | השער שנכשל | ההודעה |
|---|---|---|---|
| `unit_change` | `CashbackAmount` ×100 | `contract_vs_data` | `about 100x off, possible unit change` |
| `rename_column` | `Tenure` ← `TenureMonths` | `contract_vs_data`, `required_features` | `possible rename to one of ['TenureMonths']` |
| `out_of_range` | ערך 6 ב-`SatisfactionScore` (סולם 1 עד 5) | `contract_vs_data` | `SatisfactionScore ranges 1..6, contract allows 1..5` |
| `bad_category` | כתיב חדש: `credit card` | `contract_vs_data` | `values not allowed by the contract: ['credit card']` |
| `missing_feature` | העמודה `Complain` נמחקה | `contract_vs_data`, `required_features` | `required feature 'Complain' is not in clean_data.csv` |

## הרצה מלאה: `raw_unit_change`
הקובץ הגולמי נשבר (`CashbackAmount` ×100), ו-Crew 1 רץ עליו עם ה-LLM:
- **Crew 1 בונה חוזה שתואם לנתונים השבורים,** ולכן `contract_vs_data` **עובר**.
- **רק `locked_contract` נכשל,** עם 5 הבדלים. למשל:
  - `columns.CashbackAmount.expected_mean: locked 177.223, new 17722.303`
  - `range.max: locked 324.99, new 32499.0`
  - `dtype: locked 'float', new 'int'`
- **Crew 2 לא רץ.** ההרצה האמיתית לקחה בערך 50 שניות.

**המסקנה:** בלי החוזה הנעול, אפשר "להכשיר" נתונים שבורים, פשוט בכך שבונים עליהם חוזה חדש.

## טסטים
`tests/test_break_it.py` מכיל 7 טסטים, בלי LLM. Crew 2 מוחלף במחלקה שנכשלת אם מישהו קורא לה. לכל אחד מחמשת התרחישים נבדק:
- שה-Flow נעצר בשער הנכון ועם ההודעה הנכונה
- ש-Crew 2 לא רץ
- שנכתבו דוח ולוג

בנוסף נבדק שקובץ המקור לא השתנה, ושטבלת הסיכום נכונה. את `raw_unit_change` ברמת השער בודק
`tests/test_gates.py::test_contract_rebuilt_on_broken_data_is_caught_by_the_lock`.
