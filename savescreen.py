import json
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

from player import Player
from match import Match


class SaveScreen(MDScreen):
    """Contains all the saved games on a list"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.save = None
        self.empty = True  # Checks whether there are saves or not
        self.picked_game_data = None
        self.full_list = None

    def saved_match_list(self):
        """Creates a list with all saved games"""
        self.ids.match_list.clear_widgets()  # To avoid duplication of widgets
        with open('data.json', 'r') as file:
            data = json.load(file)
        for match_info in data:  # For every match saved in the JSON file
            self.empty = False
            result = OneLineListItem(text='{} : {} vs {}'.format(
                match_info['match_name'], match_info['player1_name'],
                match_info['player2_name']))  # Add a OneListItem widget (UI)
            result.bind(on_press=lambda a, i=match_info: self.show_dialog_saves(i, data))
            # Gets the information of the match which is chosen by the user
            self.ids.match_list.add_widget(result)
        if self.empty:  # Writes a message if there is not match saved
            self.ids.empty_text.text = 'There are no saves! Create a game!'
        else:
            self.ids.empty_text.text = ''

    def show_dialog_saves(self, data, full_list):
        """Gives the choice to the user :
        Whether he continues the game, or he checks the data of the game"""
        if not self.save:
            self.save = MDDialog(title='Do you want to continue the match or check the data?',
                                 size_hint=(0.7, 1),
                                 buttons=[
                                    MDFlatButton(text='Continue game', text_color=self.app.theme_cls.primary_color,
                                                 on_release=lambda x: self.continue_game(data, full_list)),
                                    MDFlatButton(text='Check data', text_color=self.app.theme_cls.primary_color,
                                                 on_release=lambda x: self.data_choice(data))])
        self.save.open()

    def data_choice(self, data):
        """Goes to the data_screen depending on the user's choice"""
        self.app.root.ids.data_screen.show_data(data)
        self.app.change_screen('data_screen')
        self.save.dismiss()
        self.save = None
    
    def continue_game(self, data, full_list):
        self.picked_game_data = data  # To get the information from another class
        self.full_list = full_list
        """Continues the game"""
        player1 = Player(data['player1_name'], data['player1_points'], data['player1_games'], data['player1_sets'],
                         data['player1_total_points'], data['player1_total_games'])
        player2 = Player(data['player2_name'], data['player2_points'], data['player2_games'], data['player2_sets'],
                         data['player2_total_points'], data['player2_total_games'])
        self.app.root.ids.game_screen.player1 = player1
        self.app.root.ids.game_screen.player2 = player2

        if data['server'] == player1.name:
            self.app.root.ids.game_screen.match = Match(player1, player2, data['match_name'], player1, player2)
            # Those repetitions will be removed
        else:
            self.app.root.ids.game_screen.match = Match(player1, player2, data['match_name'], player2, player1)
            # Those repetitions will be removed
        self.app.root.ids.game_screen.check_server(self.app.root.ids.game_screen.match)
        self.app.change_screen('game_screen')
        self.save.dismiss()
        self.save = None
