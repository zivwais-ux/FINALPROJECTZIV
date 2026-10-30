# מסמך המשך: פרויקט גמר, Industry-Simulated AI Product Workflow

> העתק את המסמך הזה כהודעה ראשונה בסשן חדש. הוא מכיל את כל ההקשר שצריך כדי להמשיך מאותה נקודה.

## איך לעבוד איתי (חובה)
- **לענות לי בעברית.** קוד, הודעות commit ותוצרים של הסוכנים נכתבים באנגלית.
- **לעבוד צעד אחר צעד, ולא לקפוץ קדימה.** בסוף כל צעד מסכמים מה נעשה, מציגים את הצעד הבא, ומחכים לאישור שלי.
- **לשאול אותי לפני כל החלטה מהותית** על הנתונים או על התכנון. לא להחליט במקומי.
- **לשמור על דיוק:** כל מספר צריך לבוא מהרצה אמיתית על הנתונים, לא מהזיכרון.
- **לבצע commit ו-push** לענף `claude/amazing-goldberg-s7pi2u` בסוף כל צעד. לא לפתוח PR בלי שביקשתי.

## הפרויקט
- **repo:** `zivwais-ux/finalprojectziv`, ענף `claude/amazing-goldberg-s7pi2u`.
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

- **שלב 3 ✅ נסגר:** הרצה אמיתית עברה, והתוצרים נשמרו ב-`artifacts/latest/crew1/`. הפרטים ב-`docs/analyst_crew.md`.
- **שלב 4 ✅ נסגר (Crew 2):** התוצרים ב-`artifacts/latest/crew2/`, והפרטים ב-`docs/scientist_crew.md`.
  - **החלטות:** HistGradientBoosting ו-RandomForest, בלי Logistic Regression. חלוקה של בערך 80/20 עם stratify ו-`random_state=42`,
    שבה **כל קבוצת עותקים נשארת בצד אחד**. ספי איכות: PR-AUC לפחות 0.80 ו-Recall לפחות 0.60.
  - **ממצא:** 1,112 שורות הן עותק מדויק של שורה אחרת, בלי ה-ID (556 חוזרות על שורה קודמת). 3,472 שורות יוצרות 1,736 קבוצות
    של עותק מדויק, או עותק שבו השתנה ערך אחד. נוספה לוולידטור בדיקה 10 (כפילויות), והחוזה עודכן.
  - **תוצאה:** HistGradientBoosting נבחר, עם PR-AUC של 0.8636 ו-Recall של 0.6667 על סט הבדיקה. **35 טסטים עוברים.**
- **הרצה:** `uv run kickoff`, שמריץ את Crew 1 ואחריו את Crew 2 ומסתיים עם exit 0. ה-CLI של crewai לא מותקן בקונטיינר.

- **שלב 5 ✅ נסגר (ה-Flow המלא):** שערי מעבר, router, שער איכות, `validation_report.md`, `pipeline.log`,
  ו-`--from-gate`. הפרטים ב-`docs/flow.md`. החוזה הנעול נמצא ב-`contracts/dataset_contract.lock.json`. **45 טסטים עוברים.**

- **שלב 6 ✅ נסגר (תרחישי שבירה):** `scripts/break_it.py`, עם 5 תרחישי מעבר ו-`raw_unit_change` בהרצה מלאה.
  כל התרחישים נתפסו, ו-Crew 2 לא רץ באף אחד מהם. הפרטים ב-`docs/break_it.md`. **52 טסטים עוברים.**
- **git:** ענף `main` מכיל את כל העבודה. צריך לבחור אותו כ-default branch ב-GitHub (Settings, General).

- **המטלה (מ-Drive): Deal-Prep Copilot.** היא דורשת RAG, חיפוש ברשת ותדרוך בן עמוד אחד. ML הוא בונוס.
  הוחלט להישאר עם פרויקט ה-churn ולהוסיף את שלושת הרכיבים: 6א RAG, 6ב חיפוש ברשת, ו-6ג Crew 3 לתדרוך שימור.
- **שלב 6א ✅ נסגר (RAG):** 5 מסמכים פנימיים סינתטיים ב-`knowledge/harbor_vale/`, ו-`src/churn_pipeline/rag.py` עם הכלי
  `search_internal_docs`. בבדיקה עם embeddings אמיתיים, 6 מתוך 6 שאלות החזירו את הסעיף הנכון ראשון.
  הפרטים ב-`docs/rag.md`. **61 טסטים עוברים.**
- **המפתח של OpenAI תוקן:** אין יותר קידומת `MODEL=`, ו-`MODEL` מוגדר בסביבה.

- **שלבים 6ב ו-6ג:** הוחלט לוותר על חיפוש ברשת (6ב).
- **שלב 6ג ✅ נסגר (תדרוך שימור):** `uv run brief <CustomerID>`. סוכן אחד משלב את המודל המאושר עם ה-RAG, והמצבים
  נקבעים בקוד. guardrail בודק את הציון, הציטוטים והאורך. 23 תדרוכים נמצאים ב-`artifacts/latest/briefings/`.
  הפרטים ב-`docs/briefing.md`. **70 טסטים עוברים.**

- **שלב 7 ✅ נסגר (אפליקציית Flask):** `uv run web`, עם 6 דפים, בלי LLM ובלי crewai. הפרטים ב-`docs/app.md`. **90 טסטים עוברים.**

- **שלב 8 ✅ (פריסה):**
  - **Supabase:** פרויקט `churn-pipeline`, טבלה `pipeline_runs` עם 7 ריצות.
  - **Vercel:** פרויקט `churn-pipeline`, מ-`deploy/web`. הכתובת: https://churn-pipeline-zivwais-uxs-projects.vercel.app
  - **פרטים:** `docs/deploy.md`. **97 טסטים עוברים.**
- **האתר ציבורי:** הגנת Vercel Authentication כובתה. כל push ל-`main` נפרס לבד.
- **עיצוב מחדש:** דף פתיחה עם סיור מודרך ודרישות הקורס, ודף Architecture עם 9 הסוכנים והפרומפטים שלהם. **101 טסטים עוברים.**
- **שלב א' ✅ (תדרוך מיידי):** תדרוך לכל `CustomerID` באתר, מציונים ומתוצאות RAG שחושבו מראש (`scripts/export_instant_briefings.py`). נוסף גם דף Code.
- **שלב ב' ✅ (חיפוש ברשת):** Google News RSS בלי מפתח (`news.py`), בסוכן ובאתר. נבדק בפרודקשן. **120 טסטים עוברים.**
- **החיפוש עבר לארה"ב:** לפי בקשת המשתמש, עם החרגה של `-India -Rs`.
- **שלב ג' ✅:** 20 תדרוכים נוספים שסוכן כתב, ללקוחות שנבחרו לפי כללים (`scripts/pick_briefing_customers.py`). `news.google.com` הותר ברשת של הסביבה.
- **GitHub ✅:** ענף ברירת המחדל הוא `main`, והענף הישן `claude/friendly-heisenberg-vyhztw` נמחק.
- **Supabase מהמחשב המקומי ✅:** `SUPABASE_SECRET_KEY` נמצא ב-`.env` של המשתמש. ריצה מהמחשב שלו (unit_change, 30.10, 18:21 UTC) נרשמה בטבלה.
- **בדיקת תקינות:** הרצה מלאה (exit 0, מדדים זהים), 5 תרחישי שבירה (כולם נתפסו), וטסטים. Supabase מכיל 13 ריצות.

## השלבים שאחרי (לעבור צעד צעד, ולשאול לפני כל אחד)
- **שלב 8:** פריסה ל-Vercel ול-Supabase, ו-README סופי.

## הערות סביבה
- **רשת:** הותרו `api.openai.com`, `www.kaggle.com`, `docs.crewai.com` ו-AMP.
- **התקנה:** `npx skills add crewaiinc/skills` נחסם בהרשאות. לא חובה.
- **חבילות:** משתמשים ב-`uv`, לא ב-pip. ב-`pyproject.toml` מוגדרים pandas, openpyxl, matplotlib, seaborn, ובקבוצת dev גם pytest.
