from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.behaviors import RectangularElevationBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
import logging as log


class WhiteBox(RectangularElevationBehavior, MDBoxLayout):
    pass


class AnalysisScreen(MDScreen):

    ids_names = {'check_player1': 'player1',
                 'check_player2': 'player2',
                 'check_level1': 'beginner',
                 'check_level2': 'intermediate',
                 'check_level3': 'advanced',
                 'check_style1': 'net',
                 'check_style2': 'all_court',
                 'check_style3': 'baseliner',
                 'check_style4': 'pusher'}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.match_stats = None
        self.analysis_info = {
            'player': '',
            'level': '',
            'style': '',
        }
        self.warning = None

    def on_pre_enter(self, *args):
        self.match_stats = self.app.root.ids.data_screen.match_stats
        self.app.root.ids.my_toolbar.right_action_items = [["arrow-left",
                                                            lambda x: self.app.change_screen('data_screen', 'right')]]
        self.app.root.ids.my_toolbar.title = 'Questions'
        log.info('Stats  : ' + str(self.match_stats))
        self.ids.player1.text = self.match_stats['player1_name']
        self.ids.player2.text = self.match_stats['player2_name']
        self.ids.error_message.opacity = 0
        for key, value in self.ids.items():
            if key in self.ids_names.keys():
                value.active = False  # Resets all checkboxes

    def get_checkbox_info(self):
        for key, value in self.ids.items():
            if key in self.ids_names.keys():
                if value.active:
                    self.analysis_info[value.group] = self.ids_names[key]
                    value.active = False

    def questions_done(self):
        counter = 0
        for key, value in self.ids.items():
            if key in self.ids_names.keys():
                if value.active:
                    counter += 1
        if counter == 3:
            self.get_checkbox_info()
            self.check_enough_data()
        else:
            self.ids.error_message.opacity = 1

    def check_enough_data(self):
        pl_stats = self.match_stats['{}_stats'.format(self.analysis_info['player'])]
        critical_stats = [pl_stats['backhand_unforced_errors'], pl_stats['forehand_unforced_errors'],
                          pl_stats['backhand_winners'], pl_stats['forehand_winners'], pl_stats['net_winners'],
                          pl_stats['net_unforced_errors']]
        enough_data = True
        for stat in critical_stats:
            if sum(stat) == 0:
                enough_data = False
        if not enough_data:  # To avoid error with diagrams (later : will just skip the diagrams to the next screen)
            Snackbar(text='Error! Not enough stats. Play more points!').show()

        else:
            self.app.change_screen('result_screen')
