from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = b'_5#y2L"F4Q8z\n\xec]/'
    #  Point SQLAlchemy to your Heroku database

    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "postgresql://xahcyphjjmgxvz:651b27e87aa615c908154f307b153049159ac6ebbd17d1711ae2daa822c14147@ec2-52-0-67-144.compute-1.amazonaws.com:5432/d4nlpv1l1kqttb"
    #   Gets rid of a warning
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    return app
