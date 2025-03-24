from flask import Flask, render_template, request, redirect, g
import sqlite3

app = Flask(__name__)  # Initialize Flask application
DATABASE = 'bookings.db'  # SQLite database file

# Function to connect to the database
def get_db():
    db = getattr(g, '_database', None)  # Check if a database connection already exists
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)  # Connect to SQLite database
        # Create table if it doesn't exist
        # Create bookings table if it does not exist
        db.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                name TEXT, 
                phone TEXT, 
                date TEXT, 
                time TEXT
            )
        """)  

        db.commit()  # Save changes
    return db  # Return database connection

# Close database connection after request is handled
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()  # Close connection

# Route for booking form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':  # If form is submitted
        name = request.form['name']  # Get name from form
        phone = request.form['phone']  # Get phone number from form
        date = request.form['date']  # Get selected date
        time = request.form['time']  # Get selected time
        db = get_db()  # Connect to database
        db.execute("INSERT INTO bookings (name, phone, date, time) VALUES (?, ?, ?, ?)",
                   (name, phone, date, time))  # Insert booking into database
        db.commit()  # Save changes
        return redirect('/')  # Redirect to bookings page
    return render_template('index.html')  # Render booking form template

# Route to view all bookings
@app.route('/bookings')
def bookings():
    db = get_db()  # Connect to database
    cursor = db.execute("SELECT * FROM bookings")  # Fetch all bookings
    bookings = cursor.fetchall()  # Store all bookings in a variable
    return render_template('bookings.html', bookings=bookings)  # Render admin panel template

# Route to delete a booking
@app.route('/delete/<int:id>')
def delete_booking(id):
    db = get_db()  # Connect to database
    db.execute("DELETE FROM bookings WHERE id = ?", (id,))  # Delete booking by ID
    db.commit()  # Save changes
    return redirect('/bookings')  # Redirect back to bookings page


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)  # Start the server in debug mode
