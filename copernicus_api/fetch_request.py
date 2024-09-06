import cdsapi
from website.models import User, Land
from .nc_to_json import nc_to_json_convertor, process_json
from datetime import datetime
import json

c = cdsapi.Client()

VALID_VARIABLES = [
            '2m_temperature',                    # Temperatura la 2 metri
            'total_precipitation',               # Precipitații totale
            'volumetric_soil_water_layer_1',     # Umiditatea solului (primul strat)
            'surface_solar_radiation_downwards', # Radiația solară la suprafață
            '2m_dewpoint_temperature',           # Umiditatea relativă
            '10m_u_component_of_wind',           # Viteza vântului (componenta u)
            '10m_v_component_of_wind',           # Viteza vântului (componenta v)
            'soil_temperature_level_1'           # Temperatura solului la nivelul 1
]

def get_cdsapi_infos(dict_infos: dict) -> str:

    checked_infos = check_fetch_infos(dict_infos)

    if checked_infos is None:
        print("Something went wrong")
        return
    
    currrent_user = User.query.filter_by(id=dict_infos["user"]).first()
    current_land = Land.query.filter_by(id=dict_infos["land"]).first()
    now = datetime.now()
    file_name = currrent_user.username + "_" + current_land.name + "_" + now.strftime("%Y_%m_%d_%H_%M_%S")

    print("i am here")

    for key in checked_infos.keys():
        print(key, checked_infos[key])


    c.retrieve(
        "reanalysis-era5-single-levels",  # Dataset-ul pe care vrei să-l accesezi
        {
            "product_type": 'reanalysis',
            "variable": checked_infos["parameters"],
            "year": checked_infos["year"],
            "month": checked_infos["month"],
            "day": checked_infos["day"],
            "time": ["00:00", "04:00", "08:00",
                     "12:00", "16:00","17:00", "20:00"],
            'area': current_land.get_limits(),
            'format': 'netcdf'
        },
        f"{file_name}.nc")  # Numele fișierului în care vor fi salvate datele
    
    nc_to_json_convertor(file_name)
    process_json(input_json=f"{file_name}.json", output_json=f"{file_name}_final.json")
    
    with open(f"{file_name}_final.json", 'r') as file:
        infos = json.load(file)

    return infos

def check_fetch_infos(dict_infos: dict) -> dict | None:

    # dict_checked_infos = {"user" : "",
    #                     "land" : "",
    #                     "parameters" : [], 
    #                     "year": "2023", 
    #                     "month": ['01'],
    #                     "day" : ["01"],
    #                     "area" : ""
    #                     }
    
    must_have_keys = ["user", "land", "parameters", "year", "month", "day", "area"]

    for must_key in must_have_keys:
        if must_key not in dict_infos.keys():
            print(f"You are missing {must_key} for the dict")
            return None

    if dict_infos["user"] is None:
        print("User can not be NONE")
        return None

    if dict_infos["land"] is None:
        print("Land can not be NONE")
        return None
    
    for var in dict_infos["parameters"]:
        if var not in VALID_VARIABLES:
            print(f"{var} is not a valid variable")
            return None

    return dict_infos
