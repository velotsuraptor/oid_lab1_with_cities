
# Cities Lab (Final Minimal Project)

- **Database**: `cities`
- **Table**: `cities`
- Exactly 20 rows inserted (Ukrainian city names).
- Simple interactive menu with only the required CRUD.

## 1) Install & run
```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

:: create DB 'cities' once
python create_db.py

:: run interactive menu
python main.py
```

## 2) Menu
```
1. Ensure table (create if missing)
2. Reset table and insert 20 rows
3. Show all rows
4. Select rows by city
5. Update email of row with id=1
6. Delete all rows with domain '@mail.com'
0. Exit
```

## 3) Watching in pgAdmin
Open pgAdmin → Database `cities` → Schema `public` → Table `cities`.  
Or open Query Tool:
```sql
SELECT * FROM cities ORDER BY id;
```
