from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen


class DataScreen(MDScreen):
    """Shows the data of a match"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()

    def show_data(self, data):
        self.ids.player1_name.text = data['winner_name']
        self.ids.player2_name.text = data['looser_name']
        self.ids.set1_player1.text = str(data['winner_total_games'][0])
        self.ids.set2_player1.text = str(data['winner_total_games'][1])
        self.ids.set3_player1.text = str(data['winner_total_games'][2])
        self.ids.set1_player2.text = str(data['looser_total_games'][0])
        self.ids.set2_player2.text = str(data['looser_total_games'][1])
        self.ids.set3_player2.text = str(data['looser_total_games'][2])
