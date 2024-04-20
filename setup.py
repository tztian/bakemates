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

#drop exisiting users
cur.execute("DROP USER IF EXISTS 'test'@'localhost'")
cur.execute("DROP USER IF EXISTS 'BK001'@'localhost'")
cur.execute("DROP USER IF EXISTS 'BK002'@'localhost'")
cur.execute("DROP USER IF EXISTS 'BK003'@'localhost'")
cur.execute("DROP USER IF EXISTS 'guest'@'localhost'")

# dropping existing roles
cur.execute("DROP ROLE IF EXISTS Admin")
cur.execute("DROP ROLE IF EXISTS Baker")
cur.execute("DROP ROLE IF EXISTS Buyer")
cur.execute("DROP ROLE IF EXISTS Guest")

# users table
cur.execute('''CREATE TABLE User
               (UserID VARCHAR(50) PRIMARY KEY,
                Email VARCHAR(50),
                Name VARCHAR(50),
                Phone VARCHAR(50),
                Address TEXT,
                Password CHAR(50))''')

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
                BakeryName VARCHAR(50),
                Description TEXT,
                Rating FLOAT,
                Website TEXT,
                ImagePath VARCHAR(255),
                FOREIGN KEY (BakerID) REFERENCES User (UserID)
                    ON DELETE CASCADE ON UPDATE NO ACTION)''')

# item table
cur.execute('''CREATE TABLE Item
               (ItemID VARCHAR(50) PRIMARY KEY,
                BakerID VARCHAR(50),
                ItemCount INT,
                ItemName TEXT,
                ItemType TEXT,
                ItemDescription TEXT,
                GlutenFree BOOL,
                Vegan BOOL,
                DairyFree BOOL,
                NutFree BOOL,
                Price FLOAT(2),
                ImagePath VARCHAR(255),
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
        INSERT INTO User (UserID, Email, Name, Phone, Address, Password)
        VALUES (%s, %s, %s, %s, %s, %s)
        ''', (user['UserID'], user['Email'], user['Name'], user['Phone'], user['Address'], user['Password']))
    con.commit()

# Load baker data from bakers.json
with open('./data/bakers.json', 'r') as file:
    data = json.load(file)
    bakers = data['bakers']
    for baker in bakers:
        cur.execute('''
        INSERT INTO Baker (BakerID, BakeryName, Description, Rating, Website)
        VALUES (%s, %s, %s, %s, %s)
        ''', (baker['BakerID'], baker['BakeryName'], baker['Description'], baker['Rating'], baker['Website']))
    con.commit()

# Load and insert data from items.json
with open('./data/items.json', 'r') as file:
    data = json.load(file)
    items = data['items']
    for item in items:
        cur.execute('''
        INSERT INTO Item (ItemID, BakerID, ItemCount, ItemName, ItemDescription, Price, ImagePath)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (item['ItemID'], item['BakerID'], item['ItemCount'], item['ItemName'], item['ItemDescription'], item['Price'], item['ImagePath']))
    con.commit()
# role based access


cur.execute("CREATE ROLE Admin")
cur.execute("GRANT ALL PRIVILEGES ON bakemates.* TO Admin")

cur.execute("CREATE ROLE Baker")
cur.execute("GRANT select, insert, update, delete ON bakemates.* TO Baker")
#cur.execute("GRANT CREATE VIEW, DROP VIEW ON bakemates.* TO Baker")
cur.execute("GRANT insert, update, delete ON bakemates.Item TO Baker")
cur.execute("GRANT update(Status) ON bakemates.Orders TO Baker")
cur.execute("GRANT update(Description), update(Website) ON bakemates.Baker to Baker")
cur.execute("GRANT update(Email), update(Phone), update(Name), update(Address) ON bakemates.User to Baker")


cur.execute("CREATE ROLE Buyer")
cur.execute("GRANT select ON bakemates.* TO Buyer")
#cur.execute("GRANT CREATE VIEW, DROP VIEW ON bakemates.* TO Buyer")
cur.execute("GRANT select, insert, update, delete ON bakemates.Review TO Buyer")
cur.execute("GRANT update(Notes) ON bakemates.Orders TO Buyer")
cur.execute("GRANT update(Bio), update(DietaryRestrictions) ON bakemates.Buyer TO Buyer")
cur.execute("GRANT update(Email), update(Phone), update(Name), update(Address) ON bakemates.User To Buyer")

cur.execute("CREATE ROLE Guest")
cur.execute("GRANT select ON bakemates.* TO Guest")
#cur.execute("GRANT CREATE VIEW, DROP VIEW ON bakemates.* TO Guest")


# to create accounts and add roles to users, use the following:
# CREATE USER 'username'@'hostname' IDENTIFIED BY 'username'
# GRANT 'role' to 'username'@'hostname'
cur.execute("CREATE USER 'guest'@'localhost' IDENTIFIED BY ''")
cur.execute("GRANT 'Guest' to 'guest'@'localhost'")
cur.execute("SET DEFAULT ROLE 'Guest' to 'guest'@'localhost'")

cur.execute("CREATE USER 'test'@'localhost' IDENTIFIED BY 'test'")
cur.execute("GRANT 'Admin' to 'test'@'localhost'")

cur.execute("CREATE USER 'BK001'@'localhost' IDENTIFIED BY 'password'")
cur.execute("GRANT 'Baker' to 'BK001'@'localhost'")
cur.execute("SET DEFAULT ROLE 'Baker' to 'BK001'@'localhost'")

cur.execute("CREATE USER 'BK002'@'localhost' IDENTIFIED BY 'bakemates'")
cur.execute("GRANT 'Baker' to 'BK002'@'localhost'")
cur.execute("SET DEFAULT ROLE 'Baker' to 'BK002'@'localhost'")

cur.execute("CREATE USER 'BK003'@'localhost' IDENTIFIED BY 'baker'")
cur.execute("GRANT 'Baker' to 'BK003'@'localhost'")
cur.execute("SET DEFAULT ROLE 'Baker' to 'BK003'@'localhost'")

cur.execute("FLUSH PRIVILEGES")


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