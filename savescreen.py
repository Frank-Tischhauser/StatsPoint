import json
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineAvatarIconListItem, IconRightWidget, IconLeftWidget
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton


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

    def on_pre_enter(self, *args):
        self.app.root.ids.my_toolbar.right_action_items = [["settings", lambda x:
                                                            self.app.root.ids.my_toolbar.show_dialog_confirmation()]]
    def saved_match_list(self):
        """Creates a list with all saved games"""
        self.ids.match_list.clear_widgets()  # To avoid duplication of widgets
        with open('data.json', 'r') as file:
            data = json.load(file)
        for match_info in data:  # For every match saved in the JSON file
            self.empty = False
            result = OneLineAvatarIconListItem(text='{} : {} vs {}'.format(
                match_info['match_name'], match_info['player1_name'],
                match_info['player2_name']))  # Add a OneListItem widget (UI)
            result.bind(on_press=lambda a, i=match_info: self.show_dialog_saves(i, data))
            delete_save = DeleteSave(icon='close',
                                     on_press=lambda x, i=match_info: DeleteSave().show_dialog_delete_save(i))
            tennis_icon = IconLeftWidget(icon='tennis',
                                         on_press=lambda a, i=match_info: self.show_dialog_saves(i, data))
            result.add_widget(tennis_icon)
            # Adds a button to delete the match
            result.add_widget(delete_save)
            # Gets the information of the match which is chosen by the user
            self.ids.match_list.add_widget(result)
        if self.empty:  # Writes a message if there is not match saved
            self.ids.empty_text.text = 'There are no saves! Create a game!'
        else:
            self.ids.empty_text.text = ''
        self.empty = True

    def show_dialog_saves(self, data, full_list):
        """Gives the choice to the user :
        Whether he continues the game, or he checks the data of the game"""
        if not self.save:
            self.save = MDDialog(title='Do you want to continue the match or see the statistics?',
                                 size_hint=(0.7, 1),
                                 buttons=[
                                     MDRaisedButton(text='Continue',
                                                  on_release=lambda x: self.continue_game(data, full_list)),
                                     MDFlatButton(text='Stats / Analysis', text_color=self.app.theme_cls.primary_color,
                                                  on_release=lambda x: self.data_choice(data))])
        self.save.open()

    def data_choice(self, data):
        """Goes to the data_screen depending on the user's choice"""
        if self.save is not None:
            self.app.root.ids.data_screen.show_scoreboard(data)
            self.app.root.ids.data_screen.show_stats(data)
            self.app.root.ids.data_screen.check_stat_winner()
            self.app.change_screen('data_screen')
            self.save.dismiss()
            self.save = None

    def continue_game(self, data, full_list):
        if self.save is not None:
            self.picked_game_data = data  # To get the information from another class
            self.full_list = full_list
            """Continues the game"""
            player1 = Player(data['player1_name'], data['player1_stats'])
            player2 = Player(data['player2_name'], data['player2_stats'])
            self.app.root.ids.game_screen.player1 = player1
            self.app.root.ids.game_screen.player2 = player2

            if data['server'] == player1.name:
                self.app.root.ids.game_screen.match = Match(player1, player2, data['match_name'], player1, player2,
                                                            data['sets_winners'])
                # Those repetitions will be removed
            else:
                self.app.root.ids.game_screen.match = Match(player1, player2, data['match_name'], player2, player1,
                                                            data['sets_winners'])
                # Those repetitions will be removed
            self.app.root.ids.game_screen.check_server(self.app.root.ids.game_screen.match)
            self.app.change_screen('game_screen')
            self.save.dismiss()
            self.save = None


class DeleteSave(IconRightWidget):
    """Contains the button to delete a game"""
    delete_confirmation = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()  # To get all app methods / attributes

    def show_dialog_delete_save(self, to_remove_data):
        """Ask the user to confirm his choice"""
        if not self.delete_confirmation:
            self.delete_confirmation = MDDialog(title='Do you want to delete this game?',
                                                size_hint=(0.7, 1),
                                                buttons=[
                                                    MDFlatButton(text='Yes',
                                                                 text_color=self.app.theme_cls.primary_color,
                                                                 on_release=lambda x: self.delete_data(to_remove_data)),
                                                    MDFlatButton(text='No, cancel',
                                                                 text_color=self.app.theme_cls.primary_color,
                                                                 on_release=lambda x: self.cancel())])
        self.delete_confirmation.open()

    def cancel(self):
        """Dismisses the dialog box"""
        if self.delete_confirmation is not None:
            self.delete_confirmation.dismiss()

    def delete_data(self, to_remove_data):
        """Deletes the selected game"""
        if self.delete_confirmation is not None:
            with open('data.json', 'r') as js:
                file = json.load(js)
            for game in file:
                if to_remove_data == game:  # Removes the right dictionary
                    file.remove(to_remove_data)
            with open('data.json', 'w') as js:  # Rewrites the file without the removed dict
                json.dump(file, js, indent=4, sort_keys=True)
            self.app.root.ids.save_screen.saved_match_list()  # Updates the screen
            self.cancel()
