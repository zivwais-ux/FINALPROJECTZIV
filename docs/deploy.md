# שלב 8: פריסה ל-Vercel ול-Supabase

## Supabase: היסטוריית ריצות
- **פרויקט:** `churn-pipeline` (`phxaicuxmyjcqwxwwhtz`), באזור `eu-central-1`, בתוכנית החינמית.
- **טבלה `public.pipeline_runs`:** שורה לכל ריצה של ה-pipeline ולכל תרחיש שבירה. כל שורה כוללת:
  - זמן הריצה וסוג הריצה (`pipeline` או `scenario`), ושם התרחיש
  - ההכרעה והסטטוס
  - השערים שנכשלו, ותוצאה מלאה לכל שער (`gates`)
  - המודל, PR-AUC ו-Recall. השדות האלה ריקים כש-Crew 2 לא רץ
- **אבטחה (RLS):** מותר רק `select`, ל-`anon` ול-`authenticated`. אין policy לכתיבה, ולכן המפתח הציבורי יכול רק לקרוא,
  ורק המפתח הסודי יכול לכתוב. בדיקת האבטחה של Supabase (advisors) לא מצאה בעיות.
- **תוכן:** הטבלה מכילה את 7 הריצות הקיימות: ההרצה האחרונה (PASSED) ו-6 תרחישי השבירה (FAILED).
  השורות נבנו מהדוחות עם אותה פונקציה, `run_row`.
- **קוד:** `src/churn_pipeline/run_history.py` משתמש רק בספרייה הסטנדרטית.
  - `record_run`: נקרא בסוף כל ריצה של ה-Flow, וכותב עם `SUPABASE_SECRET_KEY`. בלי מפתח, או בלי רשת, הוא רושם בלוג "skipped" ולא מכשיל את הריצה.
  - `fetch_runs`: האפליקציה קוראת איתו את ההיסטוריה, עם `SUPABASE_PUBLISHABLE_KEY`.

## Vercel: האפליקציה
- **פרויקט:** `churn-pipeline`. מחובר ל-GitHub (`zivwais-ux/FINALPROJECTZIV`) ובונה מהענף `main`, מהתיקייה `deploy/web`.
- **כתובת:** https://churn-pipeline-zivwais-uxs-projects.vercel.app
- **למה תיקייה נפרדת:** ה-`pyproject.toml` של הפרויקט כולל את crewai ואת כל תשתית הסוכנים, ולאפליקציה זה מיותר.
  `deploy/web/` מכילה `pyproject.toml` קל (Flask, pandas, pydantic, numpy, markdown), את קוד האפליקציה והחוזה,
  את הדוחות שהאפליקציה מציגה ואת החוזה הנעול, בסך הכול 1.5MB.
  - `scripts/build_web_bundle.py` בונה את התיקייה מהמקור.
  - `tests/test_web_bundle.py` נכשל אם התיקייה לא מעודכנת, או אם נכנס אליה קוד של סוכנים.
- **בנייה:** 10 שניות, Python 3.12.
- **משתני סביבה:** `SUPABASE_URL` ו-`SUPABASE_PUBLISHABLE_KEY`.
- **הקובץ `style.css`** מוגש מ-`public/static/` דרך ה-CDN, כמו ש-Vercel ממליצה.

## מה נבדק אחרי הפריסה
- **כל הדפים** מחזירים 200. בדקתי דרך הכלי של Vercel, כי הרשת בסביבת הפיתוח חוסמת את `vercel.app` ואת `supabase.co`.
- **`/runs`** מציג את 7 הריצות מ-Supabase.
- **`style.css`** מוגש.
- **אין שגיאות runtime** בשעה הראשונה.
- **בסביבה נקייה,** עם התלויות הקלות בלבד, כל הדפים עובדים, ה-checker תופס שינוי יחידות, ו-crewai לא נטען.

## עדכון האפליקציה
```bash
uv run python scripts/build_web_bundle.py   # אחרי שינוי באפליקציה, בקוד החוזה או בתוצרים
git commit -am "..." && git push origin main  # Vercel בונה מחדש מ-main
```
כדי שהרצות מקומיות ייכתבו ל-Supabase, צריך להוסיף ל-`.env` את `SUPABASE_SECRET_KEY`.
מוציאים אותו ב-Supabase: Project Settings ← API Keys.

## פערים ידועים
- **הגנת Vercel Authentication:** הפרויקט נוצר עם `all_except_custom_domains`, ולכן כתובות `*.vercel.app` דורשות התחברות ל-Vercel.
  כדי שהאתר יהיה ציבורי, צריך לכבות את ההגנה או לחבר דומיין.
- **ריצות מסביבת הפיתוח לא נכתבות ל-Supabase:** הרשת חוסמת את `supabase.co`, ואין מפתח סודי.
  מהמחשב שלך, עם המפתח ב-`.env`, הן ייכתבו.
