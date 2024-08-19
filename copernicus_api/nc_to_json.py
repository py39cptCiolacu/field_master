import xarray as xr
import json
import os
import numpy as np

def nc_to_json_convertor(nc_file_name: str) -> None:

    # Deschide fișierul NetCDF
    ds = xr.open_dataset(f"{nc_file_name}.nc")

    # Crearea unui dicționar pentru a stoca datele
    data_dict = {}

    # Iterarea prin toate variabilele din dataset și adăugarea lor în dicționar
    for var_name in ds.variables:
        data_dict[var_name] = ds[var_name].values.tolist()

    # Adăugarea atributelor datasetului (metadate)
    data_dict['attributes'] = {attr: ds.attrs[attr] for attr in ds.attrs}

    for key in data_dict.keys():
        print(key)

    # Scrierea datelor în format JSON
    with open(f'{nc_file_name}.json', 'w') as json_file:
        json.dump(data_dict, json_file, indent=4)

    # os.remove(f"{nc_file_name}.nc")

    print("Conversia a fost realizată cu succes!")


def process_json(input_json, output_json):
    # Citim datele din fișierul JSON de intrare
    with open(input_json, 'r') as file:
        data = json.load(file)
    
    # Eliminăm cheile 'longitude' și 'latitude'
    data.pop("longitude", None)
    data.pop("latitude", None)
    data.pop("attributes", None)
    
    # Verificăm dacă 'time' există
    if "time" not in data:
        raise KeyError("'time' key not found in the data")
    
    # Lista de chei pentru care se calculează media
    result = {"time": data["time"]}
    
    # Calculăm media pentru fiecare sub-sub-listă din celelalte chei
    for key, value in data.items():
        if key != "time":
            if not all(isinstance(sublist, list) for sublist in value):
                raise ValueError(f"Data for key '{key}' is not a list of lists of lists")

            means = []
            for sublist in value:
                if not all(isinstance(inner_list, list) for inner_list in sublist):
                    raise ValueError(f"Data for key '{key}' contains elements that are not lists of lists")
                
                # Calculăm media pentru fiecare sub-sub-listă
                sublist_means = []
                for inner_list in sublist:
                    try:
                        # Convertim elementele la float
                        numeric_inner_list = [float(item) for item in inner_list]
                        # Calculăm media pentru sub-sub-listă
                        sublist_means.append(np.mean(numeric_inner_list))
                    except ValueError:
                        print(f"Non-numeric value found in key '{key}': {inner_list}")
                        print(f"Original data: {value}")
                        raise ValueError(f"Element in key '{key}' cannot be converted to float.")
                
                means.append(sublist_means)
            
            result[key] = means
    
    # Calculăm media pentru fiecare sub-listă din rezultatul final
    final_result = {"time": result["time"]}
    for key, value in result.items():
        if key != "time":
            # Verificăm structura listei
            if not all(isinstance(sublist, list) for sublist in value):
                raise ValueError(f"Data for key '{key}' is not a list of lists")
            
            # Calculăm media pentru fiecare sub-listă
            final_means = []
            for sublist in value:
                try:
                    # Convertim elementele la float
                    numeric_sublist = [float(item) for item in sublist]
                    # Calculăm media pentru sub-listă
                    final_means.append(np.mean(numeric_sublist))
                except ValueError:
                    print(f"Non-numeric value found in key '{key}': {sublist}")
                    print(f"Original data: {result[key]}")
                    raise ValueError(f"Element in key '{key}' cannot be converted to float.")
            
            final_result[key] = final_means
    
    # Salvăm rezultatul în fișierul JSON de ieșire
    with open(output_json, 'w') as file:
        json.dump(final_result, file, indent=4)

    # os.remove(f"{input_json}.json")





