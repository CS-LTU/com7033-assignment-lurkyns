from flask import Flask, render_template, request, redirect, url_for  # Import necessary Flask functions
from IPython.display import display, HTML  # Import HTML for displaying in Jupyter Notebook if needed

# Initialize the Flask application
app = Flask(__name__)

# Store registered users in memory (for simplicity)
users = []

# Route for the Home page
@app.route('/')
def home():
    return render_template('home.html')  # Render the home page HTML file

# Route for the About page
@app.route('/about')
def about():
    return render_template('about.html')  # Render the about page HTML file

# Route for the Contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')  # Render the contact page HTML file

# Route for User Registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users.append({'username': username, 'password': password})  # Store the username and password
        return redirect(url_for('home'))  # Redirect to the home page after registration
    return render_template('register.html')  # Render the register page HTML file

# Route for Data Display page
@app.route('/data')
def data():
    return render_template('data.html')  # Render the data display HTML file

# Function to run the Flask app
def run_flask():
    # Display a link to open the Flask app in a new browser tab
    display(HTML('<a href="http://127.0.0.1:5000" target="_blank">Click here to open Flask app</a>'))
    app.run(host='0.0.0.0', port=5000)

# Run the Flask application
if __name__ == '__main__':
    run_flask()  # Start the Flask app
