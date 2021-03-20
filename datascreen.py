"""
DataScreen

This module contains the DataScreen class and all the classes which are related to it.
This screen contains and shows all the statistics of a tennis match.
"""
import json

from kivy.properties import StringProperty
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.clock import Clock

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.behaviors import RectangularElevationBehavior
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDFillRoundFlatButton
from kivymd.uix.dialog import MDDialog

from stats_display import StatsDisplay


def safe_div(num1, num2):
    """Returns an integer division.
    Avoids error if division by zero."""
    if num2 <= 0:
        return 0
    return num1 / num2


def number_comparison(col1, col3, highlight='max'):
    """Highlights the right statistic depending on number values"""
    result = None, None
    if highlight == 'ratio':  # Highlights the greatest number ratio
        ratio1 = col1.ids.label.text
        col1.ids.label.font_size = '14sp'
        col3.ids.label.font_size = '14sp'
        div_numbers1 = list(map(int, ratio1.split('/')))
        quotient1 = safe_div(div_numbers1[0], div_numbers1[1])
        ratio2 = col3.ids.label.text
        div_numbers2 = list(map(int, ratio2.split('/')))
        quotient2 = safe_div(div_numbers2[0], div_numbers2[1])
        if quotient1 > quotient2:
            result = col1, col3
        elif quotient2 > quotient1:
            result = col3, col1
    elif highlight in ('max', 'min'):
        final_num1 = int(col1.ids.label.text.split(' ')[0])
        final_num2 = int(col3.ids.label.text.split(' ')[0])
        if highlight == 'max':  # Highlights the greatest number
            if final_num1 > final_num2:
                result = col1, col3
            elif final_num2 > final_num1:
                result = col3, col1
        else:  # Highlights the lowest number
            if final_num1 > final_num2:
                result = col3, col1
            elif final_num2 > final_num1:
                result = col1, col3
    return result


class Rows(MDBoxLayout):
    """Rows of a table (MDGridLayout)"""
    highlight = StringProperty('max')
    """
    The name of the highlighting system.

    :attr:`highlight` is a :class:`~kivy.properties.StringProperty`
    and defaults to `'max'`.
    """


class DataLine(MDBoxLayout, RectangularElevationBehavior):
    """Line that contains the result of a match"""


class LeaderBoard(MDGridLayout):
    """
    Table which contains DataLines
    ...
    Methods
    -------
    add_rows(rows_number)
        Adds the rows that will include all the stats.
    """

    def add_rows(self, rows_number=19):
        """Add the rows that will include all the stats"""
        self.rows = rows_number
        rows_liste = []
        for i in range(rows_number):
            rows_liste.append(Rows())
        for row in rows_liste:
            self.add_widget(row)


class DataScreen(MDScreen):
    """
    Shows the data of a match
    ...
    Attributes
    ----------
    app : object
        Instance of the class StatsPointApp.

    stats_widgets : list
        Contains the four widgets which display the stats.

    data : dict
        Contains the data of the whole match.

    stats_display : object
        Instance of the class StatsDisplay.

    confirmation_dialog : object
        Instance of MDDialog class. It is a UI widget.

    Methods
    -------
    on_pre_enter():
        Is called just before the user sees the screen.

    create_special_row():
        Creates the last row, which contains the button to get the 'analysis'.

    change_last_row():
        Changes the last row of the stats_widget with the special row which contains a button.

    scroll_animation():
        Scrolls the screen from the top to the bottom, to make the user aware of the last row.

    start():
        Is called only once, at the start of the application to initialize widgets.

    show_scoreboard():
        Shows a scoreboard displaying the result of the tennis match.

    change_square_design(player_name, line_score, data):
        Changes the square design if a player wins a set.

    show_stats():
        Shows all statistics of a tennis match.

    check_stat_winner():
        Highlights the best statistic between both players.

    reset_square_design(square):
        Resets the design of a square.

    show_confirmation_dialog():
        Shows the confirmation dialog (MDDialog class).

    go_to_form():
        Switches to the form screen and dismisses the dialog box.

    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.stats_widgets = [LeaderBoard(), LeaderBoard(), LeaderBoard(), LeaderBoard()]
        for widget in self.stats_widgets:
            widget.add_rows()
        self.data = None
        self.stats_display = None
        self.confirmation_dialog = None

    def on_pre_enter(self, *args):
        """Is called just before the user sees the screen"""
        self.app.root.ids.my_toolbar.right_action_items = [
            ["plus", lambda x: self.show_confirmation_dialog()]]
        self.confirmation_dialog = None
        self.app.root.ids.my_toolbar.title = 'Statistics'
        for i in range(4):  # To avoid duplicated widgets with the last row
            self.stats_widgets[i].children[0].clear_widgets()
        self.show_scoreboard()
        self.show_stats()
        self.check_stat_winner()
        self.change_last_row()

    def create_special_row(self):
        """Creates the last row, which contains the button to get the 'analysis' """
        row = MDBoxLayout(spacing=dp(50))
        button = MDFillRoundFlatButton(
            text='Get more info!',
            on_release=lambda x: self.show_confirmation_dialog())
        button.text_color = (1, 1, 1, 1)
        button.font_name = 'fonts/Montserrat-Regular.ttf'
        button.md_bg_color = (0.91, 0.46, 0.07, 1)
        row.add_widget(Widget())  # To center the button
        row.add_widget(button)
        row.add_widget(Widget())
        return row

    def change_last_row(self):
        """Changes the last row of the stats_widget with the special row which contains a button"""
        for i in range(4):
            self.stats_widgets[i].children[0].add_widget(self.create_special_row())

    def scroll_animation(self):
        """Scrolls the screen from the top to the bottom, to make the user aware of the last row"""

        with open('json_files/settings.json', 'r') as r_json:
            content = json.load(r_json)
        if content['show_tutorial']:  # Make it happen only once
            self.ids.set1_scroll.scroll_to(
                self.stats_widgets[0].children[0], animate={'d': 0.5, 't': 'out_quad'})

            Clock.schedule_once(
                lambda x: self.ids.set1_scroll.scroll_to(
                    self.stats_widgets[0].children[-1], animate={'d': 0.5, 't': 'out_quad'}), 3)
            content['show_tutorial'] = False
            with open('json_files/settings.json', 'w') as w_json:
                json.dump(content, w_json, indent=4, sort_keys=True)

    def start(self):
        """Is called only once, at the start of the application to initialize widgets"""
        self.ids.set1_scroll.add_widget(self.stats_widgets[0])
        self.ids.set2_scroll.add_widget(self.stats_widgets[1])
        self.ids.set3_scroll.add_widget(self.stats_widgets[2])
        self.ids.total_scroll.add_widget(self.stats_widgets[3])

    def show_scoreboard(self):
        """Shows a scoreboard with the result of the tennis match"""
        players = [self.ids.player1, self.ids.player2]
        stats = [self.data['player1_stats'], self.data['player2_stats']]
        for player, name, stat in zip(
                players, [self.data['player1_name'], self.data['player2_name']], stats):
            player.ids.player_name.text = name
            player.ids.set1.ids.label.text = str(stat['total_games'][0])
            player.ids.set2.ids.label.text = str(stat['total_games'][1])
            player.ids.set3.ids.label.text = str(stat['total_games'][2])
            self.change_square_design(name, player, self.data)

    def change_square_design(self, player_name, line_score, data):
        """Changes the square design if a player wins a set"""
        squares = [line_score.ids.set1, line_score.ids.set2, line_score.ids.set3]
        for (index, square) in zip(range(3), squares):
            if player_name == data['sets_winners'][index]:
                square.md_bg_color = (0.91, 0.46, 0.07, 1)
                square.ids.label.text_color = (1, 1, 1, 1)
                square.elevation = 5
            else:
                square.md_bg_color = (self.app.get_rgba_from_hex('#f1f1f1'))
                square.ids.label.text_color = (0, 0, 0, 1)
                square.elevation = 0

    def show_stats(self):
        """Shows all statistics of a tennis match"""
        players = ['player1', 'player2']
        leaderboard = self.stats_widgets.copy()
        leaderboard.pop(-1)
        self.stats_display = StatsDisplay(self.data)
        for manche in range(3):
            self.stats_display.write_captions(leaderboard[manche])
            for player in players:
                stats = self.stats_display.get_stats_sets(manche, player)
                self.stats_display.display_stats(stats, leaderboard[manche], player)
        self.stats_display.write_captions(self.stats_widgets[3])
        for player in players:
            stats = self.stats_display.get_match_stats(player)
            self.stats_display.display_stats(stats, self.stats_widgets[3], player)

    def check_stat_winner(self):
        """Highlights the best statistic between both players"""

        for manche in self.stats_widgets:
            for row in manche.children:
                if len(row.children) > 0:
                    cols = [row.ids.col1, row.ids.col3]
                    winner_col, looser_col = number_comparison(cols[0], cols[1], row.highlight)
                    if winner_col is not None and looser_col is not None:
                        winner_col.md_bg_color = (0.91, 0.46, 0.07, 1)
                        winner_col.ids.label.text_color = (1, 1, 1, 1)
                        winner_col.elevation = 5
                        self.reset_square_design(looser_col)
                    else:
                        self.reset_square_design(cols[0])
                        self.reset_square_design(cols[1])

                    if row.highlight == 'name':
                        for i in range(2):
                            cols[i].size_hint_x = 1
                            cols[i].md_bg_color = (1, 1, 1, 1)

    def reset_square_design(self, square):
        """Resets the design of the Square"""
        square.md_bg_color = (self.app.get_rgba_from_hex('#f1f1f1'))
        square.ids.label.text_color = (0, 0, 0, 1)
        square.elevation = 0

    def show_confirmation_dialog(self):
        """Shows the confirmation dialog (MDDialog class)"""
        if not self.confirmation_dialog:
            raised_button = MDRaisedButton(
                text='Yes',
                text_color=self.app.theme_cls.primary_color,
                on_release=lambda x: self.go_to_form()

            )
            raised_button.text_color = (1, 1, 1, 1)
            self.confirmation_dialog = MDDialog(
                title="Want more information?",
                text='More details about your performance.',
                size_hint=(0.7, 1),
                buttons=[
                    raised_button,
                    MDFlatButton(
                        text='No, cancel',
                        text_color=self.app.theme_cls.primary_color,
                        on_release=lambda x: self.confirmation_dialog.dismiss())])
        self.confirmation_dialog.open()

    def go_to_form(self):
        """Switches to the form screen and dismisses the dialog box"""
        self.app.change_screen('form_screen')
        self.confirmation_dialog.dismiss()
