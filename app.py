from flask import Flask, render_template, request, redirect, flash, session
#Werkzeug for hashing passwords to enhance security
from werkzeug.security import generate_password_hash, check_password_hash
# SQLite and Mongo for handling relational database operations
import sqlite3
import pymongo
# Logging for tracking events and debugging
import logging
import re


# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'Leeds'

# Set up logging
logging.basicConfig(level=logging.INFO)

# MongoDB connection setup
try:
    client = pymongo.MongoClient("mongodb+srv://lurkynsosa:KAm7sqhZkO27JWox@osa.oskhg.mongodb.net/healthcareDB?retryWrites=true&w=majority")
    db = client['healthcareDB']
    collection = db['stroke_data']
    logging.info("Connected to MongoDB successfully.")
except Exception as e:
    logging.error(f"Error connecting to MongoDB: {e}")

# SQLite connection setup
def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            username TEXT UNIQUE,
            password TEXT NOT NULL,
            gender TEXT,
            age INTEGER,
            hypertension INTEGER,
            ever_married TEXT,
            work_type TEXT,
            residence_type TEXT,
            avg_glucose_level REAL,
            bmi REAL,
            smoking_status TEXT,
            stroke INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_sqlite_db()

# Home Page
@app.route('/')
def home():
    return render_template('Home.html')

# About Page
@app.route('/about')
def about():
    return render_template('About.html')

# Signup Page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        gender = request.form['gender']
        age = request.form['age']
        hypertension = request.form['hypertension']
        ever_married = request.form['ever_married']
        work_type = request.form['work_type']
        residence_type = request.form['residence_type']
        avg_glucose_level = request.form['avg_glucose_level']
        bmi = request.form['bmi']
        smoking_status = request.form['smoking_status']
        stroke = request.form['stroke']

        # Email validation
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash('Invalid email address. Please enter a valid email.')
            return render_template('Signup.html')

        # Password validation
        if len(password) < 8 or not re.search(r"[A-Z]", password) or not re.search(r"[a-z]", password) or not re.search(r"[0-9]", password):
            flash('Password must be at least 8 characters long, include at least one uppercase letter, one lowercase letter, and one number.')
            return render_template('Signup.html')

        # Encrypt the password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Insert user into SQLite
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (username, password, first_name, last_name, email, gender, age, hypertension, ever_married, work_type, residence_type, avg_glucose_level, bmi, smoking_status, stroke)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (username, hashed_password, first_name, last_name, email, gender, age, hypertension, ever_married, work_type, residence_type, avg_glucose_level, bmi, smoking_status, stroke))
            conn.commit()
            return redirect('/signin')
        except sqlite3.IntegrityError:
            flash('Username already exists. Please choose a different one.')
        finally:
            conn.close()

    return render_template('Signup.html')

# Signin Page
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verify user credentials
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[0], password):
            session['username'] = username
            return redirect('/dashboard')
        else:
            flash('Invalid username or password. Please try again.')

    return render_template('Signin.html')

# Dashboard Page
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']
        
        # Fetch user details from the database
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('''
                SELECT first_name, last_name, email, gender, age, hypertension, ever_married, work_type, residence_type, avg_glucose_level, bmi, smoking_status, stroke 
                FROM users WHERE username = ?
            ''', (username,))
            user_details = cursor.fetchone()
            conn.close()
            
            # Ensure user_details were found
            if user_details is None:
                flash('User not found. Please sign in again.')
                return redirect('/signin')
            
            # Create a dictionary for user details to pass to the template
            user_details_dict = {
                'first_name': user_details[0],
                'last_name': user_details[1],
                'email': user_details[2],
                'gender': user_details[3],
                'age': user_details[4],
                'hypertension': 'Yes' if user_details[5] == 1 else 'No',
                'ever_married': user_details[6],
                'work_type': user_details[7],
                'residence_type': user_details[8],
                'avg_glucose_level': user_details[9],
                'bmi': user_details[10],
                'smoking_status': user_details[11],
                'stroke': 'Yes' if user_details[12] == 1 else 'No'
            }

            # Pass user details to the template
            return render_template('Dashboard.html', username=username, user_details=user_details_dict)

        except sqlite3.Error as e:
            flash(f'An error occurred while retrieving user details: {e}', 'danger')
            return redirect('/signin')
    else:
        return redirect('/signin')

# View Users Page
@app.route('/view_users')
def view_users():
    try:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, first_name, last_name, email FROM users")
            users = cursor.fetchall()
    except sqlite3.Error as e:
        flash(f"An error occurred while retrieving users: {e}", "danger")
        return redirect('/')

    return render_template('view_users.html', users=users)

# Delete User Route
@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        flash('User deleted successfully.')
    except sqlite3.Error as e:
        flash(f'An error occurred: {e}')

    return redirect('/view_users')

# Upload CSV Route
@app.route('/upload', methods=['GET', 'POST'])
def upload_csv():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect('/upload')

        file = request.files['file']

        if file.filename == '':
            flash('No selected file', 'error')
            return redirect('/upload')

        if file and file.filename.endswith('.csv'):
            try:
                df = pd.read_csv(file)
                data_dict = df.to_dict(orient='records')
                collection.insert_many(data_dict)
                flash('File successfully uploaded and data stored in MongoDB!', 'success')
                return redirect('/')
            except Exception as e:
                flash(f'An error occurred while reading the file: {e}', 'error')
                return redirect('/upload')
        else:
            flash('Please upload a CSV file.', 'error')

    return render_template('upload.html')

# View Data from MongoDB
@app.route('/view')
def view_data():
    data = list(collection.find())
    return render_template('view_data.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
