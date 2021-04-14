from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, hData
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import random
from pprint import pprint
from datetime import datetime
import math

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
@login_required
def getData():
    if request.method == "POST":
        content = request.form
        # # keys are the "name"s of the form html items
        # # values are the values the users have entered
        # pprint(content.to_dict(flat=False))
        if content['action']=="Sleep":
            for i in range(10):
                print("Zzz..")
                dat = hData(date = datetime.today(), userId = current_user.id, hr = random.randint(40, 50), spo2 = random.randint(90, 97), bp = random.randint(110,140), cal = random.randint(20,30)/10, mode = 1)
                db.session.add(dat)
                db.session.commit()
        if content['action']=="Exercise":
            for i in range(10):
                print("Vroom")
                dat = hData(date = datetime.today(), userId = current_user.id, hr = random.randint(120, 150), spo2 = random.randint(95, 100), bp = random.randint(130,170), cal = random.randint(50,60)/10, mode = 2)
                db.session.add(dat)
                db.session.commit()
        return dashboard()
    return render_template("getData.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
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
            flash("Account created!", category="success")
            return redirect(url_for("views.home_page"))
        # flash("Account Created!", category="success")
        # return login()
    else:
        return render_template("signup.html")


@auth.route("/welcome")
@login_required
def welcome():
    return render_template("welcome.html", user=current_user)


@auth.route("/metrics")
@login_required
def metrics():
    a = hData.query.filter_by(userId=current_user.id).all()
    if len(a)==0:
        flash("No data collected, please run getData", category="error")
        return getData()
    a.reverse()
    hb = []
    bp = []
    sp = []
    cal = []

    i=0
    for x in a:
        i+=1
        hb.append(x.hr)
        bp.append(x.bp)
        sp.append(x.spo2)
        cal.append(x.cal)
        if i==5:
            mode = x.mode
        if i>9:
            break
    hrv = 0
    for i in range(8):
        hrv+=(hb[i+1]-hb[i])*(hb[i+1]-hb[i])
    hrv=hrv/8
    hrv = math.sqrt(hrv)

    if mode==1:
        printstr = "Sleep Mode"
        printstr1 = 'Variance of Heart Rate: '+str(hrv)
        printstr2 = ''
    else:
        printstr = "Excercise Mode"
        printstr1 = ''
        printstr2 = 'Calories Burnt in an hour of Excercise: '+str(60*sum(cal)/len(cal))

    return render_template("metrics.html", user=current_user, printstr = printstr, hrv = hrv, max_hb = max(hb), min_hb = min(hb), avg_hb = sum(hb)/len(hb),
        max_bp = max(bp), min_bp = min(bp), avg_bp = sum(bp)/len(bp), max_sp = max(sp), min_sp = min(sp), avg_sp = sum(sp)/len(sp), 
        max_cal = max(cal), min_cal = min(cal), avg_cal = sum(cal)/len(cal), printstr1 = printstr1, printstr2 = printstr2
    )
    


@auth.route("/dashboard")
@login_required
def dashboard():
    a = hData.query.filter_by(userId=current_user.id).all()
    if len(a)==0:
        flash("No data collected, please run getData", category="error")
        return getData()

    a.reverse()
    list_10 = []
    time_list = []
    i=0
    for x in a:
        i+=1
        list_10.append(x)
        time_list.append(int(abs(x.date.microsecond)/1000))
        if i>9:
            break
    time_list.sort()
    list_10.reverse()

    dataset = dict()
    vals = ["hb", "bp", "sp", "calories"]
    
    for measure in vals:
        dataset[measure] = []
    
    for i in range(9):
        dataset["hb"].append({"x": time_list[i], "y": list_10[i].hr})
    for i in range(9):
        dataset["bp"].append({"x": time_list[i], "y": list_10[i].bp})
    for i in range(9):
        dataset["sp"].append({"x": time_list[i], "y": list_10[i].spo2})
    for i in range(9):
        dataset["calories"].append({"x": time_list[i], "y": list_10[i].cal})
    mode = list_10[5].mode
    if mode==1:
        printstr = "Sleep Mode"
    else:
        printstr = "Excercise Mode"
    return render_template("dashboard.html", data=dataset, user=current_user, printstr=printstr)
