from dotenv import load_dotenv
import os
import redis

load_dotenv()

DB_NAME = "database.db"

class ApplicationConfig:
    SECRET_KEY = "asdasdasfasfasfasfwetgfb43"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI =  f"sqlite:///{DB_NAME}"

    SESSION_TYPE = "redis"
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.from_url("redis://127.0.0.1:6379")


