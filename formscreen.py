"""
FormScreen

This module contains the FormScreen class.
It creates the form that the user needs to complete.
"""


from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.behaviors import RectangularElevationBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.snackbar import Snackbar

import logging as log


class WhiteBox(RectangularElevationBehavior, MDBoxLayout):
    """Is a MDBoxLayout class with a shadow / elevation effect"""


class FormScreen(MDScreen):
    """
    Screen which contains a form to get information about the player.
    ...
    Attributes
    ----------
    app : object
        Instance of the class StatsPointApp.

    player_info : dict
        Contains all the information about the chosen player in order to provide a good analysis.

    match_stats : dict
        Contains all the information about a match.

    analysis_info : dict
        Contains all the information input in the form by the user.

    Methods
    -------
    on_pre_enter(*args):
        Is called just before the user sees the screen.

    get_checkbox_info():
        Get the information of the checkboxes.

    question_done():
        Checks that the user fulfills all the fields of the form.

    check_enough_data():
        Checks that enough data is available to provide a good analysis.
    """

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
        self.player_info = None
        self.analysis_info = {
            'player': '',
            'level': '',
            'style': '',
        }

    def on_pre_enter(self, *args):
        """Is called just before the user sees the screen"""
        self.match_stats = self.app.root.ids.data_screen.data
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
        """Gets the information of the checkboxes"""
        for key, value in self.ids.items():
            if key in self.ids_names.keys():
                if value.active:
                    self.analysis_info[value.group] = self.ids_names[key]
                    value.active = False

    def questions_done(self):
        """Checks that the user fulfills all the fields of the form"""
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
        """Checks that enough data is available to provide a good analysis"""
        pl_stats = self.match_stats['{}_stats'.format(self.analysis_info['player'])]
        compteur = 0
        for i in self.match_stats['sets_winners']:
            if i is not None:
                compteur += 1
        pl_stats['ended_sets'] = compteur
        self.player_info = pl_stats
        critical_stats = [pl_stats['backhand_unforced_errors'], pl_stats['forehand_unforced_errors'],
                          pl_stats['backhand_winners'], pl_stats['forehand_winners'], pl_stats['net_winners'],
                          pl_stats['net_unforced_errors']]
        enough_data = True
        for stat in critical_stats:
            if sum(stat) == 0:
                enough_data = False
        if self.player_info['ended_sets'] == 0:
            Snackbar(text='You need to finish at least 1 set!').show()
        elif not enough_data and self.player_info['ended_sets'] > 0:
            self.app.change_screen('training_screen')
        else:
            self.app.change_screen('diagram_screen')
