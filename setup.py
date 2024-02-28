import mysql.connector

con = mysql.connector.connect(
  host="localhost",
  user="root",
  password = "",
  database = "bakemates"
)

cur = con.cursor()

# users table
cur.execute("DROP TABLE IF EXISTS User")
cur.execute('''CREATE TABLE User
               (UserID VARCHAR(50) PRIMARY KEY,
                Name VARCHAR(50),
                Email VARCHAR(50),
                Phone VARCHAR(50),
                Age INT)''')

# item table
cur.execute("DROP TABLE IF EXISTS Item")
cur.execute('''CREATE TABLE Item
               (ItemID VARCHAR(50) PRIMARY KEY,
                ItemName TEXT,
                ItemDescription TEXT,
                Price FLOAT(2))''')

cur.execute("SHOW TABLES")
for x in cur:
    print(x)