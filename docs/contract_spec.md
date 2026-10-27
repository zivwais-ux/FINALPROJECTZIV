# אפיון חוזה הנתונים (`dataset_contract.json`)

החוזה מתאר את `clean_data.csv`, הפלט של Crew 1. זה הדבר היחיד ש-Crew 2 רשאי להניח על הנתונים.
כל המספרים כאן חושבו מהקובץ הגולמי. מכיוון שהוחלט לא לשנות את הנתונים (ראו `docs/data_profile.md`),
הם זהים לערכים ב-`clean_data.csv`.

## צעד 2.1: הגדרת העמודות

### כללים
- **טווח (`range`):** ה-min וה-max שנמדדו בפועל. כל ערך מחוץ לטווח הוא הפרה.
- **סוג "שלם":** בעמודה עם ערכים חסרים, pandas שומר את העמודה כ-float. החוזה מגדיר אותה כמספר שלם, והוולידטור
  בודק שכל ערך קיים הוא שלם.
- **חסרים (`expected_null_count`):** המספר המדויק שנמדד. כל שינוי במספר הוא הפרה.
- **יחידות:** כשהיחידה לא מצוינת במקור, נכתבת יחידה סבירה ומסומנת `unit_source: "assumed"`.
  כשהיחידה נלקחה מ-`Data Dict`, היא מסומנת `unit_source: "data_dict"`.

### עמודות מספריות
| עמודה | תפקיד | סוג | יחידה | מקור היחידה | min | max | ממוצע | סטיית תקן | חסרים |
|---|---|---|---|---|---|---|---|---|---|
| `CustomerID` | id | int, ייחודי | לא רלוונטי | לא רלוונטי | 50001 | 55630 | לא רלוונטי | לא רלוונטי | 0 |
| `Churn` | target | binary | flag | data_dict | 0 | 1 | 0.1684 | 0.3742 | 0 |
| `Tenure` | feature | int | months | **assumed** | 0 | 61 | 10.1899 | 8.5572 | 264 |
| `CityTier` | feature (ordinal) | int | tier | data_dict | 1 | 3 | 1.6547 | 0.9154 | 0 |
| `WarehouseToHome` | feature | int | km | **assumed** | 5 | 127 | 15.6399 | 8.5315 | 251 |
| `HourSpendOnApp` | feature | int | hours | data_dict | 0 | 5 | 2.9315 | 0.7219 | 255 |
| `NumberOfDeviceRegistered` | feature | int | count | data_dict | 1 | 6 | 3.6890 | 1.0240 | 0 |
| `SatisfactionScore` | feature (ordinal) | int | score | data_dict | 1 | 5 | 3.0668 | 1.3802 | 0 |
| `NumberOfAddress` | feature | int | count | data_dict | 1 | 22 | 4.2140 | 2.5836 | 0 |
| `Complain` | feature | binary | flag (last month) | data_dict | 0 | 1 | 0.2849 | 0.4514 | 0 |
| `OrderAmountHikeFromlastYear` | feature | int | percent | data_dict | 11 | 26 | 15.7079 | 3.6755 | 265 |
| `CouponUsed` | feature | int | count (last month) | data_dict | 0 | 16 | 1.7510 | 1.8946 | 256 |
| `OrderCount` | feature | int | count (last month) | data_dict | 1 | 16 | 3.0080 | 2.9397 | 258 |
| `DaySinceLastOrder` | feature | int | days | data_dict | 0 | 46 | 4.5435 | 3.6544 | 307 |
| `CashbackAmount` | feature | float | INR (last month average) | **assumed** | 0 | 324.99 | 177.2230 | 49.2070 | 0 |

**ההיגיון מאחורי היחידות המונחות:**
- **`Tenure` בחודשים:** טווח של 0 עד 61 וחציון 9 מתאימים לוותק בחודשים. בשנים זה היה בלתי סביר.
- **`WarehouseToHome` בק"מ:** טווח של 5 עד 36, לא כולל שני הערכים החריגים, מתאים למרחק משלוח עירוני בק"מ.
- **`CashbackAmount` ברופי הודי (INR):** אמצעי התשלום `UPI` ו-`COD` מעידים על שוק הודי.

### עמודות קטגוריאליות (הכתיבים המקוריים, בלי איחוד)
| עמודה | ערכים מותרים | חסרים |
|---|---|---|
| `PreferredLoginDevice` | `Computer`, `Mobile Phone`, `Phone` | 0 |
| `PreferredPaymentMode` | `CC`, `COD`, `Cash on Delivery`, `Credit Card`, `Debit Card`, `E wallet`, `UPI` | 0 |
| `Gender` | `Female`, `Male` | 0 |
| `PreferedOrderCat` | `Fashion`, `Grocery`, `Laptop & Accessory`, `Mobile`, `Mobile Phone`, `Others` | 0 |
| `MaritalStatus` | `Divorced`, `Married`, `Single` | 0 |

### ברמת הקובץ
| שדה | ערך |
|---|---|
| `row_count` | 5,630 |
| שיעור `Churn` | 0.1684 |
| `forbidden_features` | `CustomerID` |
| `duplicate_rows_ignoring_id` | 556 (שורות שחוזרות על שורה קודמת, בלי `CustomerID`) |
| `rows_in_duplicate_groups` | 3,472 (שורות בקבוצות של עותק מדויק, או עותק שבו השתנה ערך אחד) |
| `sha256` | של `clean_data.csv`, נקבע כשהקובץ נוצר |
| `assumptions` | בלי איחוד קטגוריות, בלי השלמת חסרים, ערכים קיצוניים נשמרים, 3 יחידות מונחות |
| `leakage_notes` | אין הגדרה לחלון הזמן של `Churn`. העמודות של החודש האחרון (`Complain`, `CouponUsed`, `OrderCount`, `CashbackAmount`, `PreferedOrderCat`) עלולות לדלוף |

## צעד 2.2: הבדיקות של הוולידטור

הוולידטור מריץ **את כל הבדיקות**, גם אחרי שאחת מהן נכשלה, ומחזיר רשימה מלאה של הפרות.
כל הפרה כוללת את העמודה, את הבדיקה, את הערך הצפוי, את הערך בפועל, והודעה קריאה.

| # | בדיקה | כלל הכשל |
|---|---|---|
| 1 | עמודות | עמודה מהחוזה חסרה בקובץ, או שיש בקובץ עמודה שלא בחוזה. כשעמודה חסרה ועמודה חדשה מופיעות יחד, ההודעה מציינת "possible rename" |
| 2 | סוג | עמודה מספרית מכילה ערך לא מספרי, או שעמודה מסוג int מכילה ערך לא שלם (בהתעלמות מ-NaN) |
| 3 | חסרים | מספר ה-NaN בעמודה שונה מ-`expected_null_count` |
| 4 | ערכים מותרים | יש ערך שאינו ב-`allowed_values` |
| 5 | טווח | יש ערך קטן מ-`min` או גדול מ-`max` |
| 6 | סטיית ממוצע | `abs(mean - expected_mean) / abs(expected_mean) > 0.01`. הממוצע מחושב על הערכים הקיימים בלבד. אם הסטייה היא פי 10 ומעלה, ההודעה מציינת "possible unit change" |
| 7 | שורות ויעד | `row_count` שונה מהצפוי, או ששיעור `Churn` סוטה ביותר מ-1% יחסי (0.1684 ± 0.0017) |
| 8 | ייחודיות | יש ערך כפול בעמודה עם `unique: true` (`CustomerID`) |
| 9 | טביעת אצבע | ה-SHA256 של `clean_data.csv` שונה מ-`dataset.sha256` |
| 10 | כפילויות | מספר השורות הכפולות בלי ה-ID, או מספר השורות בקבוצות עותקים, שונה מהחוזה (`contract/duplicates.py`). נוסף בשלב 4 |

**סבולת:** 1% יחסי, גם לממוצע וגם לשיעור הנטישה. הקובץ קבוע, ולכן כל שינוי אמיתי צריך להיתפס.
שינוי יחידות (×100 או ÷100) יוצר סטייה של 99% ומעלה, ולכן הוא יתפס בכל סבולת שנבחר.

**בדיקה 9 לעומת בדיקות 1 עד 8 ו-10:** בדיקה 9 קובעת שהקובץ השתנה. הבדיקות האחרות מסבירות מה השתנה.

## צעד 2.3: מימוש
- `src/churn_pipeline/contract/models.py`: `DatasetContract` (Pydantic). דוחה חוזה פגום כבר בטעינה.
- `src/churn_pipeline/contract/validator.py`: `validate_against_contract`, שמריץ את 9 הבדיקות.
- `tests/test_validator.py`: 17 טסטים. הנתונים האמיתיים עוברים, וכל בדיקה נתפסת כשהיא נשברת בכוונה.

## פער ידוע (הוחלט לא לטפל)
איחוד קטגוריות, למשל `Phone` ל-`Mobile Phone`, משאיר את כל הערכים בתוך `allowed_values`. לכן אף בדיקה
ברמת העמודה לא מזהה אותו. בדיקה 9 (SHA256) נכשלת, ובנתונים האלה גם בדיקה 10 נכשלת: האיחוד הופך שורה אחת נוספת
לעותק של שורה אחרת (556 הופך ל-557). אבל אף בדיקה לא מציינת איזו עמודה השתנתה.
הוחלט **לא** להוסיף בדיקת התפלגות קטגוריות. הטסט `test_merged_category_not_caught_by_allowed_values` מתעד את הפער.
