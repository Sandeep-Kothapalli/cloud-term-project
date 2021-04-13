from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import random
from pprint import pprint

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        content = request.form
        # keys are the "name"s of the form html items
        # values are the values the users have entered
        # {'inputEmail': ['testing@kgp.com'], 'inputPassword': ['kgptester']}
        email = content["inputEmail"]
        password = content["inputPassword"]

        user = User.query.filter_by(email=email).first()
        # print(user)
        if user:
            # pass
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category="success")
                login_user(user, remember=True)
                # return redirect(url_for("views.welcome_page"))
                return welcome()
            else:
                flash("Incorrect password!!", category="error")
                return render_template("login.html")
        else:
            flash("Email does not exist.", category="error")
            return render_template("login.html")
    else:
        return render_template("login.html")


@auth.route("/getData", methods=["GET", "POST"])
def getData():
    if request.method == "POST":
        content = request.form
        # keys are the "name"s of the form html items
        # values are the values the users have entered
        pprint(content.to_dict(flat=False))
    return render_template("getData.html")


@auth.route("/logout")
def logout():
    return render_template("homepage.html")


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        content = request.form
        # pprint(content.to_dict(flat=False))
        email = content["inputEmail"]
        first_name = content["first_name"]
        password1 = content["inputPassword"]
        password2 = content["confirmPassword"]

        user = User.query.filter_by(email=email).first()

        if user:
            flash("Email already exists.", category="error")
        elif len(email) < 4:
            flash("Email must be greater than 3 characters.", category="error")
        elif len(first_name) < 2:
            flash(
                "First name must be greater than 1 character.", category="error"
            )
        elif password1 != password2:
            flash("Passwords don't match.", category="error")
        elif len(password1) < 7:
            flash("Password must be at least 7 characters.", category="error")
        else:
            new_user = User(
                email=email,
                first_name=first_name,
                password=generate_password_hash(password1, method="sha256"),
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created!", category="success")
            return redirect(url_for("views.home_page"))
        # flash("Account Created!", category="success")
        # return login()
    else:
        return render_template("signup.html", user=current_user)


@auth.route("/welcome")
def welcome():
    return render_template("welcome.html")


@auth.route("/metrics")
def metrics():
    return render_template("metrics.html")


@auth.route("/dashboard")
def dashboard():

    dataset = dict()
    vals = ["hb", "bp", "sp", "calories"]

    for measure in vals:
        dataset[measure] = []
        x = []
        y = []
        for i in range(10):
            tx = random.randint(0, 100) / 10
            ty = random.randint(900, 1000) / 10
            x.append(tx)
            y.append(ty)
        x.sort()

        for i in range(10):
            dataset[measure].append({"x": x[i], "y": y[i]})

    return render_template("dashboard.html", data=dataset)
