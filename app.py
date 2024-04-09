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

@app.route('/listings')
def listings():
    # get items from database
    return render_template('listings.html')

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
    # Logic to handle editing the baker's profile
    return render_template('editbaker.html')

if __name__ == "__main__":
    app.run(debug=True)
