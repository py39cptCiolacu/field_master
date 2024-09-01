from __future__ import annotations

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from .models import User, Land
from website import db
from .helpers.views_helpers import prompt_handler

views = Blueprint("views", __name__)

points = []  

@views.route('/api/v1/user_profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user).first()
    if user is None:
        return jsonify({"message": "User not found"}), 404
    
    print(len(user.lands))
    print(user.id)

    user_profile = {
        "username": user.username,
        "email": user.email,
        "number_of_lands": len(user.lands),
        "lands": [{'id': land.id, 'name': land.name, 'size': land.get_area_surface()} for land in user.lands]  
    }
    return jsonify(user_profile), 200


@views.route('/api/v1/update_username', methods=['POST'])
@jwt_required()
def update_username():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    new_username = data.get('username')

    if not new_username:
        return jsonify({'error': 'Username cannot be empty'}), 400

    # Verifică dacă username-ul este deja folosit de un alt utilizator
    if User.query.filter_by(username=new_username).first():
        return jsonify({'error': 'Username already taken'}), 400

    # Actualizează username-ul utilizatorului curent
    user.username = new_username
    db.session.commit()

    return jsonify({'message': 'Username updated successfully', 'username': new_username}), 200


@views.route("/api/v1/add_land", methods=["POST"])
@jwt_required()
def add_land():

    current_user_jwt = get_jwt_identity()
    current_user = User.query.filter_by(email=current_user_jwt).first()

    data = request.json
    points = data.get("points", [])
    name = data.get("name")

    if len(points) != 4:
        return jsonify({'error' : 'You must provide exactly 4 points'}), 400
    
    print(points)
    print(name)
    new_land = Land(name=name, user_id=current_user.id,
                    x1=points[0][0],
                                 y1=points[0][1],
                                 x2=points[1][0],
                                 y2=points[1][1],
                                 x3=points[2][0],
                                 y3=points[2][1],
                                 x4=points[3][0],
                                 y4=points[3][1])

    surface = new_land.get_area_surface()
    print(surface)

    if surface > 3.00:
        return jsonify({'message': 'The surface must be smaller then 3'}), 400

    db.session.add(new_land)
    db.session.commit()
    return jsonify({'message': 'Land added succesfully'}), 200


@views.route("api/v1/get_coordinates", methods=["POST"])
# @jwt_required()
def get_coordinates() -> dict:

    global points
    data = request.get_json()
    lat = data.get("lat")
    lng = data.get("lng")
    points.append((lat, lng))

    if len(points) > 4:
        points = points[-4:]

    response = {
        'lat': lat,
        'lng': lng,
        'points': points if len(points) == 4 else []
    }
    # print(response)

    return jsonify(response)
  
@views.route('/api/v1/user_lands', methods=['GET'])
@jwt_required()
def get_user_lands():
    current_user_jwt = get_jwt_identity()
    current_user = User.query.filter_by(email=current_user_jwt).first()
    if current_user is None:
        return jsonify({"message": "User not found"}), 404
    
    lands = [{'id': land.id, 'name': land.name} for land in current_user.lands]
    return jsonify(lands), 200



@views.route("/api/v1/analysis", methods=["GET", "POST"])
@jwt_required()  # Asigură-te că utilizatorul este autentificat
def analysis():
    current_user_email = get_jwt_identity()  # Obține ID-ul utilizatorului logat

    # Găsim utilizatorul logat după ID
    user = User.query.filter_by(email=current_user_email).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Obținem toate terenurile asociate utilizatorului
    lands = Land.query.filter_by(user_id=user.id).all()

    # Extragem numele terenurilor
    land_names = [land.name for land in lands]

    if request.method == "POST":
        data = request.json

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        response = prompt_handler(data)

        return jsonify({
            'message': 'Data received successfully',
            'received_data': data,
            'land_names': land_names,  # Adăugăm numele terenurilor în răspuns
            'cdsapi_infos' : response
        })

    if request.method == "GET":
        # Returnăm doar numele terenurilor dacă se face un GET
        return jsonify({
            'message': 'Lands retrieved successfully',
            'land_names': land_names
        })