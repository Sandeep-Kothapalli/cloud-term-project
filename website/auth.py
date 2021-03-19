from flask import Blueprint, render_template, request, flash
from pprint import pprint
import random

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        content = request.form
        #name of the form elements
        pprint(content.to_dict(flat=False))
        return render_template("welcome.html")
    else:
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
    return render_template("homepage.html")


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        content = request.form
        pprint(content.to_dict(flat=False))
        flash('Account Created!', category='success')
        return login()
    else:
        return render_template("signup.html")


@auth.route('/welcome')
def welcome():
    return render_template("welcome.html")

@auth.route('/metrics')
def metrics():
    return render_template("metrics.html")

@auth.route('/dashboard')
def dashboard():
    
    dataset = dict()
    vals = ['hb', 'bp', 'sp', 'calories']

    for measure in vals:
        dataset[measure] = []
        x = []
        y = []
        for i in range(10):
            tx = random.randint(0,100)/10
            ty = random.randint(900,1000)/10
            x.append(tx)
            y.append(ty)
        x.sort()

        for i in range(10):
            dataset[measure].append({'x':x[i], 'y':y[i] })

    return render_template("dashboard.html", data=dataset)
