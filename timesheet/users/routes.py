from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import login_user, current_user, logout_user, login_required
from timesheet import db
from datetime import datetime
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
            login_user(user) #remember me?
            day = Daily(time_in=datetime.now().strftime("%H:%M:%S"), user_id=current_user.name)
            db.session.add(day)
            db.session.commit()
            #Get userID
            #check Daily if already logged in today (?)
            #if yes, continue;
            #else, Add record to daily

            daily = Daily.query.all()
            # return redirect(url_for('main.posts_'))
            return redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='login', form=form)
    

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))