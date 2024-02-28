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

# Buyer table
cur.execute("DROP TABLE IF EXISTS Buyer")
cur.execute('''CREATE TABLE Buyer
               (UserID VARCHAR(50) PRIMARY KEY,
                Bio TEXT,
                FOREIGN KEY (UserID) REFERENCES User (UserID)
                    ON DELETE CASCADE ON UPDATE NO ACTION)''')

#Baker table
cur.execute("DROP TABLE IF EXISTS Baker")
cur.execute('''CREATE TABLE Baker
               (UserID VARCHAR(50) PRIMARY KEY,
                Address VARCHAR(50),
                Description TEXT,
                Rating DECIMAL(2,1),
                Website TEXT,
                FOREIGN KEY (UserID) REFERENCES User (UserID)
                    ON DELETE CASCADE ON UPDATE NO ACTION)''')

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