from flask import Flask, render_template, request, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash  # Import para manejo de contraseñas
import sqlite3  # Import para conectarse a la base de datos SQLite

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
import re

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Obtener los datos del formulario
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        # Validación del correo electrónico
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash('Invalid email address. Please enter a valid email.')
            return render_template('Signup.html')

        # Validación de la contraseña
        if len(password) < 8 or not re.search(r"[A-Z]", password) or not re.search(r"[a-z]", password) or not re.search(r"[0-9]", password):
            flash('Password must be at least 8 characters long, include at least one uppercase letter, one lowercase letter, and one number.')
            return render_template('Signup.html')

        # Encriptar la contraseña
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Conectar a la base de datos y registrar al usuario
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        try:
            cursor.execute('INSERT INTO users (username, password, first_name, last_name, email) VALUES (?, ?, ?, ?, ?)',
                           (username, hashed_password, first_name, last_name, email))
            conn.commit()
            return redirect('/signin')
        except sqlite3.IntegrityError:
            flash('Username already exists. Please choose a different one.')
        finally:
            conn.close()

    return render_template('Signup.html')


#SIGNIN page
# SIGNIN page
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        # Obtener los datos del formulario
        username = request.form['username']
        password = request.form['password']

        # Conectar a la base de datos y verificar al usuario
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

# Dashboard route
@app.route('/dashboard')
def dashboard():
    if 'username' in session:  # NEW: Check if the user is signed in
        username = session['username']
        return render_template('Dashboard.html', username=username)  # Pass the username to the template
    else:
        return redirect('/signin')  # Redirect to sign in if not logged in


# Ruta para ver los usuarios registrados
@app.route('/users')
def view_users():
    try:
        # Conectar a la base de datos y obtener los usuarios registrados
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        conn.close()
    except sqlite3.Error as e:
        # Mostrar mensaje de error si hay un problema al conectarse a la base de datos
        return f"An error occurred: {e}"
    
    # Renderizar la plantilla con los usuarios
    return render_template('view_users.html', users=users)


#DELETED USERS
@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    try:
        # Conectar a la base de datos y eliminar al usuario por ID
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()
        flash('User deleted successfully.')
    except sqlite3.Error as e:
        flash(f'An error occurred: {e}')

    return redirect('/users')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)