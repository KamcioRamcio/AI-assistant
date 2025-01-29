from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

from api.data.functions import *
from api.logic.chat_logic import *

# Set a default window size
Window.size = (800, 600)

class MainScreen(BoxLayout):
    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = 15
        self.screen_manager = screen_manager
        self.start = StartingInfo()

        # Scrollable chat area
        self.scroll_view = ScrollView(size_hint=(1, 0.7))
        self.chat_label = Label(
            text="siemka",
            # text = f'[b][color=#4CAF50]{self.start.get_response()}[/color][/b]\n',
            size_hint_y=None,
            markup=True,
            halign="left",
            valign="top",
        )
        self.chat_label.bind(texture_size=self.chat_label.setter('size'))
        self.scroll_view.add_widget(self.chat_label)
        self.add_widget(self.scroll_view)

        # Input field for user query
        self.text_input = TextInput(
            hint_text="Type your question here...",
            size_hint=(1, 0.1),
            multiline=False,
            font_size=18,
            padding=(10, 10),
        )
        self.text_input.bind(on_text_validate=self.handle_query)
        self.add_widget(self.text_input)

        # Buttons
        button_layout = BoxLayout(size_hint=(1, 0.2), spacing=10)
        self.send_button = Button(
            text="Send",
            size_hint=(0.5, 1),
            background_color=(0.2, 0.6, 0.8, 1),
            font_size=16,
            on_press=self.handle_query,
        )
        button_layout.add_widget(self.send_button)

        self.new_window_button = Button(
            text="Open To-Do List",
            size_hint=(0.5, 1),
            background_color=(0.5, 0.7, 0.2, 1),
            font_size=16,
            on_press=self.open_new_window,
        )
        button_layout.add_widget(self.new_window_button)

        self.add_widget(button_layout)

    def handle_query(self, instance=None):
        query = self.text_input.text.strip()
        _handle_query = HandleQuery(query)
        if query in ["y", "Yes", "yes", "yeah"]:
            response = self.start._get_route_helper()
        else:
            response = _handle_query.get_response()

        self.update_chat(f"[color=#0000FF]You:[/color] {query}\n[color=#4CAF50]Assistant:[/color] {response}\n")
        self.text_input.text = ""

    def update_chat(self, message):
        self.chat_label.text += f"{message}\n"
        self.scroll_view.scroll_y = 1  # Scroll to the bottom

    def open_new_window(self, instance):
        self.screen_manager.current = 'new_window'


class NewWindowScreen(BoxLayout):
    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = 15
        self.screen_manager = screen_manager

        # Header
        self.label = Label(
            text="[b][color=#4CAF50]Welcome to the To-Do List[/color][/b]",
            font_size=20,
            size_hint=(1, 0.1),
            markup=True,
        )
        self.add_widget(self.label)

        # Scrollable To-Do list
        self.todo_scroll_view = ScrollView(size_hint=(1, 0.7))
        self.todo_label = Label(
            text="",
            size_hint_y=None,
            markup=True,
            halign="left",
            valign="top",
        )
        self.todo_label.bind(texture_size=self.todo_label.setter('size'))
        self.todo_scroll_view.add_widget(self.todo_label)
        self.add_widget(self.todo_scroll_view)

        # Buttons
        button_layout = BoxLayout(size_hint=(1, 0.2), spacing=10)
        self.back_button = Button(
            text="Go Back",
            background_color=(0.8, 0.3, 0.3, 1),
            font_size=16,
            on_press=self.go_back,
        )
        button_layout.add_widget(self.back_button)
        self.add_widget(button_layout)

        self.update_todo_list()

    def go_back(self, instance):
        self.screen_manager.current = 'main'

    def update_todo_list(self):
        self.todo_label.text = "[b]To-Do List[/b]\n"
        tasks = get_tasks()
        if not tasks:
            self.todo_label.text += "No tasks available."
        else:
            for task in tasks:
                status = "[color=#4CAF50]Completed[/color]" if task[4] else "[color=#FF9800]Pending[/color]"
                self.todo_label.text += f"• [b]{task[1]}[/b] - {status}\n   Deadline: {task[2]}   Location: {task[3]}\n\n"


class AssistantApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        # Main screen
        main_screen = Screen(name='main')
        main_screen.add_widget(MainScreen(self.screen_manager))
        self.screen_manager.add_widget(main_screen)

        # New window screen
        new_window_screen = Screen(name='new_window')
        new_window_screen.add_widget(NewWindowScreen(self.screen_manager))
        self.screen_manager.add_widget(new_window_screen)

        return self.screen_manager


if __name__ == "__main__":
    AssistantApp().run()
