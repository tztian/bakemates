import mysql.connector
import json


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
                FOREIGN KEY (BakerID) REFERENCES Baker (BakerID)
                    ON DELETE CASCADE ON UPDATE NO ACTION)''')

con.commit()

# Load user data from users.json
with open('./data/users.json', 'r') as file:
    data = json.load(file)
    users = data['users']
    for user in users:
        cur.execute('''
        INSERT INTO User (UserID, Email, Name, Phone, Age)
        VALUES (%s, %s, %s, %s, %s)
        ''', (user['UserID'], user['Email'], user['Name'], user['Phone'], user['Age']))
    con.commit()

# Load baker data from bakers.json
with open('./data/bakers.json', 'r') as file:
    data = json.load(file)
    bakers = data['bakers']
    for baker in bakers:
        cur.execute('''
        INSERT INTO Baker (BakerID, Address, Description, Rating, Website)
        VALUES (%s, %s, %s, %s, %s)
        ''', (baker['BakerID'], baker['Address'], baker['Description'], baker['Rating'], baker['Website']))
    con.commit()

# Load and insert data from items.json
with open('./data/items.json', 'r') as file:
    data = json.load(file)
    items = data['items']
    for item in items:
        cur.execute('''
        INSERT INTO Item (ItemID, BakerID, ItemCount, ItemName, ItemDescription, Price)
        VALUES (%s, %s, %s, %s, %s, %s)
        ''', (item['ItemID'], item['BakerID'], item['ItemCount'], item['ItemName'], item['ItemDescription'], item['Price']))
    con.commit()

cur.execute("SHOW TABLES")
for x in cur:
    print(x)

#close cursors
cur.close()
con.close()