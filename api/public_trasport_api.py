from google.oauth2.credentials import Credentials
import requests
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()


def get_route_info( destination, arrival_time, credentials: Credentials):
    origin = "Unii Lubelskiej 6, 61-249, Poznań, Poland"
    url = "https://routes.googleapis.com/directions/v2:computeRoutes"

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": os.getenv("GOOGLE_API"),
        "X-Goog-FieldMask": "routes.legs.steps.transitDetails",
    }

    payload = {
        "origin": {"address": origin},
        "destination": {"address": destination},
        "travelMode": "TRANSIT",
        "arrivalTime": f"{arrival_time}",
        "computeAlternativeRoutes": True,
    }

    try:
        # Make the request to the Google API
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        data = response.json()

        if "routes" in data:
            routes = data["routes"]
            for route_idx, route in enumerate(routes):
                if route_idx >= 2:
                    break
                print(f"Route {route_idx + 1}:")
                for leg in route["legs"]:
                    for step in leg["steps"]:
                        if "transitDetails" in step:
                            transit_details = step["transitDetails"]
                            line = transit_details["transitLine"]["nameShort"]
                            departure_stop = transit_details["stopDetails"]["departureStop"]["name"]
                            departure_time_str = transit_details["stopDetails"]["departureTime"].split("T").pop(1).strip("Z")
                            departure_time = datetime.strptime(departure_time_str, "%H:%M:%S").strftime("%H:%M")
                            arrival_time_str = transit_details["stopDetails"]["arrivalTime"].split("T").pop(1).strip("Z")
                            arrival_time = datetime.strptime(arrival_time_str, "%H:%M:%S").strftime("%H:%M")
                            arrival_stop = transit_details["stopDetails"]["arrivalStop"]["name"]
                            vehicle = transit_details["transitLine"]["vehicle"]["name"]["text"].lower()
                            result = f"  Take {vehicle} nr {line} from {departure_stop} to {arrival_stop}, departing at {departure_time}, arriving at {arrival_time}"
                            return result
        else:
            print("No routes found.")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")