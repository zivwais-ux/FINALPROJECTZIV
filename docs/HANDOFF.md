# מסמך המשך: פרויקט גמר, Industry-Simulated AI Product Workflow

> העתק את המסמך הזה כהודעה ראשונה בסשן חדש. הוא מכיל את כל ההקשר שצריך כדי להמשיך מאותה נקודה.

## איך לעבוד איתי (חובה)
- **לענות לי בעברית.** קוד, הודעות commit ותוצרים של הסוכנים נכתבים באנגלית.
- **לעבוד צעד אחר צעד, ולא לקפוץ קדימה.** בסוף כל צעד מסכמים מה נעשה, מציגים את הצעד הבא, ומחכים לאישור שלי.
- **לשאול אותי לפני כל החלטה מהותית** על הנתונים או על התכנון. לא להחליט במקומי.
- **לשמור על דיוק:** כל מספר צריך לבוא מהרצה אמיתית על הנתונים, לא מהזיכרון.
- **לבצע commit ו-push** לענף `claude/friendly-heisenberg-vyhztw` בסוף כל צעד. לא לפתוח PR בלי שביקשתי.

## הפרויקט
- **repo:** `zivwais-ux/finalprojectziv`, ענף `claude/friendly-heisenberg-vyhztw`.
- **המטלה:** CrewAI Flow שמחבר שני crews, Data Analyst ו-Data Scientist, עם חוזה נתונים
  (`dataset_contract.json`) שנאכף בקוד. ה-Flow צריך לעצור עם הודעה ברורה כשהנתונים לא תואמים לחוזה,
  למשל כששונו יחידות. הסיפור: Harbor & Vale, שבה שינוי מסנטים לדולרים הרס מודל churn במשך 5 שבועות.
- **התכנון המלא נמצא ב-`docs/`:**
  - `data_profile.md`: הנתונים וההחלטות
  - `contract_spec.md`: אפיון החוזה
  - `analyst_crew.md`: Crew 1

## החלטות שהתקבלו (לא לשנות בלי לשאול)
| נושא | החלטה |
|---|---|
| צוות | עבודת יחיד |
| Dataset | Kaggle `ankitverma2010/ecommerce-customer-churn-analysis-and-prediction`, ברישיון CC BY-NC-SA 4.0. הקובץ ב-`data/raw/E Commerce Dataset.xlsx`, גיליון `E Comm`: 5,630 שורות, 20 עמודות |
| יעד | `Churn` (1 = נטש), בשיעור 16.84%. `CustomerID` משמש רק לזיהוי. 18 העמודות האחרות הן משתנים מסבירים |
| LLM | OpenAI `gpt-4.1-mini` (משתנה `MODEL`), `temperature=0`, `max_iter=8` |
| ממשק | Flask + HTML/CSS: תצוגת תוצאות ו-Contract Checker. בלי LLM ובלי crewai באפליקציה |
| פריסה | Vercel (האפליקציה) + Supabase (היסטוריית ריצות) |
| מדד למודל | PR-AUC + Recall |
| **קטגוריות** | **לא מאחדים.** `Phone`/`Mobile Phone`, `CC`/`Credit Card`, `COD`/`Cash on Delivery`, `Mobile`/`Mobile Phone` נשארים כפי שהם, כי לכתיבים השונים יש שיעורי נטישה שונים |
| **חסרים** | **לא משלימים ולא מייצרים ערכים סינטטיים.** 1,856 שורות עם בדיוק ערך חסר אחד, ב-7 עמודות. הרשימה ב-`docs/missing_values.csv` |
| **ערכים קיצוניים** | **נשארים כפי שהם.** לא מוחקים ולא חותכים |
| דליפת מידע | אין הגדרה לחלון הזמן של `Churn`. העמודות של "החודש האחרון" נשארות במודל, ומתעדים את הסיכון |
| יחידות מונחות | `Tenure` בחודשים, `WarehouseToHome` בק"מ, `CashbackAmount` ב-INR. מסומנות `unit_source: assumed` |
| טווחי החוזה | בדיוק ה-min וה-max שנמדדו |
| סבולת | 1% יחסי, גם לממוצע וגם לשיעור הנטישה |
| בדיקת התפלגות קטגוריות | **הוחלט לא להוסיף.** זה פער ידוע: איחוד קטגוריות נתפס רק בבדיקת ה-SHA256 |
| עיקרון | סוכנים מחליטים ומסבירים, וכלי פייתון מחשבים. שערי הוולידציה הם קוד, בלי LLM |
| שפת התוצרים | הסוכנים כותבים באנגלית |

## מה נעשה (12 commits)
- **התקנה:** `uv tool install crewai` (גרסה 1.15.30). הפרויקט נוצר עם `CREWAI_DMN=true crewai create flow churn_pipeline`.
- **שלב 1 (נתונים) ✅:** הקובץ הגולמי ו-`data/raw/SOURCE.md` (SHA256 `db70f1e3…bd44d`), `docs/data_profile.md`,
  `scripts/list_missing_values.py` ו-`docs/missing_values.csv`.
- **שלב 2 (חוזה) ✅:**
  - `src/churn_pipeline/contract/models.py`: מבנה החוזה (`DatasetContract`, Pydantic).
  - `src/churn_pipeline/contract/validator.py`: `validate_against_contract`, עם 9 בדיקות: עמודות (כולל זיהוי rename), סוג, חסרים, ערכים מותרים, טווח, סטיית ממוצע (כולל זיהוי "possible unit change" כשהסטייה פי 10 ומעלה), שורות ושיעור נטישה, ייחודיות ו-SHA256.
  - `tests/fixtures/contract_v1.json`: חוזה שנכתב ידנית מהאפיון.
- **שלב 3 (Crew 1), הקוד גמור:**
  - `src/churn_pipeline/crews/analyst_crew/`: 4 סוכנים ו-4 משימות:
    - `data_quality_inspector` + `profile_raw_data`
    - `data_preparation_engineer` + `export_clean_data`
    - `eda_insights_analyst` + `run_eda`
    - `contract_steward` + `build_contract`, שמחזיר `ContractText` (טקסט בלבד)
  - `@after_kickoff` מריץ את `finalize_contract`: ממזג את הטקסט עם המספרים, מעביר את החוזה בוולידטור, וכותב `dataset_contract.json` רק אם אין הפרות.
  - `src/churn_pipeline/tools/analyst_tools.py`: הכלים.
  - `src/churn_pipeline/main.py`: Flow מינימלי (`ChurnPipelineFlow`), שמריץ רק את Crew 1 ובודק שנוצרו 8 תוצרים ב-`artifacts/latest/crew1/`.
  - **טסטים: 25 עוברים** (`uv run pytest`), בלי LLM.
- **תקלה שתוקנה:** CrewAI מחליף את `warnings.warn` בגרסה שלא תואמת ל-matplotlib 3.11, ולכן `seaborn.heatmap` קורס. מפת החום מצוירת ישירות ב-matplotlib.

## הצעד הבא בדיוק: סגירת שלב 3, הרצה אמיתית
`OPENAI_API_KEY` הוגדר כמשתנה סביבה בהגדרות הסביבה, ויש לבדוק שהוא נקלט בסשן החדש.
1. לבדוק שהמשתנה קיים, **בלי להדפיס את הערך:** `env | grep -c '^OPENAI_API_KEY='`.
2. `cd` לשורש ה-repo, `uv sync`, ואז `crewai run`. אם צריך, אפשר להריץ ישירות `uv run kickoff`.
3. לבדוק את התוצרים:
   - 8 קבצים ב-`artifacts/latest/crew1/`: `quality_report.json`, `quality_summary.md`, `clean_data.csv`,
     `preparation_log.md`, `eda_report.html`, `insights.md`, `contract_numbers.json`, `dataset_contract.json`.
   - המספרים בטקסטים של הסוכנים תואמים לפלט של הכלים.
   - הסוכנים באמת קראו לכלים.
   - `dataset_contract.json` עובר את הוולידטור.
4. להציג לי את התוצאות בעברית, ואם יש בעיות, לתקן.
5. commit ל-`artifacts/latest/crew1/` (בלי `.env`), עדכון `docs/analyst_crew.md` ו-push. שלב 3 נסגר.

## השלבים שאחרי (לעבור צעד צעד, ולשאול לפני כל אחד)
- **שלב 4, Crew 2 (Data Scientist):** 4 סוכנים: Contract Reviewer, Feature Engineer, Model Trainer & Evaluator, Model Card Writer.
  - הקלט שלו הוא רק `clean_data.csv` ו-`dataset_contract.json`.
  - לפחות 2 וריאציות מודל, שיודעות לעבוד עם NaN (למשל HistGradientBoosting). לגבי Logistic Regression, צריך לשאול אותי.
  - תוצרים: `features.csv`, `model.joblib`, `evaluation_report.md`, `model_card.md`.
- **שלב 5, ה-Flow המלא:**
  - שערים: קבצים קיימים, חוזה מול נתונים, השוואה לחוזה נעול (`contracts/dataset_contract.lock.json`), features נדרשים, איכות המודל.
  - router בין pass ל-fail. במקרה של fail: `validation_report.md` ו-exit 1, ו-Crew 2 לא רץ.
  - לוגים, ומצב `--from-gate` שמדלג על Crew 1, לדמו.
- **שלב 6:** סקריפט `scripts/break_it.py`, עם תרחישים: unit_change, rename_column, out_of_range, bad_category ו-missing_feature, וטסט לכל תרחיש.
- **שלב 7:** אפליקציית Flask, עם הדפים `/`, `/analyst`, `/scientist`, `/runs` ו-`/checker`.
- **שלב 8:** פריסה ל-Vercel ול-Supabase, ו-README סופי.

## הערות סביבה
- **רשת:** הותרו `api.openai.com`, `www.kaggle.com`, `docs.crewai.com` ו-AMP.
- **התקנה:** `npx skills add crewaiinc/skills` נחסם בהרשאות. לא חובה.
- **חבילות:** משתמשים ב-`uv`, לא ב-pip. ב-`pyproject.toml` מוגדרים pandas, openpyxl, matplotlib, seaborn, ובקבוצת dev גם pytest.
