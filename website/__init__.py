from __future__ import annotations
from datetime import timedelta, datetime, timezone
from os import path
import json

from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from flask_jwt_extended import JWTManager, get_jwt, create_access_token, get_jwt_identity

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app() -> Flask:
    app = Flask(__name__)
    jwt = JWTManager(app)
    
    app.config["SECRET_KEY"] = "a random string"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_COOKIE_NAME'] = "cookie_name"
    app.config["SESSION_COOKIE_SECURE"] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
    app.config['USE_SESSION_FOR_NEXT'] = True
    app.config["JWT_SECRET_KEY"] = "some random string"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

    db.init_app(app)
    CORS(app, supports_credentials=True)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    @app.after_request
    def reresh_expiring_jwts(response):
        try:
            exp_timestamp = get_jwt()["exp"]
            now = datetime.now(timezone.utc)
            target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
            if target_timestamp > exp_timestamp:
                access_token = create_access_token(identity=get_jwt_identity())
                data = response.get_json()
                if type(data) is dict:
                    data["access_token"] = access_token
                    response.data = json.dumps(data)
            return response
        except (RuntimeError, KeyError):
            return response

    create_database(app)
    
    return app

def create_database(app: Flask) -> None:
    if not path.exists("website/" + DB_NAME):
        with app.app_context():
            db.create_all()
            print("Database Created")
    else:
        print("db exists")
