from dotenv import load_dotenv
load_dotenv()
import mysql as sql
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_bcrypt import Bcrypt
import mysql.connector
import os
import paypalrestsdk
import datetime

# create flask application
app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'secret_key'
bcrypt = Bcrypt(app)

# Global variable to store the user's information
user_location = None
current_user = None 
password = None

#Paypal information
paypal_client_id = os.getenv('PAYPAL_CLIENT_ID')
paypal_client_secret = os.getenv('PAYPAL_CLIENT_SECRET')
paypalrestsdk.configure({
    "mode": "sandbox",
    "client_id": paypal_client_id,
    "client_secret": paypal_client_secret
})

@app.route('/')
def index():
    global current_user
    global password
    current_user = None
    password = None
    return render_template('landing.html')

@app.route('/home')
def home():
    global current_user
    global password
    current_user = None
    password = None
    return render_template('landing.html')

@app.route('/search', methods=['POST', 'GET'])
def search():
    global user_location
    global item_name

    if request.method == 'POST':
        try:
            user_location = request.form['location']
            item_name = request.form['item']

            if not item_name:
                return redirect(url_for("listings"))

            # also check for items containing one word/ substring of item name
            sub = item_name.split(' ')
            if current_user == None:
                con = mysql.connector.connect(host="localhost",user="guest",password = "",database = "bakemates")
            else:
                con = mysql.connector.connect(host="localhost",user=current_user,password =password,database = "bakemates")
            
            cur = con.cursor(buffered=True)

            for s in sub:
                cur.execute('''SELECT *
                                FROM Item
                                JOIN (
                                    SELECT *
                                    FROM Baker
                                    INNER JOIN User ON Baker.BakerID = User.UserID
                                ) AS Results ON Item.BakerID = Results.BakerID
                                WHERE LOWER(Item.ItemName) LIKE LOWER(CONCAT('%', CONCAT(%s, '%')))
                                AND LOWER(Results.Address) LIKE LOWER(CONCAT('%', CONCAT(%s, '%')))''', [s, user_location])
        
            items = cur.fetchall()  
            con.close()

            if len(items) > 0:
                print(items)
                return render_template("listings.html", items=items, user = current_user, is_baker = False)
            return render_template("error.html", msg="no results found")
        
        except Exception as e:
            print(e)
            return render_template("error.html", msg = str(e))
    #  validate the location and perform any necessary processing
    #return redirect(url_for('listings'))
        
@app.route('/error')
def error():
    return render_template('error.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/signin', methods=['POST', 'GET'])
def signin_to_page():
    if request.method == 'POST':
        global current_user
        global password 
        current_user = request.form['usrnm']
        unhashed_password = request.form['psw']

        try:
            with mysql.connector.connect(host="localhost",user='root',password='',database="bakemates") as con:
                cur = con.cursor()
                cur.execute("SELECT Password FROM User WHERE UserID = %s", (current_user,))
                password = cur.fetchone()
                if password:
                    password = password[0]
                if not password:
                    flash('User does not exist')
                    current_user = None
                    password = None
                    return redirect(url_for('signin'))
                if not bcrypt.check_password_hash(password, unhashed_password):
                    flash('Password incorrect')
                    current_user = None
                    password = None
                    return redirect(url_for('signin'))
                
                cur.execute("SELECT COUNT(*) FROM Buyer WHERE BuyerID = %s", (current_user,))
                num = cur.fetchone()[0]
                if num  == 1:
                    return redirect(url_for('listings'))
                else:
                    return redirect(url_for('baker_home'))
                
        except Exception as e:
            print(e)
            return render_template("error.html", msg = str(e))


@app.route('/buyersignup', methods=['GET', 'POST'])
def buyer_signup():
    if request.method == 'POST':
        global current_user
        global password
        current_user = request.form['usrnm']
        password = bcrypt.generate_password_hash(request.form['psw']).decode('utf-8')
        email = request.form['email']
        
        try:
            with mysql.connector.connect(host="localhost",user="root",password="",database="bakemates") as con:
                cur = con.cursor()
                cur.execute("SELECT COUNT(*) FROM User WHERE UserID = %s", (current_user,))
                num = cur.fetchone()[0]
                if num > 0:
                    flash('User already exists')
                    current_user = None
                    password = None
                    return redirect(url_for('buyer_signup'))

                cur.execute("DROP USER IF EXISTS %s@'localhost'", (current_user,))
                cur.execute("FLUSH PRIVILEGES")
                cur.execute("CREATE USER %s@'localhost' IDENTIFIED BY %s", (current_user, password))
                cur.execute("GRANT 'Buyer' TO %s@'localhost'", (current_user,))
                cur.execute("SET DEFAULT ROLE 'Buyer' TO %s@'localhost'", (current_user,))
                #cur.execute("FLUSH PRIVILEGES")

                cur.execute("INSERT INTO User(UserID, Email, Password) VALUES(%s, %s, %s)", (current_user, email, password))
                cur.execute("INSERT INTO Buyer(BuyerID) VALUES(%s)", (current_user,))
                con.commit()
        
        except Exception as e:
            con.rollback()
            print(e)
            return render_template("error.html", msg = str(e))

        else:
            return redirect(url_for('listings'))

    return render_template('buyersignup.html')

@app.route('/bakersignup', methods=['GET', 'POST'])
def baker_signup():
    if request.method == 'POST':
        global current_user
        global password
        current_user = request.form['usrnm']
        bakery_name = request.form['bname']
        password = bcrypt.generate_password_hash(request.form['psw']).decode('utf-8')
        email = request.form['email']
        
        try:
            with mysql.connector.connect(host="localhost", user="root", password = "", database = "bakemates") as con:
                cur = con.cursor()
                cur.execute("SELECT COUNT(*) FROM User WHERE UserID = %s", (current_user,))
                num = cur.fetchone()[0]
                if num > 0:
                    flash('User already exists')
                    current_user = None
                    password = None
                    return redirect(url_for('baker_signup'))

                cur.execute("DROP USER IF EXISTS %s@'localhost'", (current_user,))
                cur.execute("FLUSH PRIVILEGES")
                cur.execute("CREATE USER %s@'localhost' IDENTIFIED BY %s", (current_user, password))
                cur.execute("GRANT 'Baker' TO %s@'localhost'", (current_user,))
                cur.execute("SET DEFAULT ROLE 'Baker' TO %s@'localhost'", (current_user,))

                cur.execute("INSERT INTO User(UserID, Email, Password) VALUES(%s, %s, %s)", (current_user, email, password))
                cur.execute("INSERT INTO Baker(BakerID, BakeryName) VALUES(%s, %s)", (current_user, bakery_name))
                con.commit()
        
        except Exception as e:
            con.rollback()
            print(e)
            return render_template("error.html", msg = str(e))
        
        else:
            return redirect(url_for('baker_home'))
        
    return render_template('bakersignup.html')

@app.route('/logout')
def logout():
    global current_user
    global password
    current_user = None
    password = None

    return redirect(url_for('home'))

@app.route('/listings', methods = ['POST','GET'])
def listings():
    if current_user == None:
        con = mysql.connector.connect(host="localhost",user="guest",password = "",database = "bakemates")
    else:
        con = mysql.connector.connect(host="localhost",user=current_user,password=password,database = "bakemates")

    cur = con.cursor(buffered=True)
        
    cur.execute("SELECT * From Item")

    items = cur.fetchall()
    return render_template("listings.html", items = items, user = current_user, is_baker = False)

@app.route('/displayItem/', methods=['POST','GET'])
def display_item():
    item = request.args.get('item')
    item = item[1:len(item)-1]
    result = []
    for i, val in enumerate(item.split(', ')):
        print (val)
        if val[0] == "'":
            val = val[1:len(val)-1]
        elif i == 9:
            val = float(val)
        elif val[0] == "\"":
            val = val[1:len(val)-1]
        result.append(val)
    return render_template('item.html', item = result)

@app.route('/filter', methods=['POST'])
def filter_items():
    categories = request.form.getlist('type')
    items = []
    for category in categories:
        if category == 'All':
            return redirect('/listings')
        else:
            # get items filtered by category from database
            if current_user == None:
                con = mysql.connector.connect(host="localhost",user="guest",password = "",database = "bakemates")
            else:
                con = mysql.connector.connect(host="localhost",user=current_user,password =password,database = "bakemates")

            cur = con.cursor(buffered=True)
            cur.execute("SELECT * From Item WHERE LOWER(Item.ItemName) LIKE LOWER(CONCAT('%', CONCAT(%s, '%')))", [category])
            if category == "Bread":
                cur.execute("SELECT * FROM Item WHERE ItemType = %s", ("Bread",))
            if category == "Pastry":
                cur.execute("SELECT * FROM Item WHERE ItemType = %s", ("Pastry",))
            if category == "Cake":
                cur.execute("SELECT * FROM Item WHERE ItemType = %s", ("Cake",))
            if category == "Cookie":
                cur.execute("SELECT * FROM Item WHERE ItemType = %s", ("Cookie",))
            
                        
        items += cur.fetchall() 
    if len(items) == 0:
        print("here")
        return render_template('error.html', msg = 'No Sweet Treats Found ☹')
    return render_template('listings.html', items = items, user = current_user, is_baker = False)
    
@app.route('/clear', methods = ['POST'])
def clear_filters():
    return redirect('/listings')

# Routes for baker-specific functionality
@app.route('/bakerhome')
def baker_home():
    try:
        with mysql.connector.connect(host="localhost",user=current_user,password = password,database = "bakemates") as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM User WHERE UserID = %s", (current_user,))
            user_info = cur.fetchall()[0]
            cur.execute('''SELECT * FROM Baker WHERE BakerID = %s''', (current_user,))
            baker_info = cur.fetchall()[0]
            cur.execute('''SELECT * FROM Item WHERE BakerID = %s''', (current_user,))
            items = cur.fetchall()
            # Fetch orders
            cur.execute('''SELECT * FROM Orders o
                        JOIN Item i ON o.ItemID = i.ItemID
                        JOIN Baker b ON i.BakerID = b.BakerID
                        WHERE b.BakerID = %s''', (current_user,))
            orders = cur.fetchall()

        return render_template('bakerhome.html', user_info = user_info, baker_info = baker_info, rows = items, orders=orders)
    
    except Exception as e:
        print(e)
        return render_template("error.html", msg = str(e))

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        item_name = request.form.get('item_name')
        item_type = request.form.get('item_type')
        item_description = request.form.get('item_description')
        item_price = request.form.get('item_price')
        gluten_free = 'gluten_free' in request.form
        vegan = 'vegan' in request.form
        dairy_free = 'dairy_free' in request.form
        nut_free = 'nut_free' in request.form

        try:
            with mysql.connector.connect(host="localhost", user=current_user, password=password, database="bakemates") as con:
                cur = con.cursor()

                item_image = request.files.get('item_image')
                if item_image and item_image.filename != '':
                    timestamp = int(datetime.datetime.now().timestamp())
                    unique_filename = f"{timestamp}_{item_image.filename}"
                    item_image_path = os.path.join('./static/items', unique_filename)
                    item_image.save(item_image_path)

                # Insert the new item into the database
                cur.execute('''
                    INSERT INTO Item (BakerID, ItemName, ItemType, ItemDescription, 
                                    GlutenFree, Vegan, DairyFree, NutFree, Price, ImagePath)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', (current_user, item_name, item_type, item_description, 
                    gluten_free, vegan, dairy_free, nut_free, item_price, item_image_path))
                con.commit()
        
        except Exception as e:
            con.rollback
            print(e)
            return render_template("error.html", msg = str(e))
        
        else:
            return redirect(url_for('baker_home'))
        
    return render_template("additem.html")
    

@app.route('/edit_item', methods=['GET', 'POST'])
def edit_item():
    if request.method == 'POST':
        itemID = request.form.get('itemID')
        try: 
            with mysql.connector.connect(host="localhost", user=current_user, password=password, database="bakemates") as con:
                cur = con.cursor()

                # check if the item belongs to the baker
                cur.execute('SELECT BakerID FROM Item WHERE ItemID = %s', (itemID,))
                baker = cur.fetchone()
                if not baker or baker[0] != current_user:
                    flash('Cannot update this item')
                    return redirect(url_for('edit_item'))
                else:
                    new_name = request.form.get('new_name')
                    new_price = request.form.get('new_price')
                    new_type = request.form.get('new_type')
                    new_description = request.form.get('new_description')
                    gluten_free = 'gluten_free' in request.form
                    vegan = 'vegan' in request.form
                    dairy_free = 'dairy_free' in request.form
                    nut_free = 'nut_free' in request.form
                    new_image = request.files.get('new_image')

                    # make new image path
                    if new_image and new_image.filename != '':
                        # remove the current image path from the database
                        cur.execute("SELECT ImagePath FROM Item WHERE ItemID = %s", (itemID,))
                        existing_image = cur.fetchone()
                        existing_image_path = existing_image[0] if existing_image else None
                        if existing_image_path:
                            os.remove(existing_image_path)

                        timestamp = int(datetime.datetime.now().timestamp())
                        unique_filename = f"{timestamp}_{new_image.filename}"
                        new_image_path = os.path.join('./static/items', unique_filename)
                        new_image.save(new_image_path)
                        cur.execute('UPDATE Item SET ImagePath = %s WHERE ItemID = %s', (new_image_path, itemID))

                    # update all the categories
                    if new_name:
                        cur.execute('UPDATE Item SET ItemName = %s WHERE ItemID = %s', (new_name, itemID))
                    if new_price:
                        cur.execute('UPDATE Item SET PRICE = %s WHERE ItemID = %s', (new_price, itemID))
                    if new_type:
                        cur.execute('UPDATE Item SET ItemType = %s WHERE ItemID = %s', (new_type, itemID))
                    if new_description:
                        cur.execute('UPDATE Item SET ItemDescription = %s WHERE ItemID = %s', (new_description, itemID))
                    if new_name:
                        cur.execute('UPDATE Item SET ItemName = %s WHERE ItemID = %s', (new_name, itemID))

                    cur.execute('UPDATE Item SET GlutenFree = %s WHERE ItemID = %s', (gluten_free, itemID))
                    cur.execute('UPDATE Item SET Vegan = %s WHERE ItemID = %s', (vegan, itemID))
                    cur.execute('UPDATE Item SET DairyFree = %s WHERE ItemID = %s', (dairy_free, itemID))
                    cur.execute('UPDATE Item SET NutFree = %s WHERE ItemID = %s', (nut_free, itemID))
                    
                    con.commit()

        except Exception as e:
            con.rollback
            print(e)
            return render_template("error.html", msg = str(e)) 
        else:       
            flash('Item successfully updated')
            return redirect(url_for('edit_item'))

    return render_template('updateitem.html')

@app.route('/delete_item', methods=['GET', 'POST'])
def delete_item():
    if request.method == 'POST':
        itemID = request.form['itemID']
        with mysql.connector.connect(host="localhost", user=current_user, password=password, database="bakemates") as con:
            cur = con.cursor()
            cur.execute('SELECT BakerID FROM Item WHERE ItemID = %s', (itemID,))
            baker = cur.fetchone()
            if baker and baker[0] == current_user:
                cur.execute('DELETE FROM Item WHERE ItemID = %s', (itemID,))
                con.commit()
                flash('Item successfully deleted')
                return redirect(url_for('delete_item'))
            else:
                flash('Cannot delete this item')
                return redirect(url_for('delete_item'))

    return render_template('deleteitem.html')

@app.route('/edit_baker', methods = ['POST','GET'])
def edit_baker():
    #edit what is displayed to buyers when they look at the bakery profile
    if request.method == 'POST':
        # Retrieve form data
        name = request.form['name']
        bakery_name = request.form['bakery_name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        website = request.form['website']
        description = request.form['description']
        bakery_image = request.files['image']

        try: 
            with mysql.connector.connect(host="localhost", user=current_user, password=password, database="bakemates") as con:
                cur = con.cursor()

                if bakery_image and bakery_image.filename != '':
                    # remove the current image path from the database
                    cur.execute("SELECT ImagePath FROM Baker WHERE BakerID = %s", (current_user,))
                    existing_image = cur.fetchone()
                    existing_image_path = existing_image[0] if existing_image else None
                    if existing_image_path:
                        os.remove(existing_image_path)
                    
                    #Combine a timestamp with the filename for a unique filename to prevent overwrites
                    timestamp = int(datetime.datetime.now().timestamp())
                    unique_filename = f"{timestamp}_{bakery_image.filename}"
                    bakery_image_path = os.path.join('./static/bakers', unique_filename)
                    bakery_image.save(bakery_image_path)
                    cur.execute('UPDATE Baker SET ImagePath = %s WHERE BakerID = %s', (bakery_image_path, current_user))
                    

                # Update statement for bakery details
                if name:
                    cur.execute('UPDATE User SET Name = %s WHERE UserID = %s', (name, current_user))
                if email:
                    cur.execute('UPDATE User SET Email = %s WHERE UserID = %s', (email, current_user))
                if phone:
                    cur.execute('UPDATE User SET Phone = %s WHERE UserID = %s', (phone, current_user))
                if address:
                    cur.execute('UPDATE User SET Address = %s WHERE UserID = %s', (address, current_user))
                if bakery_name:
                    cur.execute('UPDATE Baker SET BakeryName = %s WHERE BakerID = %s', (bakery_name, current_user))
                if website:
                    cur.execute('UPDATE Baker SET Website = %s WHERE BakerID = %s', (website, current_user))    
                if description:
                    cur.execute('UPDATE Baker SET Description = %s WHERE BakerID = %s', (description, current_user))
                if bakery_image:
                    cur.execute('UPDATE Baker SET ImagePath = %s WHERE BakerID = %s', (bakery_image_path, current_user))
                
                con.commit()

        except Exception as e:
            con.rollback
            print(e)
            return render_template("error.html", msg = str(e))
        
        else:        
            return redirect(url_for('baker_home'))
        
    return render_template('editbaker.html')

@app.route('/pay', methods=['POST'])
def pay():
    data = request.get_json()
    order_id = data['orderID']
    payer_id = data['payerID']
    payment_id = data['paymentID']
    item_id = data['item_id']
    total = data['total']
    notes = data['notes']

    con = mysql.connector.connect(host="localhost", user=current_user, password=password, database="bakemates")
    cur = con.cursor()

    add_order = ("INSERT INTO Orders (OrderID, ItemID, BuyerID, Notes, Status, Time, Cost) "
                 "VALUES (%s, %s, %s, %s, %s, %s, %s)")
    data_order = (order_id, item_id, current_user, notes, 'Pending', datetime.datetime.now(), total)
    cur.execute(add_order, data_order)
    con.commit()
    cur.close()
    con.close()

    return jsonify({'success': True}), 200

@app.route('/payment/execute', methods=['GET'])
def execute():
    payment_id = request.args.get('paymentId')
    payer_id = request.args.get('PayerID')

    con = mysql.connector.connect(host="localhost", user=current_user, password=password, database="bakemates")
    cur = con.cursor()

    update_order = ("UPDATE Orders SET Status = %s WHERE OrderID = %s")
    data_update = ('Paid', payment_id)
    cur.execute(update_order, data_update)
    con.commit()
    cur.close()
    con.close()
    return redirect(url_for('buyer_profile'))

@app.route('/buyer_profile')
def buyer_profile():
    with mysql.connector.connect(host="localhost", user=current_user, password=password, database="bakemates") as con:
        cur = con.cursor()

        # Fetch user information
        cur.execute("SELECT * FROM User WHERE UserID = %s", (current_user,))
        user_info = cur.fetchone()

        # Fetch buyer information
        cur.execute("SELECT * FROM Buyer WHERE BuyerID = %s", (current_user,))
        buyer_info = cur.fetchone()

        # Fetch orders
        cur.execute("SELECT * FROM Orders WHERE BuyerID = %s", (current_user,))
        orders = cur.fetchall()

    return render_template('buyerprofile.html', user=current_user, user_info=user_info, buyer_info=buyer_info, orders=orders)

@app.route('/edit_buyer', methods=['GET', 'POST'])
def edit_buyer():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        dietary_restrictions = request.form['dietary_restrictions']
        bio = request.form['bio']

        try:
            with mysql.connector.connect(host="localhost", user=current_user, password=password, database="bakemates") as con:
                cur = con.cursor()
                if name:
                    cur.execute('UPDATE User SET Name = %s WHERE UserID = %s', (name, current_user))
                if email:
                    cur.execute('UPDATE User SET Email = %s WHERE UserID = %s', (email, current_user))
                if phone:
                    cur.execute('UPDATE User SET Phone = %s WHERE UserID = %s', (phone, current_user))
                if address:
                    cur.execute('UPDATE User SET Address = %s WHERE UserID = %s', (address, current_user))
                if dietary_restrictions:
                    cur.execute('UPDATE Buyer SET DietaryRestrictions = %s WHERE BuyerID = %s', (dietary_restrictions, current_user))
                if bio:
                    cur.execute('UPDATE Buyer SET Bio = %s WHERE BuyerID = %s', (bio, current_user))
                con.commit()
        
        except Exception as e:
            con.rollback
            print(e)
            return render_template("error.html", msg = str(e))
        
        else:
            return redirect(url_for('buyer_profile'))
    
    return render_template('editbuyer.html', user = current_user)

@app.route('/checkout')
def checkout():
    if current_user == None:
        return redirect(url_for('signin'))
    else:
        item_id = request.args.get('item_id')
        con = mysql.connector.connect(host="localhost", user=current_user, password=password, database="bakemates")
        cur = con.cursor()
        cur.execute("SELECT * FROM Item WHERE ItemID = %s", (item_id,))
        item = cur.fetchone()
        cur.close()
        con.close()
        
        if item:
            return render_template('checkout.html', client_id=paypal_client_id, item=item)
        else:
            return "Item not found", 404

@app.route('/bakery/<bakery_id>')
def bakery(bakery_id):
    # Connect to the database
    db_user = "guest" if current_user is None else current_user
    db_password = "" if current_user is None else password
    con = mysql.connector.connect(host="localhost", user=db_user, password=db_password, database="bakemates")

    cur = con.cursor()

    # Fetch bakery details
    cur.execute('''
        SELECT BakeryName, Description, ImagePath
        FROM Baker 
        WHERE BakerID = %s
    ''', (bakery_id,))
    bakery = cur.fetchone()

    # Fetch reviews for the bakery and average rating
    cur.execute('''
        SELECT Comments, Rating, BuyerID
        FROM Review
        WHERE BakerID = %s
    ''', (bakery_id,))
    reviews = cur.fetchall()

    # Calculate average rating
    if reviews:
        average_rating = sum([review[1] for review in reviews]) / len(reviews)
    else:
        average_rating = "n/a"

    con.close()

    if bakery:
        bakery_details = {
            "bakery_id": bakery_id,
            "name": bakery[0],
            "description": bakery[1],
            "image_path": bakery[2],
            "reviews": reviews,
            "average_rating": average_rating
        }
        return render_template('bakerprofile.html', bakery=bakery_details, user=current_user)
    else:
        return render_template("error.html", msg="Bakery not found")

@app.route('/bakery/listings/<bakery_id>')
def bakery_listings(bakery_id):
        try:
            # also check for items containing one word/ substring of item name
            if current_user == None:
                con = mysql.connector.connect(host="localhost",user="guest",password = "",database = "bakemates")
            else:
                con = mysql.connector.connect(host="localhost",user=current_user,password =password,database = "bakemates")
            
            cur = con.cursor(buffered=True)
            cur.execute('''SELECT *
                                FROM Item
                                JOIN (
                                    SELECT *
                                    FROM Baker
                                    INNER JOIN User ON Baker.BakerID = User.UserID
                                ) AS Results ON Item.BakerID = Results.BakerID WHERE Item.BakerID =%s''', [bakery_id])
        

            items = cur.fetchall()  

            if len(items) > 0:
                print(items)
                return render_template("listings.html", items=items, user = current_user, is_baker = True)
            return render_template("error.html", msg="no results found")
        except Exception as e:
            print(e)
            return render_template("error.html", msg = str(e))

@app.route('/submit_review/<bakery_id>', methods=['POST'])
def submit_review(bakery_id):
    if not current_user:
        return redirect(url_for('signin'))

    rating = request.form['rating']
    comments = request.form['comments']

    con = mysql.connector.connect(host="localhost", user=current_user, password=password, database="bakemates")
    cur = con.cursor()
    review_id = f"{bakery_id}_{current_user}"
    try:
        cur.execute('''
            INSERT INTO Review (ReviewID, BakerID, BuyerID, Comments, Rating)
            VALUES (%s, %s, %s, %s, %s)
        ''', (review_id, bakery_id, current_user, comments, rating))
        con.commit()
    except Exception as e:
        con.rollback()
        print("You have already reviewed this baker", e)
    finally:
        con.close()

    return redirect(url_for('bakery', bakery_id=bakery_id))

@app.route('/update_order_status/<order_id>', methods=['POST'])
def update_order_status(order_id):
    new_status = request.form['status']
    con = mysql.connector.connect(host="localhost", user=current_user, password=password, database="bakemates")
    cur = con.cursor()
    
    cur.execute("UPDATE Orders SET Status = %s WHERE OrderID = %s", (new_status, order_id))
    
    con.commit()
    con.close()
    
    return redirect(url_for('baker_home'))



if __name__ == "__main__":
    app.run(debug=True)
