from __future__ import annotations

from flask import Blueprint, render_template, request, jsonify, session
from flask_jwt_extended import jwt_required, get_jwt_identity

from .models import User, Land
from website import db

import folium
import json
import os

from copernicus_api.fetch_request import get_cdsapi_infos
from ai.prompt import generate_weather_prompt_v2

views = Blueprint("views", __name__)

points = []  # dc l am initializat pe asta aici? 

# @views.route('/api/v1/user_profile', methods=['GET'])
# @jwt_required()
# def user_profile():
#     current_user = get_jwt_identity()
#     print(current_user)
#     user = User.query.filter_by(email=current_user).first()
#     if user:
#         return jsonify(logged_in_as=current_user, email=user.email, username=user.username), 200
#     return jsonify(message="User not found"), 404

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

        print("Received data:", data)
        print("Parametrii: ", data["parameters"])

        fetch_dict = get_fetch_dict(data)
        response = get_cdsapi_infos(fetch_dict)
    
        return jsonify({
            'message': 'Data received successfully',
            'received_data': data,
            'land_names': land_names,  # Adăugăm numele terenurilor în răspuns
            'cdsapi_infos' : response
        })

    elif request.method == "GET":
        # Returnăm doar numele terenurilor dacă se face un GET
        return jsonify({
            'message': 'Lands retrieved successfully',
            'land_names': land_names
        })
    
# @jwt_required
def get_fetch_dict(data) -> dict:

    current_user_email = get_jwt_identity()
    current_user = User.query.filter_by(email=current_user_email).first()

    current_land = Land.query.filter_by(user_id = current_user.id).filter_by(name = data["field"]).first() 

    parameters_map = {
        'Temperature at 2 meters': "2m_temperature",
        'Total Precipitation' : "total_precipitation",
        'Soil Moisture (top layer)' : 'volumetric_soil_water_layer_1',
        'Solar Radiation at the surface' : 'surface_solar_radiation_downwards',
        'Relative Humidity' : '2m_dewpoint_temperature',
        'Wind Speed (u component)' : '10m_u_component_of_wind',  
        'Wind Speed (v component)' : '10m_v_component_of_wind',
        'Soil Temperature at level 1' : 'soil_temperature_level_1'
    }

    parameters_lists = []

    for param in data["parameters"]:
        parameters_lists.append(parameters_map[param])

    year = data["start_date"][0:4]
    month = data["start_date"][5:7]

    start_day = data["start_date"][8:10]
    end_day = data["end_date"][8:10]

    int_current_day = int(start_day)
    int_end_day = int(end_day)

    days = []
    while int_current_day <= int_end_day:

        if int_current_day >=10:
            days.append(str(int_current_day))
        else:
            day_to_append = '0' + str(int_current_day)
            days.append(day_to_append)
        
        int_current_day +=1 

    print(current_land.get_limits())

    fetch_dict = {
        "user" : current_user.id,
        "land" : current_land.id,
        "parameters": parameters_lists,
        "year" : year,
        "month": [month],
        "day" : [days],
        "area" : current_land.get_limits()
    }

    return fetch_dict


@views.route("/test")
def test_promt():

    JSON_FILE_NAME = "daniel1234_test_land_2024_08_11_22_24_06_final.json"
    print(os.getcwd())
    with open(JSON_FILE_NAME, 'r') as file:
        weather_data = json.load(file)

    prompts = generate_weather_prompt_v2(weather_data)
    print(prompts)

    return "<h1> ALL GOOD </h1>"