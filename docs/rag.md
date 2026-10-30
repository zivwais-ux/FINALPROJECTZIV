# שלב 6א: RAG על המסמכים הפנימיים של Harbor & Vale

רכיב ה-RAG שהמטלה דורשת. הוא מחפש במסמכים הפנימיים של החברה ומחזיר את הקטעים הרלוונטיים, עם שם הקובץ והסעיף לציטוט.
בשלב 6ג סוכן בתדרוך השימור ישתמש בו.

## המסמכים
כל המסמכים ב-`knowledge/harbor_vale/` **סינתטיים**. כתבתי אותם לפרויקט, ובראש כל אחד מהם יש סימון שהחברה והמספרים בדויים.
גם המתחרים בדויים: CartNest, ‏BazaarLane ו-QuickKart.

| קובץ | תוכן |
|---|---|
| `retention_playbook.md` | למי פונים קודם, לקוחות חדשים, תלונות ("resolve before you reward"), לקוחות COD, ערוצי פנייה, ומה אסור |
| `discount_policy.md` | תקציב חודשי, תקרות לכל לקוח, ורמות אישור |
| `past_campaigns.md` | ארבעה קמפיינים קודמים והלקחים מהם. התוצאות בדויות ולא חושבו מהנתונים |
| `competitor_offers.md` | הצעות של מתחרים, ואיך להשתמש בהן |
| `incident_postmortem.md` | תחקיר תקרית המעבר מסנטים לדולרים, והסיבות לחוזה ולשערים |

בנוסף נכללים התוצרים האחרונים של ה-crews: `artifacts/latest/crew1/insights.md` ו-`artifacts/latest/crew2/model_card.md`.
בסך הכול יש 40 קטעים מ-7 קבצים.

## איך זה עובד (`src/churn_pipeline/rag.py`)
1. **פיצול:** כל קובץ markdown מתחלק לקטע אחד לכל כותרת `## `. כל קטע מתחיל ב-"כותרת המסמך > שם הסעיף", כך שגם כשהוא נשלף לבד ברור מאיפה הוא.
2. **embeddings:** מחושבים עם OpenAI `text-embedding-3-small`, על אותו `OPENAI_API_KEY`, בלי שירות נוסף.
3. **חיפוש:** דמיון קוסינוס עם numpy. מוחזרים 4 הקטעים הקרובים ביותר, עם `source`, ‏`section`, ‏`score` ו-`text`.
4. **מטמון:** הווקטורים נשמרים ב-`artifacts/rag/index.json` לפי ה-SHA256 של טקסט הקטע. רק קטעים חדשים או ששונו מחושבים מחדש.
   אם מודל ה-embedding משתנה, המטמון כולו נבנה מחדש. הקובץ לא נשמר ב-git.
5. **הכלי לסוכנים:** `search_internal_docs`. הכלי רק מחפש, והסוכן מחליט מה לשאול ואיך להשתמש בתשובה.

**למה מימוש עצמאי ולא knowledge sources של CrewAI:** כל תוצאה מגיעה עם מקור לציטוט, ואפשר לבדוק את הכול בלי רשת.

## בדיקה עם embeddings אמיתיים
`uv run python scripts/ask_docs.py "<שאלה>"`. בכל 6 השאלות, הקטע הנכון חזר ראשון:

| שאלה | הקטע הראשון | ציון |
|---|---|---|
| How much discount can an agent approve without a team lead? | `discount_policy.md > Approval levels` | 0.52 |
| A customer complained last week. Should we send a coupon right away? | `retention_playbook.md > Customers who complained` | 0.56 |
| What retention offer works for customers who pay cash on delivery? | `retention_playbook.md > Cash on delivery (COD) customers` | 0.67 |
| Which competitor targets our phone buyers? | `competitor_offers.md > CartNest` | 0.57 |
| Why did the old churn model fail for five weeks? | `incident_postmortem.md > What happened` | 0.60 |
| What PR-AUC and recall did the churn model reach on the test set? | `model_card.md > Metrics` | 0.63 |

## טסטים
`tests/test_rag.py` מכיל 9 טסטים, בלי רשת. במקום OpenAI רץ embedder מזויף שסופר מילים. כך נבדקים הפיצול, הדירוג והמטמון,
אבל לא איכות ה-embeddings האמיתיים, שאותה בדקה הטבלה למעלה. נבדקים:
- שכל מסמך מסומן כסינתטי
- שכל קובץ מתפצל לקטעים לפי הסעיפים
- שהחיפוש מדרג ראשון את הסעיף הנכון
- שהמטמון מחשב מחדש רק קטע ששונה
- שהמטמון מתעלם מווקטורים של מודל embedding אחר
- שהבנייה מדלגת על קבצים שעדיין לא נוצרו
