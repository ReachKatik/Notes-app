from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# create a database to store signup user accounts
db = SQLAlchemy()
DB_NAME = 'database.db'

# create app using flask
def create_app():
    app = Flask(__name__)
    # secret key for our application any random string
    app.config['SECRET_KEY'] = 'My first app'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    # we need to import our pages
    from .views import views
    from .auth import auth
    # prefix will consider our python file name when we just mention /
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    from .models import User, Note
    create_database(app)
    # this is needed to find the user details
    login_manager = LoginManager()
    # where should user go when not logged it, it should go login page
    login_manager.login_view = 'auth.login'
    # use our app to login
    login_manager.init_app(app)
    
    # this login manager by itself finds the primary key from database
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

def create_database(app):
    if not path.exists('instance/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print('Created Database in instance folder')
