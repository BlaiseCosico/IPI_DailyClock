from flask import Flask
from timesheet.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    from timesheet.main.routes import main
    from timesheet.users.routes import users

    app.register_blueprint(main)
    app.register_blueprint(users)
    
    return app