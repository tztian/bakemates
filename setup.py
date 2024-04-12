import mysql.connector
import json


con = mysql.connector.connect(
  host="localhost",
  user="root",
  password = "",
  database = "bakemates"
)

cur = con.cursor()

# dropping existing tables
cur.execute("DROP TABLE IF EXISTS Review")
cur.execute("DROP TABLE IF EXISTS Orders")
cur.execute("DROP TABLE IF EXISTS Item")
cur.execute("DROP TABLE IF EXISTS Buyer")
cur.execute("DROP TABLE IF EXISTS Baker")
cur.execute("DROP TABLE IF EXISTS User")

# dropping existing roles
cur.execute("DROP ROLE IF EXISTS Admin")
cur.execute("DROP ROLE IF EXISTS Baker")
cur.execute("DROP ROLE IF EXISTS Buyer")

# users table
cur.execute('''CREATE TABLE User
               (UserID VARCHAR(50) PRIMARY KEY,
                Email VARCHAR(50),
                Name VARCHAR(50),
                Phone VARCHAR(50),
                Address TEXT)''')

# Buyer table
cur.execute('''CREATE TABLE Buyer
               (BuyerID VARCHAR(50) PRIMARY KEY,
                Bio TEXT,
                DietaryRestrictions TEXT,
                FOREIGN KEY (BuyerID) REFERENCES User (UserID)
                    ON DELETE CASCADE ON UPDATE NO ACTION)''')

# Baker table
cur.execute('''CREATE TABLE Baker
               (BakerID VARCHAR(50) PRIMARY KEY,
                Description TEXT,
                Rating FLOAT,
                Website TEXT,
                FOREIGN KEY (BakerID) REFERENCES User (UserID)
                    ON DELETE CASCADE ON UPDATE NO ACTION)''')

# item table
cur.execute('''CREATE TABLE Item
               (ItemID VARCHAR(50) PRIMARY KEY,
                BakerID VARCHAR(50),
                ItemCount INT,
                ItemName TEXT,
                ItemType TEXT,
                Flavor TEXT,
                DietaryRestriction TEXT,
                ItemDescription TEXT,
                Price FLOAT(2),
                FOREIGN KEY (BakerID) REFERENCES Baker (BakerID)
                    ON DELETE CASCADE ON UPDATE NO ACTION)''')

# order table
cur.execute('''CREATE TABLE Orders
               (OrderID VARCHAR(50) PRIMARY KEY,
                ItemID VARCHAR(50),
                BuyerID VARCHAR(50),
                Notes TEXT,
                Status VARCHAR(50),
                Time DATETIME,
                Cost FLOAT(2),
                FOREIGN KEY (ItemID) REFERENCES Item (ItemID)
                    ON DELETE CASCADE ON UPDATE NO ACTION,
                FOREIGN KEY (BuyerID) REFERENCES Buyer (BuyerID)
                    ON DELETE CASCADE ON UPDATE NO ACTION)''')

# Review table
cur.execute('''CREATE TABLE Review
               (ReviewID VARCHAR(50) PRIMARY KEY,
                BakerID VARCHAR(50),
                BuyerID VARCHAR(50),
                Comments TEXT,
                Rating DECIMAL(2,1),
                FOREIGN KEY (BakerID) REFERENCES Baker (BakerID)
                    ON DELETE CASCADE ON UPDATE NO ACTION,
                FOREIGN KEY (BuyerID) REFERENCES Buyer (BuyerID)
                    ON DELETE CASCADE ON UPDATE NO ACTION)''')

con.commit()

# Load user data from users.json
with open('./data/users.json', 'r') as file:
    data = json.load(file)
    users = data['users']
    for user in users:
        cur.execute('''
        INSERT INTO User (UserID, Email, Name, Phone, Address)
        VALUES (%s, %s, %s, %s, %s)
        ''', (user['UserID'], user['Email'], user['Name'], user['Phone'], user['Address']))
    con.commit()

# Load baker data from bakers.json
with open('./data/bakers.json', 'r') as file:
    data = json.load(file)
    bakers = data['bakers']
    for baker in bakers:
        cur.execute('''
        INSERT INTO Baker (BakerID, Description, Rating, Website)
        VALUES (%s, %s, %s, %s)
        ''', (baker['BakerID'], baker['Description'], baker['Rating'], baker['Website']))
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
# role based access
cur.execute("CREATE ROLE Admin")
cur.execute("GRANT ALL PRIVILEGES ON * TO Admin")

cur.execute("CREATE ROLE Baker")
cur.execute("GRANT insert, update, delete ON Item TO Baker")
cur.execute("GRANT update(Status) ON Orders TO Baker")
cur.execute("GRANT update(Description), update(Website) ON Baker to Baker")
cur.execute("GRANT update(Email), update(Phone), update(Name), update(Address) ON User to Baker")


cur.execute("CREATE ROLE Buyer")
cur.execute("GRANT insert, update, delete ON Review TO Buyer")
cur.execute("GRANT update(Notes) ON Orders TO Buyer")
cur.execute("GRANT update(Bio), update(DietaryRestrictions) ON Buyer TO Buyer")
cur.execute("GRANT update(Email), update(Phone), update(Name), update(Address) ON User To Buyer")

# to create accounts and add roles to users, use the following:
# CREATE USER 'username'@'hostname' IDENTIFIED BY 'username'
# GRANT 'role' to 'username'@'hostname'

cur.execute("CREATE USER 'test'@'localhost' IDENTIFIED BY 'test'")
cur.execute("GRANT 'Baker' to 'test'@'localhost'")

con.commit()

# checking the database generation is successful (delete this part later)
cur.execute("SHOW TABLES")
for x in cur:
    print(x)

cur.execute("SELECT grantee, privilege_type FROM information_schema.user_privileges WHERE grantee LIKE '%_role%'")
role_privileges = cur.fetchall()
print(role_privileges)
for role, privilege in role_privileges:
    print(f"Role: {role}, Privilege: {privilege}")

#close cursors
cur.close()
con.close()