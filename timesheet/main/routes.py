import sys
from flask import Blueprint, render_template, request
from datetime import datetime, date, timedelta
from timesheet.models import Daily

main = Blueprint('main', __name__)

posts = [
    {
        'name': 'Blaise Cosico',
        'position': 'Developer',
        'time_in': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'time_out': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    },
    {
        'name': 'Corey Schafer',
        'position': 'Developer',
        'time_in': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'time_out': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
]

@main.route('/')
@main.route('/home')
def home():
    # daily = Daily.query.all()
    daily = Daily.query.order_by(Daily.time_in.desc()) #.paginate(page=page, per_page=5)
    return render_template('homepage.html', title='Homepage', daily=daily)

@main.route('/posts')
def posts_():
    # print(f'datetime now: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', file=sys.stderr)
    # print(f'date now: {date.today()}', file=sys.stderr)
    # print(f'time now: {datetime.now().strftime("%H:%M:%S")}', file=sys.stderr)
    return render_template('posts.html', posts=posts)
