from api.calendar_api import get_upcoming_events
from utils.calendar_helper import get_credentials
from api.public_trasport_api import get_route_info
from api.weather_api import get_current_weather, get_tomorrow_weather
from datetime import datetime, timedelta
from enum import Enum



class Event:
    def __init__(self, ):
        self.google_credentials = get_credentials()
        self.events = self._fetch_events()
        self.routes = []
        self.outside_events = []
        self.inside_events = []
        self._classify_events()
        self.start_time = (datetime.now()+timedelta(hours=+1)).isoformat().split('.')[0]+"Z"

    def _fetch_events(self):
        events = get_upcoming_events(self.google_credentials)
        return self._remove_duplicate_events(events)

    def _remove_duplicate_events(self, events):
        unique_events = []
        seen_summaries = set()

        for event in events:
            if event["summary"] not in seen_summaries:
                unique_events.append(event)
                seen_summaries.add(event["summary"])
        return unique_events

    def _classify_events(self):
        for event in self.events:
            if event.get("location") and event["location"].lower() != "none":
                self.outside_events.append(event)
            else:
                self.inside_events.append(event)

    def _get_outside_events(self):
        return self.outside_events

    def get_route_info(self, location):
        try:
            route = get_route_info(location, self.start_time, self.google_credentials)
            self.routes.append(route)
            print(self.start_time)
            return route
        except Exception as e:
            print(f"Failed to get route info: {e}")
            return None

    def format_inside_events(self):
        return self._format_events(self.inside_events)

    def format_outside_events(self):
        return self._format_events(self.outside_events)

    def format_all_events(self):
        return self._format_events(self.outside_events + self.inside_events)

    def _format_events(self, events):
        event_lines = []
        for event in events:
            try:
                summary = event["summary"]
                location = event.get("location", "No location")
                start_time = datetime.strptime(event["start"].split("T")[1], "%H:%M:%S").strftime("%H:%M")
                end_time = datetime.strptime(event["end"].split("T")[1], "%H:%M:%S").strftime("%H:%M")
                event_lines.append(f"Event: {summary} at {location} from {start_time} to {end_time}")
            except KeyError as e:
                print(f"Missing data in event: {e}")
        return "\n".join(event_lines)

class WeatherCondition(Enum):
    RAIN = "rain"
    THUNDERSTORM = "thunderstorm"
    DRIZZLE = "drizzle"
    SHOWERS = "showers"
    SNOW = "snow"
    SLEET = "sleet"
    HAIL = "hail"

class Weather:
    def __init__(self, city, day=None):
        self.city = city.capitalize()
        self.current_weather = get_current_weather(self.city)
        self.tomorrow_weather = get_tomorrow_weather(self.city)
        self.advices = []
        self.thresholds = {
            "cold_temperature": 10,  # Degrees Celsius
            "high_wind_speed": 20,   # km/h
        }
        self.day = day

    def get_weather_advice(self):
        self.advices = []

        if not self.day:
            self._check_weather_conditions(self.current_weather, "today")

        else:
            self._check_weather_conditions(self.tomorrow_weather, "tomorrow")

        return self.advices

    def _check_weather_conditions(self, weather, day):
        temp_threshold = self.thresholds["cold_temperature"]
        wind_threshold = self.thresholds["high_wind_speed"]

        # Temperature Advice
        if weather["temperature"] < temp_threshold:
            self.advices.append(f"It's going to be cold {day}, wear a jacket!")

        # Rain Advice
        if weather["rain_probability"] > 0 or self._is_condition(weather["condition"], WeatherCondition.RAIN):
            self.advices.append(f"It might rain {day}, don't forget your umbrella!")

        # Snow Advice
        if self._is_condition(weather["condition"], WeatherCondition.SNOW):
            self.advices.append(f"It's going to snow {day}, be careful!")

        # Wind Advice
        if weather["wind_speed"] > wind_threshold:
            self.advices.append(f"It's going to be windy {day}, be careful!")

    @staticmethod
    def _is_condition(condition, weather_type):
        return weather_type.value in condition.lower()

    def format_weather(self, weather, day):
        return (
            f"{day.capitalize()}'s weather in {weather['location']}:\n"
            f"Temperature: {weather['temperature']}°C\n"
            f"Condition: {weather['condition']}\n"
            f"Rain probability: {weather['rain_probability']}mm\n"
            f"Wind speed: {weather['wind_speed']}km/h\n"
        )

    def format_current_weather(self):
        return self.format_weather(self.current_weather, "current")

    def format_tomorrow_weather(self):
        return self.format_weather(self.tomorrow_weather, "tomorrow")

    def format_advice(self):
        return "\n".join(self.get_weather_advice())

# Example Usage
if __name__ == "__main__":
    weather = Weather("Szczecin")
    print(weather.format_current_weather())
    print(weather.format_tomorrow_weather())
    print("Advice:")
    print(weather.format_advice())

