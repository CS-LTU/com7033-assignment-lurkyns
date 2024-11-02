from flask import Flask, render_template 

app = Flask(__name__)

#home page
@app.route('/')
def home():
    return render_template('Home.html')

#ABOUT page
@app.route('/about')
def about():
    return render_template('About.html')

#SIGNUP page
@app.route('/signup')
def signup():
    return render_template('Signup.html')

#SIGNIN page
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    return render_template('Singin.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)