from flask import Flask, render_template, request, redirect, flash, session 


app = Flask(__name__)
app.secret_key = 'some_secret_key' 


#home page
@app.route('/')
def home():
    return render_template('Home.html')

#ABOUT page
@app.route('/about')
def about():
    return render_template('About.html')

#SIGNUP page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('Signup.html')
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form['password']
        
        # Connect to the database and insert the user
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            return redirect('/signin')
        except sqlite3.IntegrityError:
            flash('Username already exists. Please choose a different one.')  # NEW: Flash message for username conflict
        finally:
            conn.close()

    return render_template('Signup.html')


#SIGNIN page
# SIGNIN page
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    return render_template('Signin.html')
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form['password']
        
        # Connect to the database and verify the user
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session['username'] = username  # NEW: Store username in session
            return redirect('/dashboard')  # Redirect to dashboard if successful
        else:
            flash('Invalid username or password. Please try again.')  # NEW: Flash message for failed login

    return render_template('Signin.html')

# Dashboard route
@app.route('/dashboard')
def dashboard():
    if 'username' in session:  # NEW: Check if the user is signed in
        username = session['username']
        return render_template('Dashboard.html', username=username)  # Pass the username to the template
    else:
        return redirect('/signin')  # Redirect to sign in if not logged in



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)