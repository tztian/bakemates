from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

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
            user_location = request.form['location']
            item_name = request.form['item']
            con = sql.connect("bakemates.db")
            con.row_factory = sql.Row
   
            cur = con.cursor()
            cur.execute("SELECT *")
   
            items = cur.fetchall()

            if items.length > 0:
                return render_template("listings.html", items = items)
        except Exception as e:
            return render_template("error.html", msg = str(e))
        finally:
            return render_template("error.html", msg="no results found")
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



if __name__ == "__main__":
    app.run(debug=True)
