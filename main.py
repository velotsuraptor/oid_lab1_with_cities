# Interactive CRUD for the 'cities' table (DB name also 'cities')
# Uses the connection helper from db.py (same folder).
from db import get_cursor

UA_CITIES = [
    "Kyiv", "Kharkiv", "Odesa", "Dnipro", "Zaporizhzhia",
    "Lviv", "Kryvyi Rih", "Mykolaiv", "Mariupol", "Vinnytsia",
    "Poltava", "Chernihiv", "Khmelnytskyi", "Cherkasy", "Sumy",
    "Zhytomyr", "Rivne", "Ivano-Frankivsk", "Ternopil", "Uzhhorod"
]

DDL_CREATE = """
CREATE TABLE IF NOT EXISTS cities (
    id SERIAL PRIMARY KEY,
    city_name TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
"""

def ensure_table():
    with get_cursor(commit=True) as cur:
        cur.execute(DDL_CREATE)

def reset_and_seed():
    """Empty the table and insert exactly 20 Ukrainian city names."""
    values = [(name,) for name in UA_CITIES]
    with get_cursor(commit=True) as cur:
        cur.execute(DDL_CREATE)
        cur.execute("TRUNCATE TABLE cities RESTART IDENTITY;")
        cur.executemany("INSERT INTO cities (city_name) VALUES (%s)", values)

def show_all():
    with get_cursor() as cur:
        cur.execute("SELECT id, city_name, created_at FROM cities ORDER BY id;")
        return cur.fetchall()

def select_by_name(name: str):
    with get_cursor() as cur:
        cur.execute(
            "SELECT id, city_name, created_at FROM cities WHERE city_name = %s;",
            (name,),
        )
        return cur.fetchall()

def update_id1(new_name: str = "Kyiv (updated)"):
    with get_cursor(commit=True) as cur:
        cur.execute("UPDATE cities SET city_name = %s WHERE id = 1;", (new_name,))
        return cur.rowcount

def delete_by_name(name: str):
    with get_cursor(commit=True) as cur:
        cur.execute("DELETE FROM cities WHERE city_name = %s;", (name,))
        return cur.rowcount

def menu():
    while True:
        print("\n=== MENU (DB = cities, table = cities) ===")
        print("1. Ensure table (create if missing)")
        print("2. Reset table and insert 20 Ukrainian city names")
        print("3. Show all cities")
        print("4. Find a city by name")
        print("5. Update city name of row with id=1")
        print("6. Delete a city by name")
        print("0. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            ensure_table()
            print("✅ Table ensured.")
        elif choice == "2":
            reset_and_seed()
            print("✅ Seeded 20 city names.")
            for r in show_all():
                print(r)
        elif choice == "3":
            rows = show_all()
            if not rows:
                print("(empty)")
            else:
                for r in rows:
                    print(r)
        elif choice == "4":
            name = input("City name: ").strip()
            rows = select_by_name(name)
            if not rows:
                print(f"(no rows for '{name}')")
            else:
                for r in rows:
                    print(r)
        elif choice == "5":
            new_name = input("New name for id=1 (default 'Kyiv (updated)'): ").strip() or "Kyiv (updated)"
            n = update_id1(new_name)
            print(f"Rows updated: {n}")
            for r in show_all():
                print(r)
        elif choice == "6":
            name = input("City name to delete: ").strip()
            n = delete_by_name(name)
            print(f"Rows deleted: {n}")
            for r in show_all():
                print(r)
        elif choice == "0":
            print("bye 👋")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    menu()
