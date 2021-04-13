from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class hData(db.Model):
    __tablename__ = "healthData"

    date = db.Column(
        db.DateTime(timezone=True), default=func.now(), primary_key=True
    )
    userId = db.Column(
        db.Integer, db.ForeignKey("usert.id")
    )  ##take care while defining user database
    hr = db.Column(db.Integer)
    spo2 = db.Column(db.Integer)
    bp = db.Column(db.Integer)
    cal = db.Column(db.Integer)
    mode = db.Column(db.Integer)

    def __init__(self, date, userId, hr, spo2, bp, cal, mode):
        self.date = date
        self.userId = userId
        self.hr = hr
        self.spo2 = spo2
        self.bp = bp
        self.cal = cal
        self.mode = mode

    def __repr__(self):
        pass


# add user class for user database


class User(db.Model, UserMixin):
    __tablename__ = "usert"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    health_data = db.relationship("hData")
