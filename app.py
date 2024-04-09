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

#NEED TO ADD ALL BAKER STUFF
#NEED TO ADD BAKERHOME.html
#NEED TO ADD ADDITEM.html

if __name__ == "__main__":
    app.run(debug=True)
