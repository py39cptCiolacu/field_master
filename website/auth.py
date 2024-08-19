from __future__ import annotations

from flask import Blueprint, request, jsonify, session
from flask_jwt_extended import create_access_token, unset_jwt_cookies, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash

from .models import User
from .auth_helpers import is_valid_user

from . import db

auth = Blueprint("auth", __name__)

@auth.route("/api/v1/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400
    
    user = User.query.filter_by(email=email).first()
    
    if not user:
        return jsonify({"message": "No such user"}), 401
    elif not check_password_hash(user.password, password):
        return jsonify({"message": "The password is incorrect"}), 401
    else:
        access_token = create_access_token(identity=email)
        response = jsonify({"access_token":access_token})
        return response



@auth.route("/api/v1/register", methods = ["GET", "POST"])
def register():
    
    data = request.json
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    password_confirm = data.get("passwordConfirm")

    user = User.query.filter_by(email=email).first()

    is_valid = is_valid_user(user, username, email, password, password_confirm)

    if not is_valid.is_valid:
        return jsonify({"message" : f"{is_valid.flash_message}"}), 401
    else:
        new_user = User(email=email, username=username, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        access_token = create_access_token(identity=email)
        response = jsonify({"access_token":access_token})
        return jsonify({"message": "Account created"}), 200

   

@auth.route("/api/v1/logout")
@jwt_required()
def logout():
    response = jsonify({"message": "logout succesful"})
    unset_jwt_cookies(response)    
    return response