from flask import Blueprint, render_template, request, flash
from pprint import pprint

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        content = request.form
        #name of the form elements
        pprint(content.to_dict(flat=False))
    return render_template("login.html")

@auth.route('/getData', methods=['GET', 'POST'])
def getData():
    if request.method == 'POST':
        content = request.form
        # keys are the "name"s of the form html items
        # values are the values the users have entered
        pprint(content.to_dict(flat=False))
    return render_template("getData.html")


@auth.route('/logout')
def logout():
    return render_template("logout.html")


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        content = request.form
        pprint(content.to_dict(flat=False))
    return render_template("signup.html")


