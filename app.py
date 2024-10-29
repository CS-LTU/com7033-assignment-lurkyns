from flask import Flask, render_template 

app = Flask(__name__)

#home page
@app.route('/')
def home():
    return render_template('Home.html')
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)