import sqlite3

conn = sqlite3.connect("giflibby.db")
cursor = conn.cursor()

# Show all tables
cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type = 'table'
ORDER BY name;
""")

print("Tables:")
tables = [row[0] for row in cursor.fetchall()]

for table in tables:
    print(table)

# Show contents of each user table
for table in tables:
    if table == "sqlite_sequence":
        continue

    print(f"\n--- {table} ---")

    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()

    if not rows:
        print("(empty)")
        continue

    for row in rows:
        print(row)

conn.close()