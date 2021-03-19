from flask import Blueprint, render_template
from flask.helpers import send_file

        #name of the form elements
views = Blueprint('views', __name__)

@views.route('/')
def home_page():
    return render_template("homepage.html")
