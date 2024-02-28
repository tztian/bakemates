import mysql.connector

con = mysql.connector.connect(
  host="localhost",
  user="root",
  password = "",
  database = "bakemates"
)

cur = con.cursor()

cur.execute("DROP TABLE IF EXISTS Item")
cur.execute("DROP TABLE IF EXISTS Buyer")
cur.execute("DROP TABLE IF EXISTS Baker")
cur.execute("DROP TABLE IF EXISTS User")

# users table
cur.execute('''CREATE TABLE User
               (UserID VARCHAR(50) PRIMARY KEY,
                Email VARCHAR(50),
                Name VARCHAR(50),
                Phone VARCHAR(50),
                Age INT)''')

# Buyer table
cur.execute('''CREATE TABLE Buyer
               (BuyerID VARCHAR(50) PRIMARY KEY,
                Bio TEXT,
                FOREIGN KEY (BuyerID) REFERENCES User (UserID)
                    ON DELETE CASCADE ON UPDATE NO ACTION)''')

#Baker table
cur.execute('''CREATE TABLE Baker
               (BakerID VARCHAR(50) PRIMARY KEY,
                Address VARCHAR(50),
                Description TEXT,
                Rating DECIMAL(2,1),
                Website TEXT,
                FOREIGN KEY (BakerID) REFERENCES User (UserID)
                    ON DELETE CASCADE ON UPDATE NO ACTION)''')

# item table
cur.execute('''CREATE TABLE Item
               (ItemID VARCHAR(50) PRIMARY KEY,
                BakerID VARCHAR (50),
                ItemCount INT,
                ItemName TEXT,
                ItemDescription TEXT,
                Price FLOAT(2),
                FOREIGN KEY (UserID) REFERENCES Baker (UserID)
                    ON DELETE CASCADE ON UPDATE NO ACTION)''')



cur.execute("SHOW TABLES")
for x in cur:
    print(x)