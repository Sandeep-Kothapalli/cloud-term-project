from flask import Blueprint, render_template
from flask.helpers import send_file

views = Blueprint('views', __name__)

@views.route('/')
def home_page():
    return render_template("homepage.html")

# @views.route('/welcome')
# def welcome_page():
#     return render_template("welcome.html")
