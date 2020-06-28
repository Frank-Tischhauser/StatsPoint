from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from player import Player
from match import Match


class InputScreen(MDScreen):
    """The user gives all the information for the creation of a match"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()

    def create_match(self):
        """Creates a match when button pressed"""
        player1 = Player(self.ids.entry1.text)
        player2 = Player(self.ids.entry2.text)
        self.app.root.ids.game_screen.player1 = player1
        self.app.root.ids.game_screen.player2 = player2
        self.app.root.ids.game_screen.match = Match(player1, player2, self.ids.entry3.text)

    def check_text(self):
        """Checks if a textfield is empty"""
        player1 = self.ids.confirmation_button.checking_text[0]
        player2 = self.ids.confirmation_button.checking_text[1]
        condition = True
        for text in self.ids.confirmation_button.checking_text:
            if text == '' or text == ' ':
                self.ids.error_message.text = 'Error : A required field is missing!'
                condition = False
        if player1 == player2:
            condition = False
            self.ids.error_message.text = 'Error : Both players cannot have the same name!'
        elif len(player1) > 9 or len(player2) > 9:
            condition = False
            self.ids.error_message.text = 'Error : Names are too long!'
        if condition:
            self.create_match()
            self.app.root.ids.game_screen.show_dialog_server()
            self.app.change_screen('game_screen')
