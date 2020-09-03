import logging as log
from math import ceil
import random
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.metrics import dp
from akivymd.uix.piechart import AKPieChart


def safe_div(num1, num2):
    """Returns an integer division.
    Avoids error if division by zero."""
    if num2 <= 0:
        return 0
    return num1 / num2


class ResultScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.match_stats = None
        self.analysis_info = None
        self.piechart1 = None
        self.piechart2 = None
        self.piechart3 = None

    def on_pre_enter(self, *args):
        self.app.root.ids.my_toolbar.title = 'Diagrams'
        self.app.root.ids.my_toolbar.right_action_items = [["arrow-right", lambda x: log.info('Next Screen (Incoming)')]]
        self.match_stats = self.app.root.ids.analysis_screen.match_stats
        self.analysis_info = self.app.root.ids.analysis_screen.analysis_info
        if self.piechart1 is not None:
            self.ids.charts1.remove_widget(self.piechart1)
            self.ids.charts2.remove_widget(self.piechart2)
            self.ids.charts3.remove_widget(self.piechart3)
        items = self.get_piechart_stats()
        self.piechart1 = self.make_piechart(items[0])
        self.piechart2 = self.make_piechart(items[1])
        self.piechart3 = self.make_piechart(items[2])
        self.ids.charts1.add_widget(self.piechart1, 1)
        self.ids.charts2.add_widget(self.piechart2, 1)
        self.ids.charts3.add_widget(self.piechart3, 1)

    def get_piechart_stats(self):
        player_stats = self.match_stats['{}_stats'.format(self.analysis_info['player'])]
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
        for item in [item1[0], item2[0], item3[0]]:  # Trick to always have a total of 100 percent (May improve)
            while sum(item.values()) > 100:
                i = random.randint(1, len(item))
                item[str(i)] -= 1
        return [item1, item2, item3]

    def make_piechart(self, items):
        piechart = AKPieChart(
            items=items, pos_hint={'center_x': 0.5, 'center_y': .5},
            size_hint=[None, None],
            size=(dp(150), dp(150))
        )
        return piechart
