from flask import Blueprint
from flask.helpers import send_file

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return send_file('templates/login.html')

@auth.route('/logout')
def logout():
    return send_file('templates/logout.html')

@auth.route('/signup')
def signup():
    return send_file('templates/signup.html')


