from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout


class Rows(MDBoxLayout):
    pass


class LeaderBoard(MDGridLayout):
    pass


class DataScreen(MDScreen):
    """Shows the data of a match"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()

    def show_data(self, data):
        self.ids.player1_name.text = data['player1_name']
        self.ids.player2_name.text = data['player2_name']
        self.ids.set1_player1.text = str(data['player1_total_games'][0])
        self.ids.set2_player1.text = str(data['player1_total_games'][1])
        self.ids.set3_player1.text = str(data['player1_total_games'][2])
        self.ids.set1_player2.text = str(data['player2_total_games'][0])
        self.ids.set2_player2.text = str(data['player2_total_games'][1])
        self.ids.set3_player2.text = str(data['player2_total_games'][2])

    def show_service_stats(self, data):
        set_widget = [self.ids.set1_stats, self.ids.set2_stats, self.ids.set3_stats]
        for sets in range(3):
            set_widget[sets].ids.row1.ids.col1.text = data['player1_name']
            set_widget[sets].ids.row1.ids.col2.text = 'VS'
            set_widget[sets].ids.row1.ids.col3.text = data['player2_name']
            set_widget[sets].ids.row2.ids.col1.text = str(data['player1_serving_stats']['ace'][sets])
            set_widget[sets].ids.row2.ids.col2.text = 'Aces'
            set_widget[sets].ids.row2.ids.col3.text = str(data['player2_serving_stats']['ace'][sets])
            set_widget[sets].ids.row3.ids.col1.text = str(data['player1_serving_stats']['double_faults'][sets])
            set_widget[sets].ids.row3.ids.col2.text = 'Double Faults'
            set_widget[sets].ids.row3.ids.col3.text = str(data['player2_serving_stats']['double_faults'][sets])
            if data['player1_serving_stats']['service_points_played'][sets] > 0:
                pl1_first_serve_number = data['player1_serving_stats']['service_points_played'][sets] - \
                                         data['player1_serving_stats']['second_service_number'][sets]
                pl1_first_serve_in_ratio = (pl1_first_serve_number / data['player1_serving_stats']['service_points_played'][sets]) * 100
                pl1_first_serve_won_ratio = (data['player1_serving_stats']['first_service_won'][sets] / pl1_first_serve_number) * 100
                set_widget[sets].ids.row4.ids.col1.text = str(int(pl1_first_serve_in_ratio)) + '%'
                set_widget[sets].ids.row5.ids.col1.text = str(int(pl1_first_serve_won_ratio)) + '%'
                if data['player1_serving_stats']['second_service_number'][sets] > 0:
                    pl1_second_serve_won_ratio = (data['player1_serving_stats']['second_service_won'][sets] / data['player1_serving_stats']['second_service_number'][sets]) * 100
                    set_widget[sets].ids.row6.ids.col1.text = str(int(pl1_second_serve_won_ratio)) + '%'

            if data['player2_serving_stats']['service_points_played'][sets] > 0:
                pl2_first_serve_number = data['player2_serving_stats']['service_points_played'][sets] - \
                                         data['player2_serving_stats']['second_service_number'][sets]
                pl2_first_serve_in_ratio = (pl2_first_serve_number / data['player2_serving_stats']['service_points_played'][sets]) \
                                           * 100
                set_widget[sets].ids.row4.ids.col3.text = str(int(pl2_first_serve_in_ratio)) + '%'
                pl2_first_serve_won_ratio = (data['player2_serving_stats']['first_service_won'][sets] / pl2_first_serve_number) * 100
                set_widget[sets].ids.row5.ids.col3.text = str(int(pl2_first_serve_won_ratio)) + '%'

                if data['player2_serving_stats']['second_service_number'][sets] > 0:
                    pl2_second_serve_won_ratio = (data['player2_serving_stats']['second_service_won'][sets] / data['player2_serving_stats']['second_service_number'][sets]) * 100
                    set_widget[sets].ids.row6.ids.col3.text = str(int(pl2_second_serve_won_ratio)) + '%'
            set_widget[sets].ids.row4.ids.col2.text = '1st serve acc. (%)'
            set_widget[sets].ids.row5.ids.col2.text = '1st serve pts won (%)'
            set_widget[sets].ids.row6.ids.col2.text = '2nd serve pts won (%)'

