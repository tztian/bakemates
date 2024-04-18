from flask import Flask, render_template, request, redirect, url_for
import mysql as sql
import mysql.connector

########################################################
# Need to change this part later to log in as the user #
########################################################
con = mysql.connector.connect(
  host="localhost",
  user="root",
  password = "",
  database = "bakemates"
)
cur = con.cursor()

###########################
# Actual application part #
###########################
app = Flask(__name__, static_url_path='/static')

# Global variable to store the user's information
user_location = None
current_user = "BK001" 
password = "password"

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

    # check if current user is a baker (TODO: CHANGE THIS PART TO USER IN MYSQL LATER!!!)
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

@app.route('/editbaker')
def edit_baker():
    #edit what is displayed to buyers when they look at the bakery profile
    return render_template('editbaker.html')

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
