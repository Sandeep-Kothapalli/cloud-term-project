from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import hData
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def getData():
    if request.method == 'POST':
        #need to modify
        note = request.form.get('note')

        if len(note) < 1:
            flash('Invalid data @', category='error')
        else:
            new_note = hData(userId=userId, hr=hr, spo2=spo2, bp=bp, cal=cal)
            db.session.add(new_note)
            db.session.commit()
            # flash('row added!', category='success')

    return render_template("getData.html", user=current_user)
