from flask import Blueprint
from flask.helpers import send_file

views = Blueprint('views', __name__)

@views.route('/')
def home_page():
    return send_file('templates/homepage.html')