import logging as log
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton


class GameScreen(MDScreen):
    """Contains all the buttons that are used by the user during a match"""

    def __init__(self, **kw):
        super().__init__(**kw)
        self.winner = None
        self.looser = None
        self.dialog = None
        self.app = MDApp.get_running_app()

    def win_condition(self):
        if self.ids.sets_label1.text == '2' or \
                self.ids.sets_label2.text == '2':
            self.app.change_screen('home_screen', 'right')

    def update_scoreboard(self, winner, opponent, match):
        """Updates the scoreboard each time a player wons a point"""
        match.points_win(winner, opponent)
        self.ids.points_label1.text = match.player1.get_points_amount()
        self.ids.points_label2.text = match.player2.get_points_amount()
        self.ids.games_label1.text = match.player1.get_games_amount()
        self.ids.games_label2.text = match.player2.get_games_amount()
        self.ids.sets_label1.text = match.player1.get_sets_amount()
        self.ids.sets_label2.text = match.player2.get_sets_amount()
        self.ids.fault.text = 'Fault'
        self.check_server(match)
        self.win_condition()

    def check_server(self, match):
        """Hide or show the tennis-ball icon depending on which player serves"""
        if match.server.get_name() == match.player1.get_name():
            self.ids.server2.opacity = 0
            self.ids.server1.opacity = 1
        else:
            self.ids.server2.opacity = 1
            self.ids.server1.opacity = 0

    def modify_fault_button(self):
        """Modify the button (Fault / Double Fault)"""
        if self.ids.fault.text == "Fault":
            self.ids.fault.text = 'Double Fault'
        elif self.ids.fault.text == 'Double Fault':
            self.ids.fault.text = 'Fault'
            self.update_scoreboard(
                self.match.receiver, self.match.server,
                self.match)

    def set_winner(self, winner, looser):
        """Sets which player wins the point"""
        self.looser = looser
        self.winner = winner

    def server(self, server, receiver):
        """Sets which player serves or receives"""
        self.match.server = server
        self.match.receiver = receiver
        self.check_server(self.match)
        self.dialog.dismiss()
        self.dialog = None
        log.info(self.match.server.get_name())

    def show_dialog_server(self):
        """Shows a dialog box to ask which player serves first"""
        if not self.dialog:
            self.dialog = MDDialog(title='Who serves first?', size_hint=(0.7, 1), buttons=[
                MDFlatButton(text=self.app.root.ids.input_screen.ids.entry1.text, text_color=self.app.theme_cls.primary_color,
                             on_release=lambda x: self.server(
                                 self.player1, self.player2)),
                MDFlatButton(text=self.app.root.ids.input_screen.ids.entry2.text, text_color=self.app.theme_cls.primary_color,
                             on_release=lambda x: self.server(
                                 self.player2, self.player1))])
        self.dialog.open()
        log.info(self.app.root.ids.input_screen.ids.entry1.text)
