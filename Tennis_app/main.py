from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.core.window import Window
from kivymd.uix.list import OneLineListItem

from Tennis_app.player import Player
from Tennis_app.match import Match

import json


Window.size = (350, 500)


class HomeScreen(Screen):
    """Homepage"""
    pass


class InputScreen(Screen):
    """The user gives all the information for the creation of a match"""
    pass


class SaveScreen(Screen):
    """Contains all the saved games on a list"""
    pass


class GameScreen(Screen):
    """Contains all the buttons that are used by the user during a match"""
    pass


class DataScreen(Screen):
    """Shows the data of a match"""
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

    def change_screen(self, screen_name, direction='left'):
        """Changes the current screen using the ScreenManager"""
        self.root.transition = SlideTransition(direction=direction)
        self.root.current = screen_name

    def print_value(self, player1, player2, points1, points2):
        self.root.ids.data_screen.ids.player1.text = player1
        self.root.ids.data_screen.ids.player2.text = player2
        self.root.ids.data_screen.ids.points1.text = points1
        self.root.ids.data_screen.ids.points2.text = points2

    def win_condition(self):
        if self.root.ids.game_screen.ids.sets_label1.text == '2' or self.root.ids.game_screen.ids.sets_label2.text == '2':
            self.change_screen('home_screen', 'right')

    def create_match(self):
        """Creates a match when button pressed"""
        player1 = Player(self.root.ids.input_screen.ids.entry1.text)
        player2 = Player(self.root.ids.input_screen.ids.entry2.text)
        GameScreen.player1 = player1
        GameScreen.player2 = player2
        GameScreen.match = Match(player1, player2, self.root.ids.input_screen.ids.entry3.text)

    def update_scoreboard(self, winner, opponent, match):
        """Updates the scoreboard each time a player wons a point"""
        match.points_win(winner, opponent)
        self.root.ids.game_screen.ids.points_label1.text = match.player1.get_points_amount()
        self.root.ids.game_screen.ids.points_label2.text = match.player2.get_points_amount()
        self.root.ids.game_screen.ids.games_label1.text = match.player1.get_games_amount()
        self.root.ids.game_screen.ids.games_label2.text = match.player2.get_games_amount()
        self.root.ids.game_screen.ids.sets_label1.text = match.player1.get_sets_amount()
        self.root.ids.game_screen.ids.sets_label2.text = match.player2.get_sets_amount()
        self.win_condition()

    def saved_match_list(self):
        """Creates a list with all saved games"""
        self.root.ids.save_screen.ids.match_list.clear_widgets()
        data = self.get_json()

        for dict in data:  # For every match saved in the JSON file
            result = OneLineListItem(text='{} : {} vs {}'.format(
                dict['match_name'], dict['winner_name'], dict['looser_name']))  # Add a OneListItem widget (UI)
            result.bind(on_press=lambda a: self.change_screen('data_screen'))
            winner_points = dict['winner_points']
            looser_points = dict['looser_points']
            result.bind(
                on_press=lambda a: self.print_value(dict['winner_name'], dict['looser_name'], str(winner_points[0]),
                                                    str(looser_points[0])))
            self.root.ids.save_screen.ids.match_list.add_widget(result, 1)


if __name__ == "__main__":
    TennisApp().run()
