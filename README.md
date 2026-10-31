# Churn Pipeline: Industry-Simulated AI Product Workflow

פרויקט גמר. מערכת AI לחברת מסחר מקוון בדויה, Harbor & Vale. יש בה שני crews של סוכנים שמחוברים בחוזה נתונים שנאכף בקוד,
מודל לחיזוי נטישה, RAG על מסמכים פנימיים, חיפוש חדשות מ-48 השעות האחרונות, ותדרוך שימור בן עמוד אחד לכל לקוח.

**האפליקציה:** https://churn-pipeline-zivwais-uxs-projects.vercel.app · [מדריך שימוש והצגה](docs/demo_guide.md)

**הסיפור:** ב-Harbor & Vale, שינוי שקט מסנטים לדולרים בקובץ שעבר בין הצוותים גרם למודל ה-churn לדרג לקוחות כמעט באקראי במשך 5 שבועות.
הפרויקט בונה את ה-pipeline שהיה תופס את זה: כשהנתונים לא תואמים לחוזה, ה-Flow עוצר ומסביר מה השתנה.

## הארכיטקטורה
```
data/raw (Kaggle, 5,630 לקוחות)
   │
   ▼
Crew 1: Data Analyst (4 סוכנים) ─► clean_data.csv + dataset_contract.json
   │
   ▼
שערים בקוד: קבצים · נתונים מול חוזה · חוזה מול חוזה נעול · משתנים נדרשים
   │  נכשל ─► validation_report.md, exit 1, ו-Crew 2 לא רץ
   ▼
Crew 2: Data Scientist (4 סוכנים) ─► features, שני מודלים, כרטיס מודל
   │
   ▼
שער איכות: PR-AUC ≥ 0.80, Recall ≥ 0.60 ─► model_approved.json
   │
   ▼
Retention Briefing: המודל + תוכנית שימור בקוד + RAG + חדשות (Google News)
   │  הסוכן מסביר את ההחלטות, guardrail בקוד בודק, הקוד מרכיב ─► תדרוך בן עמוד אחד
   │
   ▼
Supabase (היסטוריית ריצות) ─► אפליקציית Flask ב-Vercel (בלי LLM)
```

**עיקרון מנחה:** הסוכנים מחליטים ומסבירים, וכלי Python מחשבים. כל מספר בטקסט של סוכן מגיע מפלט של כלי.
השערים הם קוד ולא LLM, וגם החלטות השימור (מי מקבל פנייה, באיזה ערוץ, איזו הטבה) הן קוד: `retention_plan.py` מיישם את מדריך השימור ומדיניות ההנחות, והסוכן רק מסביר.

## הרכיבים מול המטלה
| דרישה במטלה | איפה בפרויקט |
|---|---|
| מודלי שפה (LLM) | 9 סוכנים ב-CrewAI, ‏`gpt-4.1-mini`, ‏`temperature=0` |
| סוכנים עם קריאות לכלים | כל סוכן קורא לכלי Python משלו. ההרצות מתועדות ב-`docs/` |
| RAG על מסמכים פנימיים | `src/churn_pipeline/rag.py`: מדריך שימור, מדיניות הנחות, קמפיינים קודמים, מתחרים ותחקיר התקרית (`knowledge/harbor_vale/`, סינתטיים) |
| תדרוך בן עמוד אחד שמשלב RAG ומידע חי | באתר: מקלידים `CustomerID` ומקבלים מיד ציון, תוכנית שימור, כללי המסמכים (RAG) עם מקור וחדשות חיות. בנוסף, `uv run brief` מריץ סוכן שכותב תדרוך (23 קיימים) |
| תכנון מערכת: מפת RAG וכלים, סכמות, פרומפטים | דף Architecture באתר, חוזה הנתונים (Pydantic), וכל הפרומפטים ב-`config/*.yaml` |
| מודל ML (בונוס) | HistGradientBoosting מול RandomForest, נבחר לפי PR-AUC בקרוס-ולידציה |
| אפליקציה פרוסה | Flask ב-Vercel, עם היסטוריית ריצות ב-Supabase |
| חיפוש ברשת (חדשות מ-48 השעות האחרונות) | `src/churn_pipeline/news.py`: חיפוש ב-Google News RSS, בלי מפתח. רץ בזמן אמת בתדרוך באתר, ובכלי של סוכן התדרוך |

## תוצאות
- **המודל:** HistGradientBoosting. על סט בדיקה שלא שימש לבחירת המודל, PR-AUC הוא 0.864 (מול 0.168 לניחוש אקראי) ו-Recall הוא 0.667.
- **כפילויות:** 3,472 שורות הן עותקים של לקוחות שהופיעו שוב עם מזהה חדש. בחלוקה אקראית ל-train ו-test יצא PR-AUC מנופח של 0.99.
  לכן כל קבוצת עותקים נשארת בצד אחד של החלוקה.
- **שישה תרחישי שבירה,** וכולם נתפסו לפני Crew 2:
  - שינוי יחידות
  - שינוי שם עמודה
  - ערך מחוץ לטווח
  - כתיב חדש של קטגוריה
  - עמודה חסרה
  - שינוי יחידות בקובץ הגולמי. את זה תפס רק החוזה הנעול
- **תדרוכים:** 23 מתוך 23 תואמים לתוכנית השימור (`scripts/audit_briefings.py`). לפני שההחלטות עברו לקוד: 18 מתוך 23.
- **טסטים:** 145 עוברים, כולם בלי LLM.

## מבנה התיקיות
| תיקייה | תוכן |
|---|---|
| `data/raw/` | הנתונים: Kaggle E-commerce Customer Churn (CC BY-NC-SA 4.0) |
| `src/churn_pipeline/main.py` | ה-Flow: crews, שערים, router |
| `src/churn_pipeline/crews/` | `analyst_crew`, ‏`scientist_crew` ו-`briefing_crew` |
| `src/churn_pipeline/tools/` | הכלים שמחשבים |
| `src/churn_pipeline/contract/` | מבנה החוזה, הוולידטור (10 בדיקות), וזיהוי כפילויות |
| `src/churn_pipeline/gates.py` | 5 שערי הוולידציה |
| `src/churn_pipeline/rag.py` | RAG על המסמכים הפנימיים |
| `src/churn_pipeline/retention_plan.py` | מדריך השימור ומדיניות ההנחות כקוד |
| `src/churn_pipeline/news.py` | חיפוש חדשות מ-48 השעות האחרונות (Google News RSS) |
| `src/churn_pipeline/web/` | אפליקציית Flask |
| `src/churn_pipeline/run_history.py` | היסטוריית ריצות ב-Supabase |
| `contracts/dataset_contract.lock.json` | החוזה הנעול שאושר |
| `knowledge/harbor_vale/` | מסמכים פנימיים סינתטיים, ל-RAG |
| `scripts/` | תרחישי שבירה, שאלות ל-RAG, ובניית תיקיית הפריסה |
| `artifacts/latest/`, `artifacts/broken/` | התוצרים של ההרצה האחרונה ושל תרחישי השבירה |
| `deploy/web/` | התיקייה ש-Vercel פורס. נבנית מהמקור, אין לערוך בה ידנית |
| `docs/` | התכנון וההחלטות, לפי שלבים |
| `tests/` | טסטים |

## הרצה
```bash
uv sync
cp .env.example .env                 # OPENAI_API_KEY, ואופציונלית מפתחות Supabase
uv run kickoff                       # Crew 1, שערים, Crew 2, שער איכות
uv run kickoff --from-gate           # מדלג על Crew 1 (לדמו)
uv run python scripts/break_it.py    # 5 תרחישי שבירה
uv run python scripts/ask_docs.py "How much discount can an agent approve?"   # RAG
uv run brief 51809                   # תדרוך שימור ללקוח
uv run python scripts/audit_briefings.py   # כל התדרוכים תואמים לתוכנית?
uv run web                           # האפליקציה: http://127.0.0.1:5000
uv run pytest
```

## תיעוד
- [`docs/data_profile.md`](docs/data_profile.md): הנתונים וההחלטות
- [`docs/contract_spec.md`](docs/contract_spec.md): החוזה והוולידטור
- [`docs/analyst_crew.md`](docs/analyst_crew.md): Crew 1
- [`docs/scientist_crew.md`](docs/scientist_crew.md): Crew 2
- [`docs/flow.md`](docs/flow.md): ה-Flow והשערים
- [`docs/break_it.md`](docs/break_it.md): תרחישי השבירה
- [`docs/rag.md`](docs/rag.md): RAG
- [`docs/briefing.md`](docs/briefing.md): תדרוך השימור
- [`docs/app.md`](docs/app.md): האפליקציה
- [`docs/deploy.md`](docs/deploy.md): הפריסה
- [`docs/demo_guide.md`](docs/demo_guide.md): מדריך שימוש והצגה למרצה

## פערים ידועים
- **החיפוש ברשת מכסה שוק אמיתי:** Harbor & Vale בדויה, ולכן החדשות הן על מסחר מקוון בארה"ב, לפי הקטגוריה של הלקוח.
- **בדיקת התפלגות קטגוריות לא נוספה.** לכן איחוד קטגוריות נתפס רק דרך ה-SHA256 ודרך בדיקת הכפילויות.
- **רלוונטיות החדשות משתנה:** בתדרוך המיידי לפעמים מופיעה כתבה כללית. בתדרוך שסוכן כותב הוא בוחר רק כתבות רלוונטיות.
- **לחלון הזמן של `Churn` אין הגדרה,** ולכן העמודות של החודש האחרון עלולות לדלוף. זה מתועד בחוזה ובכרטיס המודל.
- **המסמכים הפנימיים של Harbor & Vale סינתטיים,** ותוצאות הקמפיינים בהם בדויות.
