from ..api.calendar_api import get_upcoming_events
from ..utils.calendar_helper import get_credentials
from ..api.public_trasport_api import get_route_info
from ..services.todo_service import TodoService  # Relative import
from ..api.weather_api import get_current_weather, get_tomorrow_weather
from datetime import datetime, timedelta
from enum import Enum
import requests



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

    def get_outside_events(self):
        return self.outside_events

    def get_inside_events(self):
        return self.inside_events

    def get_route_info(self, location, start_time):
        print(start_time)
        print(location)
        try:
            route = get_route_info(location, start_time+"Z", self.google_credentials)
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
                location = event.get("location")
                if location == "None":
                    location = "Home"
                start_time = datetime.strptime(event["start"].split("T")[1], "%H:%M:%S").strftime("%H:%M")
                end_time = datetime.strptime(event["end"].split("T")[1], "%H:%M:%S").strftime("%H:%M")
                event_lines.append(f"\nEvent: {summary} at {location} from {start_time} to {end_time}")
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

    def _print_weather_advice(self):
        return "\n".join(self.get_weather_advice())

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
            f"Advice: {self._print_weather_advice()}"
        )

    def format_current_weather(self):
        return self.format_weather(self.current_weather, "current")

    def format_tomorrow_weather(self):
        return self.format_weather(self.tomorrow_weather, "tomorrow")

    def format_advice(self):
        return "\n".join(self.get_weather_advice())

class TodoList:
    def __init__(self, conversation=None, conversation_id=None):
        self.conversation = conversation
        self.conversation_id = conversation_id
        self.task_data = {
            "name": None,
            "location": None,
            "deadline": None,
        }

        self.todo_list_id = None

        if self.conversation.task_state:
            self._load_state_task()

        if self.conversation.todo_list_id:
            self._load_state_todo_list()

    def _load_state_task(self):
        self.task_data["name"] = self.conversation.task_name
        self.task_data["deadline"] = self.conversation.task_deadline
        self.task_data["location"] = self.conversation.task_location

    def _load_state_todo_list(self):
        self.todo_list_id = self.conversation.todo_list_id

    def chat_add_task(self, user_input):
        if not self.conversation.task_state:
            self.conversation.task_state = 'NAME'
            self._save_state()
            return "What is the name of the task?"

        if self.conversation.task_state == 'NAME':
            self.conversation.task_name = user_input
            self.conversation.task_state = 'DEADLINE'
            self._save_state()
            return "When is the deadline (YYYY-MM-DD)?"

        if self.conversation.task_state == 'DEADLINE':
            try:
                datetime.strptime(user_input, "%Y-%m-%d")
                self.conversation.task_deadline = user_input
                self.conversation.task_state = 'LOCATION'
                self._save_state()
                return "Where is the task location?"
            except ValueError:
                return "Invalid date format. Please use YYYY-MM-DD"

        if self.conversation.task_state == 'LOCATION':
            self.conversation.task_location = user_input
            result = self._save_task()
            self._reset()
            return result

        return "An error occurred. Please start over."

    def _save_state(self):
        self.conversation.save()

    def _save_task(self):

        task_data = {
            'name': self.conversation.task_name,
            'location': self.conversation.task_location,
            'deadline': self.conversation.task_deadline
        }

        success, result = TodoService.create_task(
            conversation=self.conversation,
            task_data=task_data
        )

        return "Task added successfully!" if success else f"Error: {result}"

    def _reset(self):
        self.conversation.task_state = None
        self.conversation.task_name = None
        self.conversation.task_deadline = None
        self.conversation.task_location = None
        self.conversation.save()

    def get_todo_list(self, user_input):
        # Initial state - prompt for list selection
        if not self.conversation.todo_list_state:
            todo_lists = TodoService.get_user_todo_lists(self.conversation.user)

            if not todo_lists:
                return "You have no todo lists! Create one first."

            # Format lists as numbered options
            list_options = []
            for idx, lst in enumerate(todo_lists, 1):
                list_options.append(f"{idx}. {lst.get('name', 'Unnamed List')} (ID: {lst['id']})")

            prompt = (
                    "Which todo list would you like to view?\n" +
                    "\n".join(list_options) +
                    "\n\nPlease enter either the list number or ID:"
            )

            self.conversation.todo_list_state = 'AWAITING_ID'
            self._save_state()
            return prompt

        # Handle ID input state
        if self.conversation.todo_list_state == 'AWAITING_ID':
            todo_lists = TodoService.get_user_todo_lists(self.conversation.user)

            try:
                # Try to handle numeric input (list index)
                if user_input.isdigit():
                    index = int(user_input) - 1
                    if 0 <= index < len(todo_lists):
                        self.todo_list_id = todo_lists[index]['id']
                    else:
                        raise ValueError("Invalid list number")
                # Handle ID input
                else:
                    # Verify ID exists in user's lists
                    if any(str(lst['id']) == user_input for lst in todo_lists):
                        self.todo_list_id = user_input
                    else:
                        raise ValueError("Invalid list ID")
            except ValueError as e:
                # Maintain state to retry
                return f"Invalid input: {e}. Please try again."

            # Clear state after successful selection
            self.conversation.todo_list_state = None
            self._save_state()

            # Get and return tasks
            tasks_response = TodoService.get_user_tasks(
                user=self.conversation.user,
                todo_list_id=self.todo_list_id
            )
            return tasks_response

        return "An error occurred in todo list selection. Please start over."






# test = Todo()
# test.get_tasks()