
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

from nlp.ollama_engine import query_ollama
from logic import Event, Weather

class AssistantApp(App):

    def build(self):
        self.root_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        self.scroll_view = ScrollView(size_hint=(1, 0.7))
        self.chat_label = Label(
            text="Welcome to the Assistant!\n",
            size_hint_y=None,
            markup=True,
            halign="left",
            valign="top",
        )
        self.chat_label.bind(texture_size=self.chat_label.setter('size'))
        self.scroll_view.add_widget(self.chat_label)
        self.root_layout.add_widget(self.scroll_view)

        # Input field for user query
        self.text_input = TextInput(
            hint_text="Type your question here...",
            size_hint=(1, 0.1),
            multiline=False,
        )
        self.text_input.bind(on_text_validate=self.handle_query)
        self.root_layout.add_widget(self.text_input)

        # Buttons
        button_layout = BoxLayout(size_hint=(1, 0.2), spacing=10)

        self.send_button = Button(text="Send", on_press=self.handle_query)
        button_layout.add_widget(self.send_button)

        # self.voice_button = Button(text="From Voice", on_press=self.handle_voice_query)
        # button_layout.add_widget(self.voice_button)


        self.root_layout.add_widget(button_layout)

        return self.root_layout

    def handle_query(self, instance=None):
        query = self.text_input.text.strip()
        if not query:
            self.update_chat("Assistant: Please enter a question.")
            return

        if "weather" in query.lower():
            city = query.split("weather in")[-1].strip()
            weather = Weather(city)
            if "tomorrow" in query.lower():
                weather = Weather(city, "tomorrow")
                response = weather.format_tomorrow_weather()
                response += weather.format_advice()
            else:
                response = weather.format_current_weather()
                response += weather.format_advice()
        elif "calendar" in query.lower() or "events" in query.lower():
            event = Event()
            if "inside" in query.lower():
                response = event.format_inside_events()
            elif "outside" in query.lower():
                response = event.format_outside_events()
            else:
                response = event.format_all_events()
        else:
            response = query_ollama(query)

        self.update_chat(f"You: {query}\nAssistant: {response}\n\n")
        self.text_input.text = ""

    # def handle_voice_query(self, instance=None):
    #     query = transcribe_audio()
    #     if not query:
    #         self.update_chat("Assistant: Could not understand the audio.")
    #         return
    #
    #     if "weather" in query.lower():
    #         city = query.split("weather in")[-1].strip()
    #         if "tomorrow" in query.lower():
    #             response = get_tomorrow_weather(city)
    #         else:
    #             response = get_current_weather(city)
    #     elif "calendar" in query.lower() or "events" in query.lower():
    #         response = get_upcoming_events(google_credentials)
    #
    #
    #     else:
    #         response = query_ollama(query)
    #
    #     self.update_chat(f"You: {query}\nAssistant: {response}")


    def update_chat(self, message):
        self.chat_label.text += f"{message}\n"
        self.scroll_view.scroll_y = 0  # Scroll to the bottom


if __name__ == "__main__":
    AssistantApp().run()
