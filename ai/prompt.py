import datetime

def generate_weather_prompt_v2(weather_data):
    """
    Generates a prompt for AI based on weather data from a temporally structured JSON.
    
    weather_data: dict
        Dictionary with weather data, structured with keys:
        - "time": List of timestamps.
        - other keys: List of values corresponding to each timestamp.
        
    Returns:
        str: Generated prompt for AI.
    """
    
    # Convert timestamps to human-readable format
    times = [datetime.datetime.utcfromtimestamp(t/1e9).strftime('%Y-%m-%d %H:%M:%S') for t in weather_data["time"]]
    
    # Assume all lists have the same length
    n = len(weather_data["time"])
    
    prompts = []
    
    for i in range(n):
        details = []
        
        if "t2m" in weather_data:
            temp_celsius = weather_data["t2m"][i] - 273.15
            details.append(f"the temperature at 2 meters was {temp_celsius:.2f}°C")
        
        if "swvl1" in weather_data:
            details.append(f"the soil moisture in the first layer was {weather_data['swvl1'][i]:.2f}")
        
        if "d2m" in weather_data:
            dewpoint_celsius = weather_data["d2m"][i] - 273.15
            details.append(f"the dew point temperature at 2 meters was {dewpoint_celsius:.2f}°C")
        
        if "tp" in weather_data:
            details.append(f"the total precipitation was {weather_data['tp'][i]:.2f} mm")
        
        if "ssrd" in weather_data:
            details.append(f"the surface solar radiation was {weather_data['ssrd'][i]:.2f} W/m²")
        
        if "u10" in weather_data:
            details.append(f"the wind speed at 10 meters (u-component) was {weather_data['u10'][i]:.2f} m/s")
        
        if "stl1" in weather_data:
            temp_soil_layer1_celsius = weather_data["stl1"][i] - 273.15
            details.append(f"the soil temperature in the first layer was {temp_soil_layer1_celsius:.2f}°C")
        
        if "v10" in weather_data:
            details.append(f"the wind speed at 10 meters (v-component) was {weather_data['v10'][i]:.2f} m/s")
        
        # Create the prompt for this timestamp
        if details:
            details_str = "; ".join(details)
            prompt = f"Based on the weather data for {times[i]}, {details_str}. What advice do you have for crop management under these conditions?"
            prompts.append(prompt)
    
    # Join all prompts into one paragraph with a maximum of 20 sentences
    combined_prompt = " ".join(prompts)
    sentences = combined_prompt.split('. ')
    return '. '.join(sentences[:20]) + '.'
