from flask import Flask, render_template, request, redirect, url_for
import mysql as sql
import mysql.connector
import os
import time

app = Flask(__name__, static_url_path='/static')

# Global variable to store the user's information
user_location = None
current_user = None 
password = None

@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/search', methods=['POST', 'GET'])
def search():
    global user_location
    global item_name

    if request.method == 'POST':
        try:
            #user_location = request.form['location']
            item_name = request.form['item']

            # also check for items containing one word/ substring of item name
            sub = item_name.split(' ')

            cur = con.cursor(buffered=True)

            for s in sub:
                cur.execute("SELECT * From Item WHERE ItemName LIKE CONCAT('%', CONCAT(%s, '%'))", [s])
             
            #cur.execute("SELECT * FROM Item WHERE ItemName = %s", [item_name])

            items = cur.fetchall()  
            print(items)

            if len(items) > 0:
                print("here")
                print(items)
                print("here2")
                return render_template("listings.html", items=items)
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
        password = request.form['psw']

        with mysql.connector.connect(host="localhost", user=current_user, password = password, database = "bakemates") as con:
            cur = con.cursor()
            cur.execute("SELECT COUNT(*) FROM User WHERE UserID = %s AND Password = %s", (current_user, password))
            num = cur.fetchone()[0]
            if num != 1:
                return render_template("error.html")
            
            cur.execute("SELECT COUNT(*) FROM Buyer WHERE BuyerID = %s", (current_user,))
            num = cur.fetchone()[0]
            if num  == 1:
                return redirect(url_for('listings'))
            else:
                return redirect(url_for('baker_home'))


@app.route('/buyersignup')
def buyer_signup():
    return render_template('buyersignup.html')

@app.route('/signupbuyer', methods=['POST'])
def signupbuyer():
    # get the form data
    return redirect(url_for('listings'))

@app.route('/bakersignup')
def baker_signup():
    return render_template('bakersignup.html')

@app.route('/signupbaker', methods=['POST'])
def signupbaker():
    # get the form data
    return redirect(url_for('baker_home'))


@app.route('/listings', methods = ['POST','GET'])
def listings():
    return render_template("listings.html")

@app.route('/displayItem/', methods=['POST','GET'])
def display_item():
    item = request.args.get('item')
    item = item[1:len(item)-1]
    result = []
    for val in item.split(', '):
        if val[0] == "'":
            val = val[1:len(val)-1]
        result.append(val)
    return render_template('item.html', item = result)

@app.route('/filter', methods=['POST'])
def filter_items():
    category = request.form['category']
    if category == 'All':
        return redirect('/listings')
    else:
        # get items filtered by category from database
        return render_template('listings.html')

# Routes for baker-specific functionality
@app.route('/bakerhome')
def baker_home():
    #retrieve and display information for the baker's home page
    #get bakery name from database, and somehow knowing whos logged in.
    #all items from the database for that bakery
    #return render_template('bakerhome.html', bakery_name=bakery_name, items=items)

    with mysql.connector.connect(host="localhost", user=current_user, password = password, database = "bakemates") as con:
        cur = con.cursor()
        cur.execute("SELECT Name FROM User WHERE UserID = %s", (current_user,))
        baker_name = cur.fetchone()
        if baker_name:
            baker_name = baker_name[0]
        cur.execute('''SELECT ItemID, ItemName, ItemCount, ItemType, Flavor, DietaryRestriction,
                    ItemDescription, Price FROM Item WHERE BakerID = %s''', (current_user,))
        rows = cur.fetchall()

    return render_template('bakerhome.html', baker_name = baker_name, rows = rows)

@app.route('/additem')
def add_item():
    #needs to work with the form from additem.html
    #also needs to send everything from the form into the database
    return render_template('additem.html')

@app.route('/editbaker', methods = ['POST','GET'])
def edit_baker():
    #edit what is displayed to buyers when they look at the bakery profile
    try:
        con = mysql.connector.connect(host="localhost", user=current_user, password=password, database="bakemates")
        cur = con.cursor()

        if request.method == 'POST':
            # Retrieve form data
            bakery_name = request.form.get('bakery_name')
            bakery_description = request.form.get('bakery_description')
            bakery_website = request.form.get('bakery_website')
            bakery_image = request.files['bakery_image']

            if bakery_image and bakery_image.filename != '':
                #Combine a timestamp with the filename for a unique filename to prevent overwrites
                timestamp = int(time.time())
                unique_filename = f"{timestamp}_{bakery_image.filename}"
                bakery_image_path = os.path.join('./static/bakers', unique_filename)
                bakery_image.save(bakery_image_path)
                
                # Get the current image path from the database
                cur.execute("SELECT ImagePath FROM Baker WHERE BakerID = %s", (current_user,))
                existing_image = cur.fetchone()
                existing_image_path = existing_image[0] if existing_image else None

                # Update statement for bakery details
                update_query = """
                UPDATE Baker SET
                    BakeryName = %s,
                    Description = %s,
                    Website = %s,
                    ImagePath = %s
                WHERE BakerID = %s
                """
                update_values = (
                    bakery_name,
                    bakery_description,
                    bakery_website,
                    bakery_image_path,
                    current_user
                )
                cur.execute(update_query, update_values)
                con.commit()

                if existing_image_path:
                    os.remove(existing_image_path)
                
                return redirect(url_for('baker_home'))
            # Update statement for bakery details
            update_query = """
            UPDATE Baker SET
                BakeryName = %s,
                Description = %s,
                Website = %s
            WHERE BakerID = %s
            """
            update_values = (
                bakery_name,
                bakery_description,
                bakery_website,
                current_user
            )
            cur.execute(update_query, update_values)
            con.commit()
                
            return redirect(url_for('baker_home'))

        else:
            cur.execute("SELECT BakeryName, Description, Website, ImagePath FROM Baker WHERE BakerID = %s", (current_user,))
            baker_data = cur.fetchone()
            if baker_data:  
                baker_info = {
                    'name': baker_data[0],
                    'description': baker_data[1],
                    'website': baker_data[2],
                    'image_path': baker_data[3]
                }
            else:
                baker_info = {'error': 'No bakery information found for this user.'}
    except mysql.connector.Error as err:
        print("Error: ", err)
        baker_info = {'error': 'Database connection or execution issue'}
    finally:
        cur.close()
        con.close()

    return render_template('editbaker.html', baker=baker_info)

@app.route('/bakerprofile')
def baker_profile():
    #edit what is displayed to buyers when they look at the bakery profile
    return render_template('bakerprofile.html')

@app.route('/custom_order')
def custom_order():
    return render_template('customorder.html')

#CUSTOM ORDER FORM SUBMISSION
@app.route('/submit_custom_order', methods=['POST'])
def submit_custom_order():
    # Extract form data to send to bakery somehow ??
    item_name = request.form['item_name']
    item_quantity = request.form['item_quantity']
    item_date = request.form['item_date']
    item_type = request.form['item_type']
    dietary_restrictions = request.form['dietary-restrictions']
    item_flavor = request.form['item_flavor']
    item_description = request.form['item_description']
    
    # Process data (e.g., save to database, send email, etc.)
    
    # Redirect to another page after processing
    return redirect(url_for('order_confirmation'))  # Redirect to an order confirmation page


if __name__ == "__main__":
    app.run(debug=True)
