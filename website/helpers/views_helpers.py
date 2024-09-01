import folium
import json
import os

from flask_jwt_extended import get_jwt_identity

from copernicus_api.fetch_request import get_cdsapi_infos
from ai.prompt import generate_weather_prompt
from ai.get_response import generate_response
from ..models import User, Land


def prompt_handler(data) -> str:
    fetch_dict = get_fetch_dict(data)
    cdsapi_data = get_cdsapi_infos(fetch_dict)
    prompt = generate_weather_prompt(cdsapi_data)
    response = generate_response(prompt)

    print(prompt)
    return response

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