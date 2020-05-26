from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.list import OneLineListItem

from Tennis_app.player import Player
from Tennis_app.match import Match

import json

Window.size = 350, 500


class HomeScreen(Screen):
    pass


class InputScreen(Screen):
    pass


class SaveScreen(Screen):
    pass


class ListItem(OneLineListItem):
    pass


class CreateButton(MDRectangleFlatButton):

    def on_press(self):
        """Create a match when button pressed"""
        player1 = Player(self.player1_name)
        player2 = Player(self.player2_name)
        GameScreen.player1 = player1
        GameScreen.player2 = player2
        GameScreen.match = Match(player1, player2, self.match_name)


class GameScreen(Screen):
    pass


class DataScreen(Screen):
    pass


class TennisApp(MDApp):

    def build(self):
        """Creates the app"""
        self.theme_cls.primary_palette = "Teal"
        return Builder.load_file("main.kv")

    def get_json(self):

        """Gets the data from the JSON file"""

        with open('data.json', 'r') as file:
            return json.load(file)

    def on_start(self):

        data = self.get_json()

        for dict in data:  # For every match saved in the JSON file
            result = ListItem(text='{} : {} vs {}'.format(
                    dict['match_name'], dict['winner_name'], dict['looser_name']))  # Add a OneListItem widget (UI)
            result.bind(on_press=lambda a: self.change_screen('data_screen'))
            winner_points = dict['winner_points']
            looser_points = dict['looser_points']
            result.bind(on_press= lambda a: self.print_value(dict['winner_name'], dict['looser_name'], str(winner_points[0]), str(looser_points[0])))
            self.root.ids.save_screen.ids.match_list.add_widget(result)

    def change_screen(self, screen_name):
        """Change the current screen using the ScreenManager"""
        self.root.current = screen_name

    def print_value(self, player1, player2, points1, points2):
        self.root.ids.data_screen.ids.player1.text = player1
        self.root.ids.data_screen.ids.player2.text = player2
        self.root.ids.data_screen.ids.points1.text = points1
        self.root.ids.data_screen.ids.points2.text = points2


if __name__ == "__main__":
    TennisApp().run()
