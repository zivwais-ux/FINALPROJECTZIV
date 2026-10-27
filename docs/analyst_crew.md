# שלב 3: Data Analyst Crew

## מבנה
- `src/churn_pipeline/crews/analyst_crew/`: ה-crew עצמו. נוצר עם `crewai flow add-crew analyst_crew`.
- `src/churn_pipeline/tools/analyst_tools.py`: הכלים. פייתון טהור, בלי LLM.
- `src/churn_pipeline/main.py`: Flow מינימלי שמריץ רק את Crew 1. ה-Flow המלא ייבנה בשלב 5.

## סוכנים, משימות וכלים
| # | סוכן | משימה | כלי | קבצים שהכלי כותב | קובץ שהסוכן כותב |
|---|---|---|---|---|---|
| 1 | `data_quality_inspector` | `inspect_raw_data_task` | `profile_raw_data` | `quality_report.json` | `quality_summary.md` |
| 2 | `data_preparation_engineer` | `prepare_clean_data_task` | `export_clean_data` | `clean_data.csv` | `preparation_log.md` |
| 3 | `eda_insights_analyst` | `eda_task` | `run_eda` | `eda_report.html` | `insights.md` |
| 4 | `contract_steward` | `publish_contract_task` | `build_contract` | `contract_numbers.json` | מחזיר `ContractText` (טקסט בלבד) |

**הגדרות משותפות לכל הסוכנים:** `gpt-4.1-mini` (מהמשתנה `MODEL`), `temperature=0`, `max_iter=8`.

**אחרי שה-crew מסיים** (`@after_kickoff`): `finalize_contract` ממזג את הטקסט של ה-Contract Steward עם המספרים של
`build_contract`, ובודק את החוזה מול `clean_data.csv` עם הוולידטור משלב 2. רק אם אין הפרות נכתב
`dataset_contract.json`. אחרת נזרקת שגיאה, ולא נמסר חוזה שגוי.

**כל התוצרים** נכתבים לתיקייה `artifacts/latest/crew1/`, שנקבעת ב-Flow.

## פרטים חשובים בכלים
- **`export_clean_data`:** כותב CSV בלי שום שינוי, קורא אותו מחדש ומשווה לגולמי תא מול תא, גם בערכים וגם במיקום החסרים.
  התוצאה: `identical_to_raw: true` ו-1,856 ערכים חסרים שנשמרו. ה-SHA256 של הקובץ זהה בין ריצות.
- **`profile_raw_data`:** חריגים לפי כלל קבוע, ערך מחוץ ל-Q1−3·IQR עד Q3+3·IQR. לפי הכלל הזה:

  | עמודה | ערכים חריגים לפי הכלל |
  |---|---|
  | `Tenure` | 2 |
  | `WarehouseToHome` | 2 |
  | `NumberOfAddress` | 4 |
  | `DaySinceLastOrder` | 3 |
  | `CouponUsed` | 303 |
  | `OrderCount` | 263 |

  ב-`CouponUsed` וב-`OrderCount` רוב הערכים צפופים ליד 1 עד 2, ולכן הכלל מסמן הרבה ערכים. הם מסומנים בדוח בלבד, ולא מוסרים
  (לפי ההחלטה מצעד 1.3).
- **`build_contract`:** היחידות לקוחות מטבלה קבועה בקוד (`UNITS`), שמשקפת את ההחלטות מ-`docs/contract_spec.md`.
  טסט מוודא שכל המספרים שהכלי מחשב זהים לאפיון שנכתב ידנית ב-`tests/fixtures/contract_v1.json`.

## תקלה שנמצאה ותוקנה
**הבעיה:** CrewAI מחליף את `warnings.warn` בגרסה שלא תומכת בפרמטר `skip_file_prefixes`, ש-matplotlib 3.11 משתמש בו.
לכן כל אזהרת deprecation של matplotlib מפילה את הכלי. `seaborn.heatmap` מפעיל אזהרה כזו.

**הפתרון:** מפת החום של הקורלציות מצוירת ישירות ב-matplotlib.

## טסטים
`tests/test_analyst_tools.py` מכיל 8 טסטים, בלי LLM. הם בודקים:
- שכל כלי כותב את הקובץ שלו
- שהייצוא זהה לגולמי ודטרמיניסטי
- שמספרי החוזה תואמים לאפיון
- שחוזה ממוזג עובר את הוולידטור
- שחוזה לא נכתב אם חסר תיאור לעמודה, או אם `clean_data.csv` השתנה, למשל ביחידות ×100

## הרצה
```bash
cp .env.example .env    # ולהכניס OPENAI_API_KEY
crewai run
```

## הרצה אמיתית (סגירת שלב 3)
הרצה עם `uv run kickoff` ו-`gpt-4.1-mini`, ב-`temperature=0`. ה-Flow הסתיים עם exit 0, והתוצרים נשמרו ב-`artifacts/latest/crew1/`.

**מה נבדק:**
- **כל 8 התוצרים קיימים:** `quality_report.json`, `quality_summary.md`, `clean_data.csv`, `preparation_log.md`,
  `eda_report.html`, `insights.md`, `contract_numbers.json`, `dataset_contract.json`.
- **כל סוכן קרא לכלי שלו פעם אחת:** `profile_raw_data`, `export_clean_data`, `run_eda` ו-`build_contract`.
- **`dataset_contract.json` עובר את `validate_against_contract`** מול `clean_data.csv`, עם 0 הפרות.
- **`clean_data.csv` זהה לגיליון `E Comm`:** 5,630 שורות ו-20 עמודות. ה-SHA256 שלו הוא `e0c951d4…f847019`.
- **המספרים בטקסטים:** כל המספרים ב-`quality_summary.md`, ב-`preparation_log.md` וב-`insights.md` חושבו מחדש מהקובץ הגולמי
  בסקריפט נפרד. כולם תואמים, חוץ משלושה מקרים:
  - הפרשים שהסוכן חישב, ושנבדקו ידנית (28.77−15.44=13.33)
  - עיגול שהסוכן כתב במפורש ("~27%")
  - ספירות ערכים קיצוניים לפי כלל 3×IQR, שתואמות ל-`quality_report.json`

**תיקונים שנדרשו אחרי ההרצה הראשונה:**
1. **הפרומפט של `eda_task`** הציג כתיבים שונים כ"דפוס שאולי נובע מאיסוף הנתונים", והסוכנים כתבו שזו "כנראה הקלדה לא עקבית".
   זה סותר את ההחלטה לא לאחד קטגוריות. הפרומפטים של `inspect_raw_data_task` ושל `eda_task` מנחים עכשיו להציג את הכתיבים
   כקטגוריות נפרדות עם שני שיעורי הנטישה, בלי לנחש את הסיבה.
2. **הסוכן כתב "lowest satisfaction score (5)".** במילון הנתונים אין כיוון לסולם, ובנתונים שיעור הנטישה עולה עם הציון:
   11.51% בציון 1 לעומת 23.83% בציון 5. הפרומפט מנחה עכשיו לכתוב "score 5", ולא "נמוך" או "גבוה".
3. **`kickoff()` החזיר dict ל-`sys.exit`,** ולכן ריצה מוצלחת הסתיימה עם exit 1. הפונקציה לא מחזירה ערך יותר.

## עדכון בשלב 4: כפילויות בלי `CustomerID`
`profile_raw_data` השווה שורות שלמות, כולל ה-ID הייחודי, ולכן דיווח על 0 כפילויות. עכשיו הוא מחזיר גם
`duplicates_ignoring_id`: 1,112 שורות הן עותק מדויק של שורה אחרת, חוץ מה-ID, ו-556 מהן חוזרות על שורה קודמת.
כשמוסיפים עותקים שבהם השתנה ערך אחד, 3,472 שורות יוצרות 1,736 קבוצות. שיעור הנטישה בקבוצות האלה הוא 19.47%.
- **החוזה** כולל את `duplicate_rows_ignoring_id` (556) ואת `rows_in_duplicate_groups` (3,472), והוולידטור בודק אותם (בדיקה 10).
- **`run_eda`** מחזיר משפט כפילויות שנבנה בקוד. הסוכנים מצטטים אותו ב-`quality_summary.md` וב-`insights.md`.
- **הנחיות לסוכנים:** ב-`build_contract` הסוכן מוסיף הנחה ("duplicate rows kept") והערת דליפה: עותקים דולפים בין
  train ל-test, אלא אם כל קבוצה נשארת בצד אחד.
