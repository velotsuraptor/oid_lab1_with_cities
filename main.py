from db import get_cursor

BASE_CITIES_4 = ["Kyiv", "Lviv", "Odesa", "Kharkiv"]
NEW_CITY = "Dnipro"
RENAME_FROM = "Odesa"
RENAME_TO = "Odesa (updated)"
DELETE_CITY = "Lviv"
ADD_BACK_CITY = "Lviv"

def ensure_table():
    with get_cursor(commit=True) as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS cities (
                id SERIAL PRIMARY KEY,
                city_name TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT NOW()
            );
        """)

def truncate():
    with get_cursor(commit=True) as cur:
        cur.execute("TRUNCATE TABLE cities RESTART IDENTITY;")

def seed_4():
    with get_cursor(commit=True) as cur:
        cur.executemany("INSERT INTO cities (city_name) VALUES (%s)", [(c,) for c in BASE_CITIES_4])

def add_city(name):
    with get_cursor(commit=True) as cur:
        cur.execute("INSERT INTO cities (city_name) VALUES (%s) ON CONFLICT (city_name) DO NOTHING", (name,))

def rename_city(old, new):
    with get_cursor(commit=True) as cur:
        cur.execute("UPDATE cities SET city_name=%s WHERE city_name=%s", (new, old))

def delete_city(name):
    with get_cursor(commit=True) as cur:
        cur.execute("DELETE FROM cities WHERE city_name=%s", (name,))

def rows():
    with get_cursor() as cur:
        cur.execute("SELECT id, city_name FROM cities ORDER BY id")
        return cur.fetchall()

def print_rows(title):
    print(f"\n{title}")
    data = rows()
    for r in data:
        print(f"{r['id']:>2}  {r['city_name']}")
    print(f"Total rows: {len(data)}")

def press(msg):
    input(msg)

def main():
    ensure_table()

    press("Press Enter to FILL the database (4 base cities)...")
    truncate()
    seed_4()
    print_rows("After seed (4 rows)")

    press(f"Press Enter to ADD a new city: {NEW_CITY} ...")
    add_city(NEW_CITY)
    print_rows("After add (5 rows)")

    press(f"Press Enter to RENAME city '{RENAME_FROM}' -> '{RENAME_TO}' ...")
    rename_city(RENAME_FROM, RENAME_TO)
    print_rows("After rename")

    press(f"Press Enter to DELETE city '{DELETE_CITY}' ...")
    delete_city(DELETE_CITY)
    print_rows("After delete (4 rows)")

    press(f"Press Enter to ADD BACK city '{ADD_BACK_CITY}' ...")
    add_city(ADD_BACK_CITY)
    print_rows("After add back (5 rows)")

if __name__ == "__main__":
    main()
