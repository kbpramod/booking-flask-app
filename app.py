from flask import Flask, render_template, request, redirect, g, session
import sqlite3

app = Flask(__name__)
DATABASE = 'bookings.db'
app.secret_key = "your_secret_key"  # Needed for session management

# Hardcoded admin credentials
ADMIN_USER = "admin"
ADMIN_PASS = "pass"

# Function to connect to the database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                name TEXT, 
                phone TEXT, 
                date TEXT, 
                time TEXT
            )
        """)
        db.commit()
    return db

# Close database connection after request is handled
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Route for booking form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        date = request.form['date']
        time = request.form['time']
        db = get_db()
        db.execute("INSERT INTO bookings (name, phone, date, time) VALUES (?, ?, ?, ?)",
                   (name, phone, date, time))
        db.commit()
        return redirect('/')
    return render_template('index.html')

# Route to view bookings and login in one page
@app.route('/bookings', methods=['GET', 'POST'])
def bookings():
    if request.method == 'POST':
        # Handle admin login
        username = request.form.get('Username')
        password = request.form.get('password')

        if username == ADMIN_USER and password == ADMIN_PASS:
            session['admin'] = True  # Store admin session
        else:
            return render_template('bookings.html', error="Invalid credentials", bookings=[])

    if 'admin' not in session:
        return render_template('bookings.html', error=None, bookings=[])

    # Fetch and display bookings if admin is logged in
    db = get_db()
    cursor = db.execute("SELECT id, name, phone, date, time FROM bookings")
    bookings = cursor.fetchall()
    return render_template('bookings.html', error=None, bookings=bookings)

# Route to delete a booking (Only Admins Can Delete)
@app.route('/delete/<int:id>')
def delete_booking(id):
    if 'admin' not in session:
        return redirect('/bookings')

    db = get_db()
    db.execute("DELETE FROM bookings WHERE id = ?", (id,))
    db.commit()
    return redirect('/bookings')

# Logout Route
@app.route('/logout')
def logout():
    session.pop('admin', None)  # Remove admin session
    return redirect('/bookings')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
