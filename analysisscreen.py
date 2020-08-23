from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.behaviors import RectangularElevationBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
import logging as log


class WhiteBox(RectangularElevationBehavior, MDBoxLayout):
    pass


class AnalysisScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.match_stats = None
        self.menu = None

    def on_pre_enter(self, *args):
        self.match_stats = self.app.root.ids.data_screen.match_stats
        self.app.root.ids.my_toolbar.right_action_items = [["arrow-left",
                                                            lambda x: self.app.change_screen('data_screen', 'right')]]
        log.info('Stats  : ' + str(self.match_stats))
        self.ids.player1.text = self.match_stats['player1_name']
        self.ids.player2.text = self.match_stats['player2_name']


