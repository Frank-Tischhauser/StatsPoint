import json
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineListItem
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.lang import Builder
from kivy.uix.screenmanager import SlideTransition
from kivy.core.window import Window
from player import Player
from match import Match
from game_screen import GameScreen


Window.size = (350, 500)


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
    app = None

    def saved_match_list(self):
        """Creates a list with all saved games"""
        self.app = TennisApp.get_running_app()
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


class DataScreen(MDScreen):
    """Shows the data of a match"""

    def show_data(self, data):
        self.ids.player1_name.text = data['winner_name']
        self.ids.player2_name.text = data['looser_name']
        self.ids.set1_player1.text = str(data['winner_games'][0])
        self.ids.set2_player1.text = str(data['winner_games'][1])
        self.ids.set3_player1.text = str(data['winner_games'][2])
        self.ids.set1_player2.text = str(data['looser_games'][0])
        self.ids.set2_player2.text = str(data['looser_games'][1])
        self.ids.set3_player2.text = str(data['looser_games'][2])


class SettingScreen(MDScreen):
    """Screen that contains all the settings"""
    pass


class TennisApp(MDApp):
    confirmation = None

    def build(self):
        """Creates the app"""
        self.theme_cls.primary_palette = "Teal"
        return Builder.load_file("kv/main.kv")

    def change_screen(self, screen_name, direction='left'):
        """Changes the current screen using the ScreenManager"""
        self.root.ids.manager.transition = SlideTransition(direction=direction)
        self.root.ids.manager.current = screen_name

    def create_match(self):
        """Creates a match when button pressed"""
        player1 = Player(self.root.ids.input_screen.ids.entry1.text)
        player2 = Player(self.root.ids.input_screen.ids.entry2.text)
        GameScreen.player1 = player1
        GameScreen.player2 = player2
        GameScreen.match = Match(player1, player2, self.root.ids.input_screen.ids.entry3.text)

    def check_text(self):
        """Checks if a textfield is empty"""
        condition = True
        for text in self.root.ids.input_screen.ids.confirmation_button.checking_text:
            if text == '' or text == ' ':
                condition = False
        if condition:
            self.create_match()
            self.root.ids.game_screen.show_dialog_server()
            self.change_screen('game_screen')
        else:
            self.root.ids.input_screen.ids.error_message.text = 'Error : A required field is missing!'

    def show_dialog_confirmation(self):
        """Shows a dialog box to confirm the user's choice"""
        if not self.confirmation:
            self.confirmation = MDDialog(title='Do you want to leave this screen?', size_hint=(0.7, 1), buttons=[
                MDFlatButton(text='Yes', text_color=self.theme_cls.primary_color,
                             on_press=lambda x: self.change_screen('setting_screen'),
                             on_release=lambda x: self.dismiss_confirmation()),
                MDFlatButton(text='No, Cancel', text_color=self.theme_cls.primary_color,
                             on_release=lambda x: self.dismiss_confirmation())])
        self.confirmation.open()

    def dismiss_confirmation(self):
        self.confirmation.dismiss()
        self.confirmation = None


if __name__ == "__main__":
    TennisApp().run()
