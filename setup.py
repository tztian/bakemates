import mysql.connector

con = mysql.connector.connect(
  host="localhost",
  user="root",
  password = "",
  database = "bakemates"
)

cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS items")
cur.execute('''CREATE TABLE items (
                itemID VARCHAR(10) PRIMARY KEY,
                price REAL
              )''')

# users table
cur.execute("DROP TABLE IF EXISTS User")
cur.execute('''CREATE TABLE User
               (UserID TEXT PRIMARY KEY,
                Age INT,
                Sex TEXT)''')

cur.execute("SHOW TABLES")
for x in cur:
    print(x)