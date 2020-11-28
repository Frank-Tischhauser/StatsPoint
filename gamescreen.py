# pylint: disable=E1101
"""
GameScreen

Module that manges the scoreboard system and the input of the information for every point.
"""


import logging as log
import json
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.behaviors import RectangularElevationBehavior
from kivy.properties import StringProperty


class ScoreLine(MDBoxLayout, RectangularElevationBehavior):
    """Box containing the score with a shadow effect"""


class Square(MDBoxLayout, RectangularElevationBehavior):
    """Square set in the kv file, contains numbers / stats"""


class Box(MDBoxLayout, RectangularElevationBehavior):
    """White box with shadow effect"""


class GameScreen(MDScreen):
    """
    Contains all the buttons that are used by the user during a match
    ...
    Attributes
    ----------
    app : object
        Instance of the class StatsPointApp.

    winner : object
        Instance of the class Player. The player who won the point.

    looser : object
        Instance of the class Player. The player who lost the point.

    dialog : object
        Instance of MDDialog class. It is a UI widget.

    confirmation_save_match : object
        Instance of MDDialog class. It is a UI widget.

    Methods
    -------
    on_pre_enter():
        Is called just before the user sees the screen.

    on_pre_leave():
        Is called just before leaving the screen.

    update_scoreboard(winner, opponent, match, score_change=True):
        Updates the scoreboard each time a player wins a point.

    square_design(player, line_score):
        Change the design of the square object when a player wins a set.

    check_server(match):
        Hide or show the tennis-ball icon depending on which player serves.

    set_winner(winner, looser):
        Sets which player wins the point.

    show_dialog_server():
        Shows a dialog box to ask which player serves first.

    server(server, receiver):
        Sets which player serves or receives, depending on user's choice.

    show_dialog_save_match_confirmation():
        Shows a dialog box to ask if the player wants to save the match.

    cancel():
        Cancels the confirmation_save_match dialog.

    leave_match(match_end=False):
        Leaves and saves the match.

    check_service_degree():
        Checks if it's a first or second serve.

    press_ace():
        Called at each ace.

    press_rally():
        Called each time there is a rally.

    press_fault():
        Called each time there is a fault in the service.

    press_save():
        Called each time the user wants to save the match.

    press_player(winner_pl, looser_pl):
        Called when the user chose the winner of the point.

    press_unforced_error():
        Called when there is an unforced error.

    press_forced_error():
        Called when there is a forced error.

    press_winner():
        Called when there is a winner.

    press_volley():
        Called if the last shot was a volley.

    press_backhand():
        Called if the last shot was a backhand.

    press_forehand():
        Called if the last shot was a forehand.
    """

    detail_context = StringProperty('')
    """
    Detail about how a point ended.
    Can be "unforced_error", "forced_error" or "winner".

    :attr:`detail_context` is a :class:`~kivy.properties.StringProperty`
    and defaults to `''`.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.winner = None
        self.looser = None
        self.dialog = None
        self.confirmation_save_match = None
        self.app = MDApp.get_running_app()

    def on_pre_enter(self, *args):
        """Is called just before the user sees the screen"""
        self.ids.score_line1.ids.player_name.text = self.player1.get_name()
        self.ids.score_line2.ids.player_name.text = self.player2.get_name()
        self.ids.pl1_btn.text = self.player1.get_name()
        self.ids.pl2_btn.text = self.player2.get_name()
        self.update_scoreboard(self.winner, self.looser, self.match, False)
        self.app.root.ids.my_toolbar.title = 'Game'

    def on_pre_leave(self, *args):
        """Called just before leaving the screen"""
        self.ids.game_manager.current = 'service'

    def update_scoreboard(self, winner, opponent, match, score_change=True):
        """Updates the scoreboard each time a player wins a point"""
        if score_change:
            match.points_win(winner, opponent)
        players = [match.player1, match.player2]
        line_scores = [self.ids.score_line1, self.ids.score_line2]

        for (player, line_score) in zip(players, line_scores):
            line_score.ids.points_label.ids.label.text = player.get_points_amount()
            line_score.ids.set1.ids.label.text = str(player.total_games[0])
            line_score.ids.set2.ids.label.text = str(player.total_games[1])
            line_score.ids.set3.ids.label.text = str(player.total_games[2])
            self.square_design(player, line_score)
        self.ids.fault.text = 'Fault'  # Fixes problem with Fault / DoubleFault button
        self.check_server(match)

    def square_design(self, player, line_score):
        """Changes the square design when a player wins a set"""
        squares = [line_score.ids.set1, line_score.ids.set2, line_score.ids.set3]
        for (index, square) in zip(range(3), squares):
            if player.name == self.match.sets_winners[index]:
                square.md_bg_color = (0.91, 0.46, 0.07, 1)
                square.ids.label.text_color = (1, 1, 1, 1)
                square.elevation = 5
            else:
                square.md_bg_color = (self.app.get_rgba_from_hex('#f1f1f1'))
                square.ids.label.text_color = (0, 0, 0, 1)
                square.elevation = 0

    def check_server(self, match):
        """Hide or show the tennis-ball icon depending on which player serves"""
        if match.server.get_name() == match.player1.get_name():
            self.ids.score_line2.ids.server.opacity = 0
            self.ids.score_line1.ids.server.opacity = 1
        else:
            self.ids.score_line2.ids.server.opacity = 1
            self.ids.score_line1.ids.server.opacity = 0

    def set_winner(self, winner, looser):
        """Sets which player wins the point"""
        self.looser = looser
        self.winner = winner

    def show_dialog_server(self):
        """Shows a dialog box to ask which player serves first"""
        if not self.dialog:
            self.dialog = MDDialog(title='Who serves first?', size_hint=(0.7, 1), buttons=[
                MDFlatButton(text=self.app.root.ids.input_screen.ids.entry1.text,
                             text_color=self.app.theme_cls.primary_color,
                             on_release=lambda x: self.server(
                                 self.player1, self.player2)),
                MDFlatButton(text=self.app.root.ids.input_screen.ids.entry2.text,
                             text_color=self.app.theme_cls.primary_color,
                             on_release=lambda x: self.server(
                                 self.player2, self.player1))])
        self.dialog.open()

    def server(self, server, receiver):
        """Sets which player serves or receives, depending on user's choice"""
        if self.dialog is not None:
            self.match.server = server
            self.match.receiver = receiver
            self.check_server(self.match)
            self.dialog.dismiss()
            self.dialog = None
            log.info('Le serveur est ' + self.match.server.get_name())

    def show_dialog_save_match_confirmation(self):
        """Shows a dialog box to ask if the player wants to save the match"""
        if not self.confirmation_save_match:
            self.confirmation_save_match = MDDialog(
                title='Do you want to save the match?',
                size_hint=(0.7, 1),
                buttons=[
                    MDFlatButton(text='Yes',
                                 text_color=self.app.theme_cls.primary_color,
                                 on_release=lambda x: self.leave_match(),
                                 ),
                    MDFlatButton(text='No, cancel',
                                 text_color=self.app.theme_cls.primary_color,
                                 on_release=lambda x: self.cancel())])
        self.confirmation_save_match.open()

    def cancel(self):
        """Cancels the confirmation_save_match dialog"""
        if self.confirmation_save_match is not None:
            self.confirmation_save_match.dismiss()
            self.confirmation_save_match = None

    def leave_match(self, match_end=False):
        """Leaves and saves the match"""
        if self.confirmation_save_match is not None or match_end:
            full_list = self.app.root.ids.save_screen.full_list  # Full json file (list format)
            to_remove_dict = self.app.root.ids.save_screen.picked_game_data
            # Lines that we want to remove, to avoid duplication of saves
            if full_list is not None and to_remove_dict is not None:
                # Check to avoid errors, if the file is empty
                for i in full_list:
                    if to_remove_dict == i:
                        full_list.remove(self.app.root.ids.save_screen.picked_game_data)
                        with open('../statspoint_data.json', 'w') as file:
                            json.dump(full_list, file, indent=4, sort_keys=True)
                            # Rewrite the json file, without the duplication
            self.app.change_screen('home_screen')
            self.cancel()
            self.match.save_match(match_end)

    def check_service_degree(self):
        """Checks if it's a first or second serve"""
        if self.winner.name == self.match.server.name:
            if self.ids.fault.text == 'Fault':
                self.match.server.service_stats['first_service_won'][self.match.set_index] += 1
            elif self.ids.fault.text == 'Double Fault':
                self.match.server.service_stats['second_service_won'][self.match.set_index] += 1
        log.info('First Service Won {}'.format(
            self.match.server.service_stats['first_service_won']))

    def press_ace(self):
        """Called at each ace"""
        self.set_winner(self.match.server, self.match.receiver)
        self.check_service_degree()
        self.match.receiver.stats['return_points_played'][self.match.set_index] -= 1
        self.match.ace_played()
        self.update_scoreboard(self.match.server, self.match.receiver, self.match)
        log.info('yes' + str(self.match.server.total_points))

    def press_rally(self):
        """Called each time there is a rally"""
        self.ids.game_manager.current = 'on_court'

    def press_fault(self):
        """Called each time there is a fault in the service"""
        if self.ids.fault.text == "Fault":
            self.ids.fault.text = 'Double Fault'
            self.match.server.service_stats['second_service'][self.match.set_index] += 1
            self.match.server.service_stats['second_service_in'][self.match.set_index] += 1

        elif self.ids.fault.text == 'Double Fault':
            self.match.server.service_stats['second_service_in'][self.match.set_index] -= 1
            self.match.server.service_stats['double_faults'][self.match.set_index] += 1
            self.match.receiver.stats['return_points_played'][self.match.set_index] -= 1
            log.info(self.match.server.service_stats['double_faults'])
            self.ids.fault.text = 'Fault'
            self.update_scoreboard(self.match.receiver, self.match.server, self.match)

    def press_save(self):
        """Called when the user wants to save the match"""
        self.show_dialog_save_match_confirmation()

    def press_player(self, winner_pl, looser_pl):
        """Called when the user chose the winner of the point"""
        self.set_winner(winner_pl, looser_pl)
        self.check_service_degree()
        if self.match.receiver.name == self.winner.name:
            self.match.receiver.stats['return_points_won'][self.match.set_index] += 1
        self.ids.detail1_box.ids.caption.text = 'Why did {} win the point?'.format(
            self.winner.get_name())
        self.ids.game_manager.current = 'game_details1'

    def press_unforced_error(self):
        """Called when there is an unforced error"""
        self.detail_context = 'unforced_error'
        self.ids.detail2_box.ids.caption.text = "{}'s unforced error was a ...".format(
            self.looser.get_name())
        self.looser.stats['unforced_errors'][self.match.set_index] += 1
        self.ids.game_manager.current = 'game_details2'

    def press_forced_error(self):
        """Called when there is a forced error"""
        self.detail_context = 'forced_error'
        self.update_scoreboard(self.winner, self.looser, self.match)
        self.ids.game_manager.current = 'service'

    def press_winner(self):
        """Called when there is a winner"""
        self.detail_context = 'winner'
        self.ids.detail2_box.ids.caption.text = "{}'s winner was a ...".format(
            self.winner.get_name())
        self.ids.game_manager.current = 'game_details2'
        self.winner.stats['winners'][self.match.set_index] += 1

    def press_volley(self):
        """Called if the last shot was a volley"""
        if self.detail_context == 'forced_error':
            self.winner.stats['net_points'][self.match.set_index] += 1
        elif self.detail_context == 'winner':
            self.winner.stats['net_points'][self.match.set_index] += 1
            self.winner.stats['net_winners'][self.match.set_index] += 1
        elif self.detail_context == 'unforced_error':
            self.looser.stats['net_unforced_errors'][self.match.set_index] += 1
        self.update_scoreboard(self.winner, self.looser, self.match)
        self.ids.game_manager.current = 'service'

    def press_backhand(self):
        """Called if the last shot was a backhand"""
        self.update_scoreboard(self.winner, self.looser, self.match)
        self.ids.game_manager.current = 'service'
        if self.detail_context == 'unforced_error':
            self.looser.stats['backhand_unforced_errors'][self.match.set_index] += 1
        elif self.detail_context == 'winner':
            self.winner.stats['backhand_winners'][self.match.set_index] += 1

    def press_forehand(self):
        """Called if the last shot was a forehand"""
        self.update_scoreboard(self.winner, self.looser, self.match)
        self.ids.game_manager.current = 'service'
        if self.detail_context == 'unforced_error':
            self.looser.stats['forehand_unforced_errors'][self.match.set_index] += 1
        elif self.detail_context == 'winner':
            self.winner.stats['forehand_winners'][self.match.set_index] += 1
