# Churn Pipeline: Industry-Simulated AI Product Workflow

פרויקט גמר: CrewAI Flow שמחבר שני crews, Data Analyst ו-Data Scientist, דרך חוזה נתונים שנאכף בקוד.
כשהנתונים לא תואמים לחוזה, למשל אחרי שינוי יחידות, ה-Flow עוצר עם דוח ברור, ו-Crew 2 לא רץ.

**הסיפור:** בחברה הבדיונית Harbor & Vale, שינוי מסנטים לדולרים בקובץ שעבר בין הצוותים הרס את מודל ה-churn במשך 5 שבועות, בלי שאיש שם לב.

## מבנה
```
Crew 1 (Data Analyst) ─► שערי מעבר ─► Crew 2 (Data Scientist) ─► שער איכות
                           │                                       │
                           └─ נכשל: validation_report.md, exit 1    └─ נכשל: המודל לא מאושר, exit 1
```

| תיקייה | תוכן |
|---|---|
| `data/raw/` | הנתונים: Kaggle E-commerce Customer Churn, ‏5,630 לקוחות |
| `src/churn_pipeline/crews/` | `analyst_crew` ו-`scientist_crew`, ‏4 סוכנים בכל אחד |
| `src/churn_pipeline/tools/` | הכלים שמחשבים: הסוכנים מחליטים ומסבירים, והקוד מחשב |
| `src/churn_pipeline/contract/` | מבנה החוזה, הוולידטור (10 בדיקות), וזיהוי כפילויות |
| `src/churn_pipeline/gates.py` | 5 שערי הוולידציה של ה-Flow |
| `contracts/dataset_contract.lock.json` | החוזה הנעול שאושר |
| `artifacts/latest/` | התוצרים של ההרצה האחרונה |
| `docs/` | התכנון וההחלטות, לפי שלבים |
| `tests/` | טסטים, בלי LLM |

## הרצה
```bash
uv sync
cp .env.example .env          # להכניס OPENAI_API_KEY
uv run kickoff                # Crew 1, שערים, Crew 2, שער איכות
uv run kickoff --from-gate    # מדלג על Crew 1, לדמו
uv run pytest
```

## תיעוד
- [`docs/data_profile.md`](docs/data_profile.md): הנתונים וההחלטות
- [`docs/contract_spec.md`](docs/contract_spec.md): החוזה והוולידטור
- [`docs/analyst_crew.md`](docs/analyst_crew.md): Crew 1
- [`docs/scientist_crew.md`](docs/scientist_crew.md): Crew 2
- [`docs/flow.md`](docs/flow.md): ה-Flow והשערים

## מצב
שלבים 1 עד 5 הושלמו. בהמשך: תרחישי שבירה (`scripts/break_it.py`), אפליקציית Flask, ופריסה ל-Vercel ול-Supabase.
