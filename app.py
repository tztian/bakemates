from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__, static_url_path='/static')

# Function to connect to MySQL database
def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="bakemates"
    )
    return connection

@app.route('/')
def index():
    return render_template('landing.html')

# Route to handle search form submission and redirect to listings page
@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    # HERE WE SHOULD CHECK IF IT IS VALID 
    return redirect('/listings')

@app.route('/listings')
def listings():
   # connection = get_db_connection()
   # cursor = connection.cursor(dictionary=True)
   # cursor.execute('SELECT DISTINCT category FROM Item')  # Fetch distinct categories
   # categories = [row['category'] for row in cursor.fetchall()]
   # cursor.execute('SELECT * FROM Item')
   # items = cursor.fetchall()
   # cursor.close()
   # connection.close()
   # return render_template('listings.html', items=items, categories=categories)
    return render_template('listings.html')

# Route to filter items by category for listings page
@app.route('/filter', methods=['POST'])
def filter_items():
    category = request.form['category']
    if category == 'All':
        return redirect('/listings')
    else:
      #  connection = get_db_connection()
      #  cursor = connection.cursor(dictionary=True)
      #  cursor.execute('SELECT * FROM Item WHERE category = %s', (category,))
      #  items = cursor.fetchall()
      #  cursor.close()
      #  connection.close()
        return render_template('listings.html', items=items)

if __name__ == "__main__":
    app.run(debug=True)
