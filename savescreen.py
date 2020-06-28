import json
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineListItem


class SaveScreen(MDScreen):
    """Contains all the saved games on a list"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()

    def saved_match_list(self):
        """Creates a list with all saved games"""
        self.ids.match_list.clear_widgets()  # To avoid duplication of widgets
        with open('data.json', 'r') as file:
            data = json.load(file)
        for match_info in data:  # For every match saved in the JSON file
            result = OneLineListItem(text='{} : {} vs {}'.format(
                match_info['match_name'], match_info['winner_name'],
                match_info['looser_name']))  # Add a OneListItem widget (UI)
            result.bind(on_release=lambda a: self.app.change_screen('data_screen'))
            result.bind(on_press=lambda a, i=match_info: self.app.root.ids.data_screen.show_data(i))
            self.ids.match_list.add_widget(result)