import logging as log
import json
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
        self.confirmation_save_match = None
        self.app = MDApp.get_running_app()

    def update_scoreboard(self, winner, opponent, match):
        """Updates the scoreboard each time a player wons a point"""
        match.points_win(winner, opponent)
        self.ids.points_label1.text = match.player1.get_points_amount()
        self.ids.points_label2.text = match.player2.get_points_amount()
        self.ids.games_label1.text = match.player1.get_games_amount()
        self.ids.games_label2.text = match.player2.get_games_amount()
        self.ids.sets_label1.text = match.player1.get_sets_amount()
        self.ids.sets_label2.text = match.player2.get_sets_amount()
        self.ids.fault.text = 'Fault'  # Fixes problem with Fault / DoubleFault button
        self.check_server(match)

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
            self.match.server.service_stats['second_service'][self.match.set_index] += 1
            self.match.server.service_stats['second_service_in'][self.match.set_index] += 1
        elif self.ids.fault.text == 'Double Fault':
            self.ids.fault.text = 'Fault'
            self.update_scoreboard(
                self.match.receiver, self.match.server,
                self.match)

    def set_winner(self, winner, looser):
        """Sets which player wins the point"""
        self.looser = looser
        self.winner = winner

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

    def server(self, server, receiver):
        """Sets which player serves or receives, depending on user's choice"""
        self.match.server = server
        self.match.receiver = receiver
        self.check_server(self.match)
        self.dialog.dismiss()
        self.dialog = None
        log.info('Le serveur est ' + self.match.server.get_name())

    def show_dialog_save_match_confirmation(self):
        """Shows a dialog box to ask if the player wants to save the match"""
        if not self.confirmation_save_match:
            self.confirmation_save_match = MDDialog(title='Do you want to save the match?',
                                                    size_hint=(0.7, 1),
                                                    buttons=[
                                                        MDFlatButton(text='Yes',
                                                                     text_color=self.app.theme_cls.primary_color,
                                                                     on_release=lambda x: self.leave_match()
                                                                     ),
                                                        MDFlatButton(text='No, cancel',
                                                                     text_color=self.app.theme_cls.primary_color,
                                                                     on_release=lambda x: self.cancel())])
        self.confirmation_save_match.open()

    def cancel(self):
        self.confirmation_save_match.dismiss()
        self.confirmation_save_match = None

    def leave_match(self):
        full_list = self.app.root.ids.save_screen.full_list  # Full json file (list format)
        to_remove_dict = self.app.root.ids.save_screen.picked_game_data
        # Lines that we want to remove, to avoid duplication of saves
        if full_list is not None and to_remove_dict is not None:  # Check to avoid errors, if the file is empty
            for i in full_list:
                if to_remove_dict == i:
                    full_list.remove(self.app.root.ids.save_screen.picked_game_data)
                    with open('data.json', 'w') as file:
                        json.dump(full_list, file, indent=4, sort_keys=True)
                        # Rewrite the json file, without the duplication
        self.app.change_screen('home_screen')
        self.cancel()
        self.match.save_match()

    def service_number(self):
        if self.winner.name == self.match.server.name:
            if self.ids.fault.text == 'Fault':
                self.match.server.service_stats['first_service_won'][self.match.set_index] += 1
            elif self.ids.fault.text == 'Double Fault':
                self.match.server.service_stats['second_service_won'][self.match.set_index] += 1
        log.info('First Service Won {}'.format(self.match.server.service_stats['first_service_won']))

    def button_ace_press(self):
        self.set_winner(self.match.server, self.match.receiver)
        self.service_number()
        self.match.ace_played()
