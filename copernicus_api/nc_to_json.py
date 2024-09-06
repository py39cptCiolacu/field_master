from typing import Tuple, Union, List
import xarray as xr
import json
import os
import shutil
import numpy as np

def move_results(file: str, username: str, land_name: str) -> None:
    
    src_path = os.path.join(os.getcwd(), file)
    dest_dir = os.path.join(os.getcwd(), "..", "results", username, land_name)

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    dest_path = os.path.join(dest_dir, file)

    try:
        shutil.move(src_path, dest_path)
        print("File moved")
    except FileNotFoundError:
        print("File not found")
    except Exception as e:
        print(str(e))

def nc_to_json_convertor(nc_file_name: str) -> None:

    ds = xr.open_dataset(f"{nc_file_name}.nc")

    data_dict = {}

    for var_name in ds.variables:
        data_dict[var_name] = ds[var_name].values.tolist()

    data_dict['attributes'] = {attr: ds.attrs[attr] for attr in ds.attrs}

    for key in data_dict.keys():
        print(key)

    with open(f'{nc_file_name}.json', 'w') as json_file:
        json.dump(data_dict, json_file, indent=4)

    # os.remove(f"{nc_file_name}.nc")

    print("Conversia a fost realizată cu succes!")


def process_json(input_json: str, output_json) -> None:
    with open(input_json, 'r') as file:
        data = json.load(file)
    
    data.pop("longitude", None)
    data.pop("latitude", None)
    data.pop("attributes", None)
    
    if "time" not in data:
        raise KeyError("'time' key not found in the data")
    
    result = calculate_mean(data)
    
    with open(output_json, 'w') as file:
        json.dump(result, file, indent=4)

    # os.remove(f"{input_json}.json")


def calculate_mean(data: dict) -> dict:
    """
    Every .nc file could be considered a list of lists of lists - something like this:

    [[[12, 67, 12], [34, 1, 65]], [[55, 12], [56, 33]]]. This function take as an input this kind triple nested lists and return a list of 
    """

    result = {"time": data["time"]}

    for key, value in data.items():
        
        if key == "time":
            continue

        if not all(isinstance(sublist, list) for sublist in value):
            raise ValueError(f"Data for key {key} is not a list of lists of lists")
        
        current_means = []
        for sub_value in value:
            total, count = calculate_mean_in_list(sub_value)
            current_means.append(total/count)

        result[key] = current_means 
        
    return result


def calculate_mean_in_list(value_list: list) -> Tuple[float, int]:
    total = 0
    count = 0

    for element in value_list:
        if isinstance(element, list):

            sub_total, sub_count = calculate_mean_in_list(element)
            total += sub_total
            count += sub_count

        elif isinstance(element, (int, float, str)):
            numeric_element = float(element)
            total += numeric_element
            count += 1

    return total, count