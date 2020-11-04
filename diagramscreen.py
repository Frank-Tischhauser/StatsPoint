"""
DiagramScreen

This module contains the DiagramScreen class.
It creates and displays nice and clean diagrams with a player's statistics.
"""

from math import ceil
import random
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.metrics import dp
from kivy.utils import platform
from akivymd.uix.piechart import AKPieChart


def safe_div(num1, num2):
    """Returns an integer division.
    Avoids error if division by zero."""
    if num2 <= 0:
        return 0
    return num1 / num2


class DiagramScreen(MDScreen):
    """
    Screen which contains 3 diagrams about the player's match.
    ...
    Attributes
    ----------
    app : object
        Instance of the class StatsPointApp.

    player_info : dict
        Contains all the information about the chosen player in order to provide a good analysis.

    piecharts : list
        Contains all the piechart widgets (UI).

    Methods
    -------
    on_pre_enter():
        Is called just before the user sees the screen.

    get_piechart_stats():
        Get all the stats necessary for the 3 piecharts.

    make_piechart():
        Creates the piechart.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.player_info = None
        self.piecharts = [0, 0, 0]

    def on_pre_enter(self, *args):
        """Is called just before the user sees the screen."""
        self.app.root.ids.my_toolbar.title = 'Diagrams'
        self.app.root.ids.my_toolbar.right_action_items = [
            ["arrow-right", lambda x: self.app.change_screen('training_screen')]]
        self.player_info = self.app.root.ids.form_screen.player_info

        if platform == 'win':  # Unwanted on phone
            self.ids.diagram_layout.spacing = dp(60)

        if self.piecharts[0] != 0:  # Resets all piecharts
            self.ids.charts1.remove_widget(self.piecharts[0])
            self.ids.charts2.remove_widget(self.piecharts[1])
            self.ids.charts3.remove_widget(self.piecharts[2])

        items = self.get_piechart_stats()
        for i in range(3):
            self.piecharts[i] = self.make_piechart(items[i])
        self.ids.charts1.add_widget(self.piecharts[0], 1)
        self.ids.charts2.add_widget(self.piecharts[1], 1)
        self.ids.charts3.add_widget(self.piecharts[2], 1)

    def get_piechart_stats(self):
        """"Get all the stats necessary for the 3 piecharts"""
        player_stats = self.player_info
        backhand_winners = sum(player_stats['backhand_winners'])
        forehand_winners = sum(player_stats['forehand_winners'])
        net_winners = sum(player_stats['net_winners'])
        total_winners = backhand_winners + forehand_winners + net_winners
        backhand_winners_ratio = ceil(safe_div(backhand_winners, total_winners) * 100)
        forehand_winners_ratio = ceil(safe_div(forehand_winners, total_winners) * 100)
        net_winners_ratio = ceil(safe_div(net_winners, total_winners) * 100)

        backhand_unforced_errors = sum(player_stats['backhand_unforced_errors'])
        forehand_unforced_errors = sum(player_stats['forehand_unforced_errors'])
        net_unforced_errors = sum(player_stats['net_unforced_errors'])
        total_unforced_errors = backhand_unforced_errors + forehand_unforced_errors + net_unforced_errors
        backhand_unforced_errors_ratio = ceil(safe_div(backhand_unforced_errors, total_unforced_errors) * 100)
        forehand_unforced_errors_ratio = ceil(safe_div(forehand_unforced_errors, total_unforced_errors) * 100)
        net_unforced_errors_ratio = ceil(safe_div(net_unforced_errors, total_unforced_errors) * 100)

        errors_ratio = ceil(safe_div(total_unforced_errors, total_unforced_errors + total_winners) * 100)
        winners_ratio = ceil(safe_div(total_winners, total_unforced_errors + total_winners) * 100)
        item1 = [{'1': backhand_winners_ratio, '2': forehand_winners_ratio, '3': net_winners_ratio}]

        item2 = [{'1': backhand_unforced_errors_ratio,
                  '2': forehand_unforced_errors_ratio,
                  '3': net_unforced_errors_ratio}]
        item3 = [{'1': winners_ratio, '2': errors_ratio}]
        for item in [item1[0], item2[0], item3[0]]:
            # Trick to always have a total of 100 percent (May improve)
            while sum(item.values()) > 100:
                i = random.randint(1, len(item))
                item[str(i)] -= 1
        return [item1, item2, item3]

    def make_piechart(self, items):
        """Creates the piechart"""
        piechart = AKPieChart(
            items=items, pos_hint={'center_x': 0.5, 'center_y': .5},
            size_hint=[None, None],
            size=(dp(150), dp(150))
        )
        return piechart
