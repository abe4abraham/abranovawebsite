from src.common.database import Database
from src.models.user import User
from flask import Flask, session, request, render_template

app = Flask(__name__)  # '__main__'
app.secret_key = "abraham"

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/register')
def register_template():
    return render_template('home.html')


@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/auth/register', methods=['POST'])
def register_user():
    name = request.form['name']
    email = request.form['email']

    User.register(name, email)

    return render_template("profile.html", email=session['email'])



if __name__ == '__main__':
    app.run(port=5005, debug=True)