import sys
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import login_user, current_user, logout_user, login_required
from timesheet import db, bcrypt
from datetime import datetime, date
from timesheet.models import User, Daily
from timesheet.users.forms import LoginForm, RegistrationForm

users = Blueprint('users', __name__)
todays_datetime = datetime(datetime.today().year, datetime.today().month, datetime.today().day)

@users.route('/login', methods=['GET','POST'])
def login():

    def time_in(): #refactor

        check_user = Daily.query.filter_by(user_id=current_user.username).filter_by(date_today=todays_datetime).first()    #check if name and date today exists day.date_today.strftime("%Y/%m/%d
        if check_user is None:
            day = Daily(time_in=datetime.now().strftime("%H:%M"), user_id=current_user.username) #remove seconds
            db.session.add(day)
            db.session.commit()

            return day

        return None

    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
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

@users.route('/time_out')
@login_required
def time_out():

    user = Daily.query.filter_by(user_id=current_user.username).filter_by(date_today=todays_datetime).first()
    user.time_out = datetime.now().strftime("%H:%M")
    db.session.commit()
    flash('You have timed out!', 'success')
    daily = Daily.query.order_by(Daily.time_in.desc())


    return render_template('posts.html', title='Timed Out',
                           daily=daily)

@users.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.fname.data + ' ' + form.lname.data, username=form.username.data, email=form.email.data, 
                    position=form.position.data, password=hashed_password)
        
        #TODO validate if user already exists
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@users.route('/profile')
def profile():
    pass

