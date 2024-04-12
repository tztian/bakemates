from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, static_url_path='/static')

# Global variable to store the user's location
user_location = None

@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/search', methods=['POST'])
def search():
    global user_location
    user_location = request.form.get('location')
    #  validate the location and perform any necessary processing
    return redirect(url_for('listings'))

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
    # get items from database
    if request.method == 'POST':
        try:
            itm = request.form['item']
            loc = request.form['location']
        
            con = sql.connect("bakemates.db")
            con.row_factory = sql.Row

            cur = con.cursor()
            cur.execute("SELECT *")

            rows = cur.fetchall()
            if len(rows) != 0:
                cur.execute()
                items = cur.fetchall()
    
        except:
            con.rollback()
    
        finally:
            return render_template('listings.html')
        con.close()


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
    return render_template('bakerhome.html')

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
