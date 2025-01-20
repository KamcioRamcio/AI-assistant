from utils.word_correction import correct_word
from enum import Enum
from nlp.ollama_engine import query_ollama
from logic import Event, Weather
import re

class WordDict(Enum):
    WEATHER = ["weather", "forecast"]
    CALENDAR = ["calendar", "events"]
    ROUTE = ["route", "directions", "way", "navigate"]
    TOMORROW = ["tomorrow", "next"]
    TODAY = ["today", "current"]
    EVENT = ["event", "reminder", "note", "list"]
    INSIDE = ["inside", "home"]
    OUTSIDE = ["outside", "school", "other"]
    CITIES = ["poznan", "szczecin", "wroclaw", "gdansk", "krakow"]



class HandleQuery:
    def __init__(self, query=None):
        self.query = query.lower() if query else ""
        self.clear_query()
        self.response = self.handle_query()

    def clear_query(self):
        words = self.query.split()
        corrected_words = [correct_word(word) for word in words]
        self.query = " ".join(corrected_words)

    def handle_query(self):
        if not self.query.strip():
            return "Please enter a question.\n"

        match = re.search(r"weather(?:\s+in\s+(\w+))?", self.query)
        if match:
            city = match.group(1)
            if city and city in WordDict.CITIES.value:
                return Weather(city).format_current_weather()
            else:
                return "Please specify a valid city for the weather information."

        if any(word in self.query for word in WordDict.CALENDAR.value):
            if any(word in self.query for word in WordDict.INSIDE.value):
                return Event().format_inside_events()
            elif any(word in self.query for word in WordDict.OUTSIDE.value):
                return Event().format_outside_events()
            else:
                return Event().format_all_events()

        if any(word in self.query for word in WordDict.ROUTE.value):
            location = self.extract_location()
            if location:
                # TODO
                #   add autocomplete for location using Google Maps API
                #   format destination to allow api to accept it
                return Event().get_route_info("Pleszewska 1, 61-136, Poznan, Poland", )
            else:
                return "Please specify a location for route directions."

        return query_ollama(self.query)

    def extract_location(self):
        match = re.search(r"(to|in)\s+(\w+)", self.query)
        return match.group(2) if match else None

    def get_response(self):
        return self.response

class HandleVoiceQuery:
    pass

class StartingInfo:
    def __init__(self):
        self.response = "Hi Kamcio! My name is Yuki and i will help you with everything you want :>>\n\n"
        self.weather = Weather("poznan").format_current_weather()
        self._outside_events = Event()._get_outside_events()
        self._outside_events = Event().format_outside_events()
        self.inside_events = Event().format_inside_events()

    def get_route(self):
        for event in self._outside_events:
            return Event().get_route_info(event["location"])

    def get_response(self):
        self.response += ("Today's weather in Poznan is \n" + self.weather + "\n" +
                          "Your today inside events are listed here\n" + self.inside_events + "\n\n"
                          + "Your today outside events are listed here\n" + self._outside_events + "\n\n" +
                            "Do you want to know the route to the event?"
                          )
        return self.response

# test = HandleQuery("hello can you show me route to Sz")
# print(test.get_response())

test = StartingInfo()
print(test.get_response())

# TODO
#   Add date of the event in printing routes,
#   Add feels-like in weather information