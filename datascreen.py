"""
DataScreen

This module contains the DataScreen class and all the classes which are related to it.
This screen contains and shows all the statistics of a tennis match.
"""

from kivy.properties import StringProperty

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.behaviors import RectangularElevationBehavior
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog

def safe_div(num1, num2):
    """Returns an integer division.
    Avoids error if division by zero."""
    if num2 <= 0:
        return 0
    return num1 / num2


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
    """Table which contains DataLines"""

    def add_rows(self, rows_number=16):
        """Add the rows that will include all the stats"""
        self.rows = rows_number
        rows_liste = []
        for i in range(rows_number):
            rows_liste.append(Rows())
        for row, j in zip(rows_liste, range(rows_number)):
            self.add_widget(row)


class DataScreen(MDScreen):
    """Shows the data of a match"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.set1_stats = LeaderBoard()
        self.set1_stats.add_rows()
        self.set2_stats = LeaderBoard()
        self.set2_stats.add_rows()
        self.set3_stats = LeaderBoard()
        self.set3_stats.add_rows()
        self.match_stats = None
        self.confirmation_dialog = None

    def on_pre_enter(self, *args):
        self.app.root.ids.my_toolbar.right_action_items = [["magnify", lambda x: self.show_confirmation_dialog()]]
        self.confirmation_dialog = None

    def start(self):
        self.ids.set1_scroll.add_widget(self.set1_stats)
        self.ids.set2_scroll.add_widget(self.set2_stats)
        self.ids.set3_scroll.add_widget(self.set3_stats)

    def number_comparison(self, col1, col3, highlight='max'):
        """Highlights the right statistic depending on number values"""
        result = None, None
        if highlight == 'ratio':  # Highlights the greatest number ratio
            ratio1 = col1.ids.label.text
            col1.ids.label.font_size = '15sp'
            col3.ids.label.font_size = '15sp'
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

    def show_confirmation_dialog(self):
        if not self.confirmation_dialog:
            self.confirmation_dialog = MDDialog(title='Do you want to check the analysis (experimental)?',
                                 size_hint=(0.7, 1),
                                 buttons=[
                                     MDRaisedButton(text='Yes', text_color=self.app.theme_cls.primary_color,
                                                  on_release=lambda x: self.go_to_analysis()),
                                     MDFlatButton(text='No cancel', text_color=self.app.theme_cls.primary_color,
                                                  on_release=lambda x: self.confirmation_dialog.dismiss())])
        self.confirmation_dialog.open()

    def go_to_analysis(self):
        self.app.change_screen('analysis_screen')
        self.confirmation_dialog.dismiss()

    def show_scoreboard(self, data):
        """Shows a scoreboard with the result of the tennis match"""
        self.match_stats = data
        players = [self.ids.player1, self.ids.player2]
        stats = [data['player1_stats'], data['player2_stats']]
        for player, name, stat in zip(players, [data['player1_name'], data['player2_name']], stats):
            player.ids.player_name.text = name
            player.ids.set1.ids.label.text = str(stat['total_games'][0])
            player.ids.set2.ids.label.text = str(stat['total_games'][1])
            player.ids.set3.ids.label.text = str(stat['total_games'][2])
            self.change_square_design(name, player, data)

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

    def show_stats(self, data):
        """Shows all statistics of a tennis match"""
        data_settings = {
            'VS': 'name',
            'Total points won': 'max',
            'Aces': 'max',
            'Double Faults': 'min',
            '1st Serve in (%)': 'max',
            '1st Serve Pts Won (%)': 'max',
            '2nd Serve Pts Won (%)': 'max',
            'Break points converted': 'ratio',
            'Winners': 'max',
            'Forehand winners': 'max',
            'Backhand winners': 'max',
            'Net points': 'max',
            'Return points won': 'ratio',
            'Unforced errors': 'min',
            'Forehand unforced errors': 'min',
            'Backhand unforced errors': 'min'

        }
        caption = list(data_settings.keys())[::-1]
        highlights = list(data_settings.values())[::-1]  # "highlight" property of each row
        players = ['player1', 'player2']
        leaderboard = [self.set1_stats, self.set2_stats, self.set3_stats]

        for manche in range(3):
            for row, i in zip(leaderboard[manche].children, range(len(caption))):
                row.ids.col2.text = caption[i]  # Writes all the captions
                row.highlight = highlights[i]
            for player in players:
                name = data[str(player + '_name')]
                full_stats = data[str(player + '_stats')]
                serving_stats = full_stats['service_stats']
                double_faults = serving_stats['double_faults'][manche]
                aces = serving_stats['ace'][manche]
                service_pts_played = serving_stats['service_points_played'][manche]
                nbr_first_service_in = service_pts_played - serving_stats['second_service'][manche]
                ratio_first_service_in = int(safe_div(nbr_first_service_in * 100,
                                                      service_pts_played))
                ratio_first_service_won = int(safe_div(
                    serving_stats['first_service_won'][manche] * 100, nbr_first_service_in))
                ratio_second_service_won = int(safe_div(
                    serving_stats['second_service_won'][manche] * 100,
                    serving_stats['second_service_in'][manche]))
                break_points = full_stats['break_points'][manche]
                #  break_points_conv = int(safe_div(
                #  full_stats['return_game_won'][manche] * 100, break_points))
                break_points_ratio = '{}/{}'.format(
                    full_stats['return_game_won'][manche], break_points)

                return_ratio = '{}/{}'.format(full_stats['return_points_won'][manche],
                                              full_stats['return_points_played'][manche])

                stats = [name, full_stats['total_points'][manche], aces, double_faults, ratio_first_service_in,
                         ratio_first_service_won,
                         ratio_second_service_won, break_points_ratio, full_stats['winners'][manche],
                         full_stats['forehand_winners'][manche], full_stats['backhand_winners'][manche],
                         full_stats['net_points'][manche], return_ratio,
                         full_stats['unforced_errors'][manche], full_stats['forehand_unforced_errors'][manche],
                         full_stats['backhand_unforced_errors'][manche]][::-1]

                stats = list(map(str, stats))
                for row, j in zip(leaderboard[manche].children, range(len(caption))):
                    cols = []
                    for col in row.ids.values():
                        cols.append(col)
                    cols.pop(1)
                    cols[players.index(player)].ids.label.text = stats[j]
                    if stats[j] == name:
                        cols[players.index(player)].size_hint = 1, 1
                        cols[players.index(player)].md_bg_color = (1, 1, 1, 1)

    def check_stat_winner(self):
        """Highlights the best statistic between both players"""

        sets = [self.set1_stats, self.set2_stats, self.set3_stats]
        for manche in sets:
            for row in manche.children:
                cols = [row.ids.col1, row.ids.col3]
                winner_col, looser_col = self.number_comparison(cols[0], cols[1], row.highlight)
                if winner_col is not None and looser_col is not None:
                    winner_col.md_bg_color = (0.91, 0.46, 0.07, 1)
                    winner_col.ids.label.text_color = (1, 1, 1, 1)
                    winner_col.elevation = 5
                    self.reset_square_design(looser_col)
                else:
                    self.reset_square_design(cols[0])
                    self.reset_square_design(cols[1])

                if row.highlight == 'name':
                    cols[0].size_hint_x = 1
                    cols[0].md_bg_color = (1, 1, 1, 1)
                    cols[1].size_hint_x = 1
                    cols[1].md_bg_color = (1, 1, 1, 1)

    def reset_square_design(self, square):
        """Resets the design of the Square"""
        square.md_bg_color = (self.app.get_rgba_from_hex('#f1f1f1'))
        square.ids.label.text_color = (0, 0, 0, 1)
        square.elevation = 0
