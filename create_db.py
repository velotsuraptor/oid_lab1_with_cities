
# Create the 'cities' database if not exists
import psycopg2, getpass, os

HOST = os.getenv("DB_HOST", "127.0.0.1")
PORT = int(os.getenv("DB_PORT", "5432"))
USER = os.getenv("DB_USER", "postgres")
DBNAME = os.getenv("DB_NAME", "cities")

def ensure_db(password: str):
    conn = psycopg2.connect(host=HOST, port=PORT, dbname="postgres", user=USER, password=password)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM pg_database WHERE datname=%s", (DBNAME,))
    if not cur.fetchone():
        cur.execute(f"CREATE DATABASE {DBNAME};")
        print(f"Created database '{DBNAME}'.")
    else:
        print(f"Database '{DBNAME}' already exists.")
    cur.close()
    conn.close()

if __name__ == "__main__":
    pw = getpass.getpass(f"Password for user '{USER}': ")
    ensure_db(pw)
