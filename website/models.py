from . import db
from sqlalchemy.dialects.postgresql import JSON


class hData(db.Model):
    __tablename__ = 'healthData'

    date = db.Column(db.DateTime(timezone=True), default=func.now(), primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('usert.id')) ##take care while defining user database
    hr = db.Column(db.Integer)
    spo2 = db.Column(db.Integer)
    bp = db.Column(db.Integer)
    cal = db.Column(db.Integer)

    def __init__(self, date, userId, hr, spo2, bp, cal):
        self.date = date
        self.userId = userId
        self.hr = hr
        self.spo2 = spo2
        self.bp = bp
        self.cal = cal
    

    def __repr__(self):
        pass
        

#add user class for user database
