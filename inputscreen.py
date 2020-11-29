"""
InputScreen

Module that manages the creation of a match / game.
"""

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from player import Player
from match import Match


class InputScreen(MDScreen):
    """
    The user gives all the information for the creation of a match
    ...
    Attributes
    ----------
    app : object
        Instance of the class StatsPointApp.

    Methods
    -------
    on_pre_enter():
        Is called just before the user sees the screen.

    create_match():
        Creates a match when button pressed.

    check_text():
        Checks if the text written respects the all the conditions.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()

    def on_pre_enter(self, *args):
        """Is called just before the user sees the screen"""
        self.app.root.ids.my_toolbar.title = 'Create a game'
        self.app.root.ids.my_toolbar.right_action_items = [
            ["information-outline", lambda x: self.app.root.ids.my_toolbar.show_dialog_confirmation()]]

    def create_match(self):
        """Creates a match when button pressed"""
        player1 = Player(self.ids.entry1.text)
        player2 = Player(self.ids.entry2.text)
        self.app.root.ids.game_screen.player1 = player1
        self.app.root.ids.game_screen.player2 = player2
        self.app.root.ids.game_screen.match = Match(player1, player2, self.ids.entry3.text)
        self.app.root.ids.game_screen.ids.score_line1.ids.server.opacity = 0
        # Fixes small graphic bug
        self.app.root.ids.game_screen.ids.score_line2.ids.server.opacity = 0

    def check_text(self):
        """Checks if the text written respects the conditions"""
        condition = True
        fields = [self.ids.entry1, self.ids.entry2, self.ids.entry3]
        fields[0].error = False
        fields[1].error = False
        fields[2].error = False
        if fields[0].text == fields[1].text:  # If both players have the same name (creates bugs)
            self.ids.error_message.text = 'Both players cannot have the same name!'
            fields[0].error = True
            fields[1].error = True
        for field in fields:
            if field.text == '' or field.text == ' ':  # If a field is empty
                self.ids.error_message.text = 'A field is empty!'
                field.error = True
            elif len(field.text) > 8:  # If names are too long (creates graphic bugs)
                self.ids.error_message.text = 'Names are too long!'
                field.error = True
            if field.error:
                condition = False
                field.error = False
        if condition:  # If everything is fine, creates the match
            self.create_match()
            self.app.root.ids.game_screen.show_dialog_server()
            self.app.root.ids.save_screen.picked_game_data = None
            # To avoid problems with saved games
            self.app.root.ids.save_screen.full_list = None
            self.app.change_screen('game_screen')
