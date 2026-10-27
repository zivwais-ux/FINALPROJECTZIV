# Crew 2: Data Scientist Crew

הקלט של ה-Crew הוא רק שני קבצים מ-Crew 1: `artifacts/latest/crew1/clean_data.csv` ו-`dataset_contract.json`.
התוצרים נכתבים ל-`artifacts/latest/crew2/`.

## החלטות (שלב 4)
| נושא | החלטה |
|---|---|
| מודלים | HistGradientBoosting ו-RandomForest. שניהם מטפלים ב-NaN בעצמם, ולכן אין השלמת ערכים. Logistic Regression לא נכלל |
| חלוקה | בערך 80/20, עם stratify על `Churn` ו-`random_state=42`. **כל קבוצת עותקים נשארת באותו צד של החלוקה** (`StratifiedGroupKFold(5)`, החלק הראשון הוא סט הבדיקה) |
| בחירת מודל | לפי PR-AUC ממוצע בקרוס-ולידציה של 5 חלקים, עם אותה חלוקה לקבוצות, על סט האימון בלבד. סט הבדיקה משמש פעם אחת, אחרי הבחירה |
| סף החלטה | 0.5 |
| ספי איכות | PR-AUC לפחות 0.80 ו-Recall לפחות 0.60 על סט הבדיקה. שער האיכות ב-Flow נאכף בשלב 5 |

## הממצא שהוביל לחלוקה לפי קבוצות
ב-Crew 1 נספרו 0 כפילויות, כי השורות הושוו כולל `CustomerID`, שתמיד ייחודי. בלי ה-ID:
- 1,112 שורות הן עותקים מדויקים של שורה אחרת. 556 מהן חוזרות על שורה קודמת.
- כשמוסיפים גם עותקים שבהם השתנה ערך אחד, 3,472 שורות יוצרות 1,736 קבוצות של 2 שורות.
- שיעור הנטישה בשורות האלה הוא 19.47%, לעומת 16.84% בכלל הנתונים.

בחלוקה אקראית, 193 מתוך 1,126 שורות הבדיקה היו עותק מדויק של שורת אימון. כך יצא PR-AUC של 0.993 ו-Recall של 0.921,
מספרים מנופחים. כשכל קבוצה נשארת בצד אחד, ההערכה אמינה. החישוב של הקבוצות נמצא ב-`src/churn_pipeline/contract/duplicates.py`,
ומשמש גם את Crew 1 (דוח האיכות), גם את החוזה (שדות `duplicate_rows_ignoring_id` ו-`rows_in_duplicate_groups`)
וגם את החלוקה.

## סוכנים, משימות וכלים
| סוכן | משימה | כלי | תוצר |
|---|---|---|---|
| `contract_reviewer` | `review_contract_task` | `review_contract` | `contract_review.md` |
| `feature_engineer` | `engineer_features_task` | `build_features` | `features.csv`, `feature_spec.json`, `feature_log.md` |
| `model_trainer_evaluator` | `train_evaluate_task` | `train_and_evaluate` | `model.joblib`, `evaluation_metrics.json`, `evaluation_report.md` |
| `model_card_writer` | `model_card_task` | `read_model_facts` | `model_card.md` |

- **`@before_kickoff`:** מריץ את הוולידטור בקוד לפני הסוכן הראשון. אם הנתונים לא תואמים לחוזה, ה-Crew לא מתחיל.
  גם `build_features` מסרב לרוץ במקרה כזה.
- **`build_features`:** משתנים מספריים נשארים כמו שהם, כולל 1,856 החסרים. כל קטגוריה הופכת לעמודת 0/1 לכל ערך מותר בחוזה,
  ולכן `COD` ו-`Cash on Delivery` נשארים נפרדים. יש 34 עמודות משתנים. `CustomerID` לא נכלל, ו-`duplicate_group` הוא מפתח לחלוקה ולא משתנה.
- **משפט הכפילויות** נבנה בקוד (`duplicate_counts(...)["summary"]`), והסוכנים מצטטים אותו. בהרצות הקודמות הסוכנים
  צירפו את המספרים בעצמם, וטעו: "3472 rows in 556 groups", ו-"share the same CustomerID".

## תוצאות ההרצה
| מודל | PR-AUC בקרוס-ולידציה | PR-AUC בבדיקה | Recall | Precision | ROC-AUC |
|---|---|---|---|---|---|
| **HistGradientBoosting (נבחר)** | 0.8167 ± 0.0364 | **0.8636** | **0.6667** | 0.9000 | 0.9497 |
| RandomForest | 0.8132 ± 0.0335 | 0.8447 | 0.5185 | 0.9159 | 0.9411 |

- **סטים:** 4,504 שורות אימון ו-1,126 שורות בדיקה. שיעור הנטישה בבדיקה הוא 0.1679, וזה גם ה-PR-AUC של ניחוש אקראי. אף קבוצת עותקים לא נמצאת בשני הצדדים.
- **מטריצת הבלבול בסף 0.5:** 126 נוטשים זוהו, 63 נוטשים לא זוהו, ו-14 לקוחות נאמנים סומנו בטעות.
- **עמידה בספים:** המודל עומד בשניהם.
- **המשתנים החשובים לפי permutation importance:** `Tenure`, `Complain`, `NumberOfAddress`, `SatisfactionScore`, `WarehouseToHome`.

**מה נבדק:**
- **ה-Flow** רץ עם exit 0, וכל אחד מ-8 הסוכנים בשני ה-Crews קרא לכלי שלו.
- **כל המספרים** בארבעת הטקסטים של Crew 2 נבדקו מול פלט הכלים, וכולם תואמים.
- **פער ידוע:** בסעיף Assumptions של `contract_review.md` הסוכן כתב "1,112 rows ... forming 1,736 groups", צירוף לא מדויק.
  המשפט המצוטט בסעיף Duplicates נכון.

## טסטים
`tests/test_scientist_tools.py` מכיל 8 טסטים, בלי LLM. הם בודקים:
- שהחוזה עובר
- שהמשתנים נבנים רק מהחוזה, בלי איחוד ובלי השלמה
- שהכלי מסרב לנתונים ששונו ביחידות
- שאין קבוצת עותקים בשני צידי החלוקה
- שהמודל עומד בספים
- שהאימון דטרמיניסטי
- שקובץ המודל עובד
