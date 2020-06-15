from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window
from kivymd.uix.list import OneLineListItem
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

from player import Player
from match import Match

import json

#  Window.size = (350, 500)


class NavDrawer(MDNavigationDrawer):
    """Navigation Drawer controlled by the toolbar"""
    pass


class HomeScreen(MDScreen):
    """Homepage"""
    pass


class InputScreen(MDScreen):
    """The user gives all the information for the creation of a match"""
    pass


class SaveScreen(MDScreen):
    """Contains all the saved games on a list"""
    pass


class GameScreen(MDScreen):
    """Contains all the buttons that are used by the user during a match"""
    pass


class DataScreen(MDScreen):
    """Shows the data of a match"""
    pass


class TennisApp(MDApp):
    dialog = None

    def build(self):
        """Creates the app"""
        self.theme_cls.primary_palette = "Teal"
        return Builder.load_file("kv/main.kv")

    def change_screen(self, screen_name, direction='left'):
        """Changes the current screen using the ScreenManager"""
        self.root.ids.manager.transition = SlideTransition(direction=direction)
        self.root.ids.manager.current = screen_name

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
        self.check_server(match)
        self.win_condition()

    def saved_match_list(self):
        """Creates a list with all saved games"""
        self.root.ids.save_screen.ids.match_list.clear_widgets()  # To avoid duplication of widgets
        with open('data.json', 'r') as file:
            data = json.load(file)
        for match_info in data:  # For every match saved in the JSON file
            result = OneLineListItem(text='{} : {} vs {}'.format(
                match_info['match_name'], match_info['winner_name'],
                match_info['looser_name']))  # Add a OneListItem widget (UI)
            result.bind(on_release=lambda a: self.change_screen('data_screen'))
            result.bind(on_press=lambda a, i=match_info: self.show_data(i))
            self.root.ids.save_screen.ids.match_list.add_widget(result)

    def show_data(self, data):
        self.root.ids.data_screen.ids.player1_name.text = data['winner_name']
        self.root.ids.data_screen.ids.player2_name.text = data['looser_name']
        self.root.ids.data_screen.ids.set1_player1.text = str(data['winner_games'][0])
        self.root.ids.data_screen.ids.set2_player1.text = str(data['winner_games'][1])
        self.root.ids.data_screen.ids.set3_player1.text = str(data['winner_games'][2])
        self.root.ids.data_screen.ids.set1_player2.text = str(data['looser_games'][0])
        self.root.ids.data_screen.ids.set2_player2.text = str(data['looser_games'][1])
        self.root.ids.data_screen.ids.set3_player2.text = str(data['looser_games'][2])

    def check_text(self):
        """Checks if a textfield is empty"""
        condition = True
        for text in self.root.ids.input_screen.ids.confirmation_button.checking_text:
            if text == '' or text == ' ':
                condition = False
        if condition:
            self.create_match()
            self.show_dialog_server()
            self.change_screen('game_screen')
        else:
            self.root.ids.input_screen.ids.error_message.text = 'Error : A required field is missing!'

    def modify_fault_button(self):
        """Modify the button (Fault / Double Fault)"""
        if self.root.ids.game_screen.ids.fault.text == "Fault":
            self.root.ids.game_screen.ids.fault.text = 'Double Fault'
        elif self.root.ids.game_screen.ids.fault.text == 'Double Fault':
            self.root.ids.game_screen.ids.fault.text = 'Fault'
            self.update_scoreboard(self.root.ids.game_screen.match.receiver, self.root.ids.game_screen.match.server, self.root.ids.game_screen.match)

    def show_dialog_server(self):
        """Shows a dialog box to ask which player serves first"""
        if not self.dialog:
            self.dialog = MDDialog(title='Who serves first?', size_hint=(0.7, 1), buttons=[
                MDFlatButton(text=self.root.ids.input_screen.ids.entry1.text, text_color=self.theme_cls.primary_color,
                             on_release=lambda x: self.server(self.root.ids.game_screen.player1, self.root.ids.game_screen.player2)),
                MDFlatButton(text=self.root.ids.input_screen.ids.entry2.text, text_color=self.theme_cls.primary_color,
                             on_release=lambda x: self.server(self.root.ids.game_screen.player2, self.root.ids.game_screen.player1))])
        self.dialog.open()

    def server(self, server, receiver):
        """Sets which player serves or receives"""
        self.root.ids.game_screen.match.server = server
        self.root.ids.game_screen.match.receiver = receiver
        self.check_server(self.root.ids.game_screen.match)
        self.dialog.dismiss()
        print(self.root.ids.game_screen.match.server.get_name())

    def check_server(self, match):
        """Hide or show the tennis-ball icon depending on which player serves"""
        if match.server.get_name() == match.player1.get_name():
            self.root.ids.game_screen.ids.server2.opacity = 0
            self.root.ids.game_screen.ids.server1.opacity = 1
        else:
            self.root.ids.game_screen.ids.server2.opacity = 1
            self.root.ids.game_screen.ids.server1.opacity = 0

    def set_winner(self, winner, looser):
        """Sets which player wins the point"""
        self.root.ids.game_screen.winner = winner
        self.root.ids.game_screen.looser = looser


if __name__ == "__main__":
    TennisApp().run()
