import sys
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import login_user, current_user, logout_user, login_required
from timesheet import db
from datetime import datetime, date
from timesheet.models import User, Daily
from timesheet.users.forms import LoginForm

users = Blueprint('users', __name__)

@users.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            time_in()

            return redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='login', form=form)
    

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


def time_in(): #refactor
    todays_datetime = datetime(datetime.today().year, datetime.today().month, datetime.today().day)

    check_user = Daily.query.filter_by(user_id=current_user.name).filter_by(date_today=todays_datetime).first()    #check if name and date today exists day.date_today.strftime("%Y/%m/%d
    if check_user is None:
        day = Daily(time_in=datetime.now().strftime("%H:%M"), user_id=current_user.name) #remove seconds
        db.session.add(day)
        db.session.commit()

        return day

    return None
