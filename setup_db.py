import sqlite3
conn=sqlite3.connect("resume_checks.db")
cursor=conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS resume_checks(
id INTEGER PRIMARY KEY AUTOINCREMENT,
match_percentage REAL,
missing_skills TEXT,
feedback TEXT,
timestamp DATETIME DEFAULT CURRENT_TIMESTAMP )
""")
conn.commit()
conn.close()

print("Database and Table created successfully")