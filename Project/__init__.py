from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()
DB_Name = "Book_my_show.sqlite"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'My secret key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_Name}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')

    from .models import User, Venue

    login_manager = LoginManager()
    login_manager.login_view = 'auth.Login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    with app.app_context():
        db.create_all()
        user = User.query.filter_by(email='admin@gmail.com').first()
        if user:
            pass
        else:
            first_user = User(email = 'admin@gmail.com', name = 'Admin', password = generate_password_hash('admin', method='scrypt'), isadmin = True)
            db.session.add(first_user)
            db.session.commit()

    return app 