from datetime import datetime, date
from timesheet import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False) #Blaise Cosico
    username = db.Column(db.String(20), unique=True, nullable=False) #C81440
    email = db.Column(db.String(120), unique=True, nullable=False)
    position = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    daily = db.relationship('Daily', backref='employee', lazy=True) #fix naming convention

    def __repr__(self):
        return f"User('{self.username}', '{self.position}')"
    
class Daily(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_today = db.Column(db.DateTime, nullable=False, default=date.today) #default=datetime.utcnow
    time_in = db.Column(db.String(20), nullable=True) #SQLite DateTime type only accepts Python datetime and date objects as input.
    time_out = db.Column(db.String(20), nullable=True)
    user_id = db.Column(db.String, db.ForeignKey('user.username'), nullable=False)

    def __repr__(self):
        return f"Daily('{self.user_id}', '{self.date_today}')"  