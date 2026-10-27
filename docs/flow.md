# שלב 5: ה-Flow המלא

```
Crew 1 (Data Analyst) ─► שערי מעבר ─┬─ handoff_failed ─► validation_report.md, exit 1 (Crew 2 לא רץ)
                                     └─ handoff_passed ─► Crew 2 (Data Scientist) ─► שער איכות ─┬─ model_rejected ─► דוח, exit 1
                                                                                                └─ model_accepted ─► model_approved.json, exit 0
```

הקוד ב-`src/churn_pipeline/main.py` (`ChurnPipelineFlow`). השערים ב-`src/churn_pipeline/gates.py`: פייתון בלבד, בלי LLM.

## השערים
| # | שער | מתי | נכשל כאשר |
|---|---|---|---|
| 1 | `crew1_artifacts` | אחרי Crew 1 | אחד מ-8 התוצרים חסר או ריק. במקרה כזה שאר השערים לא רצים |
| 2 | `contract_vs_data` | אחרי Crew 1 | `clean_data.csv` מפר את `dataset_contract.json`: אחת מ-10 בדיקות הוולידטור |
| 3 | `locked_contract` | אחרי Crew 1 | החוזה החדש שונה מ-`contracts/dataset_contract.lock.json` |
| 4 | `required_features` | אחרי Crew 1 | אחד מ-18 המשתנים שבחוזה הנעול חסר ב-`clean_data.csv`, או לא שמיש בחוזה החדש |
| 5 | `model_quality` | אחרי Crew 2 | חסר תוצר של Crew 2, PR-AUC מתחת ל-0.80, Recall מתחת ל-0.60, או קבוצת עותקים בשני צידי החלוקה |

**החוזה הנעול:** עותק של החוזה שאושר, שנשמר ב-git. השער משווה את כל המספרים והכללים. הוא מתעלם רק מהטקסטים שהסוכנים
כותבים מחדש בכל הרצה: `description`, `assumptions` ו-`leakage_notes`. עמודות מושוות לפי שם, כך ששינוי שם או עמודה
שנמחקה מופיעים בהודעה בשם העמודה.

**שער 3 מכסה מקרה שהוולידטור לא מכסה:** אם הנתונים הגולמיים נשברים, Crew 1 בונה חוזה שתואם לנתונים השבורים, ולכן שער 2 עובר.
רק ההשוואה לנעילה תופסת את השינוי. למשל: `columns.CashbackAmount.expected_mean: locked 177.223, new 17722.303`.
כדי לשנות את החוזה בכוונה, מעתיקים את החוזה החדש ל-`contracts/dataset_contract.lock.json` ושומרים ב-commit.

## תוצרים של כל הרצה
- **`artifacts/latest/validation_report.md`:** הכרעה (PASSED או FAILED), טבלת שערים, וכל הבעיות לפי שער.
- **`artifacts/latest/pipeline.log`:** לוג עם זמנים, לכל שלב ולכל שער.
- **`artifacts/latest/crew2/model_approved.json`:** נכתב רק כשהמודל עבר את שער האיכות, ונמחק בכל הרצה אחרת.

## הרצה
```bash
uv run kickoff              # Crew 1, שערים, Crew 2, שער איכות
uv run kickoff --from-gate  # מדלג על Crew 1 ומתחיל בשערים, עם הקבצים שב-artifacts/latest/crew1
```
exit 0 פירושו שהכול עבר. exit 1 פירושו ששער נכשל.

## מה נבדק
- **הרצה מלאה אמיתית:** exit 0, וכל 5 השערים עברו. Crew 1 רץ כ-48 שניות ו-Crew 2 כ-47 שניות.
  Crew 1 ניסח מחדש את הטקסטים בחוזה, והשער מול הנעילה עבר כמצופה.
- **`--from-gate` אחרי ש-`CashbackAmount` הוכפל ב-100:** exit 1 תוך 15 שניות. Crew 2 לא רץ.
  הדוח מפרט את ההפרות, כולל "about 100x off, possible unit change".
- **`tests/test_gates.py`, 10 טסטים בלי LLM.** במקום Crew 2 רץ `FakeScientistCrew`, שמריץ את הכלים בלי סוכנים. נבדקים:
  - כל שער, כשהוא נשבר בכוונה
  - שטקסט של סוכנים לא מכשיל את הנעילה
  - שלושת המסלולים של ה-Flow: עובר, נעצר לפני Crew 2, ומודל שנדחה
