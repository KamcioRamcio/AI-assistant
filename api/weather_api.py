import requests
from dotenv import load_dotenv
import os

load_dotenv()
base_url = "http://api.weatherapi.com/v1/"


def get_current_weather(city):
    params = {
        "key": os.getenv("WEATHER_API"),
        "q": city
    }
    try:
        response = requests.get(f'{base_url}current.json', params=params)
        response.raise_for_status()
        data = response.json()

        current_weather_dict = {
            "location": data["location"]["name"],
            "temperature": data["current"]["temp_c"],
            "condition": data["current"]["condition"]["text"],
            "rain_probability": data["current"]["precip_mm"],
            "wind_speed": data["current"]["wind_kph"]
        }

        return current_weather_dict
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"


def get_tomorrow_weather(city):
    params = {
        "key": os.getenv("WEATHER_API"),
        "q": city,
        "days": 2
    }
    try:
        response = requests.get(f'{base_url}forecast.json', params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        tomorrow = data["forecast"]["forecastday"][1]

        tomorrow_weather_dict = {
            "location": data["location"]["name"],
            "temperature": tomorrow["day"]["avgtemp_c"],
            "condition": tomorrow["day"]["condition"]["text"],
            "rain_probability": tomorrow["day"]["daily_chance_of_rain"],
            "wind_speed": tomorrow["day"]["maxwind_kph"]
        }

        return tomorrow_weather_dict


    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"


