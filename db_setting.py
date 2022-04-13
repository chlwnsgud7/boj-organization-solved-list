import sqlite3

conn = sqlite3.connect("unsolved.db")
cur = conn.cursor()

cur.execute('CREATE TABLE user(name text PRIMARY KEY, solved int)')
cur.execute('CREATE TABLE problem(id int PRIMARY KEY)')

# cur.execute("INSERT OR REPLACE INTO user (name, solved) VALUES ('siontama', 300)")
# cur.execute("SELECT solved FROM user WHERE name = 'siontam'")
conn.commit()
cur.close()
conn.close()
