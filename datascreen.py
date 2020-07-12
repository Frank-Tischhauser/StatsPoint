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
        caption = ['VS', 'Aces', 'Double Faults', '1st Serve (%)', '1st Serve Points Won (%)',
                   '2nd Serve Points Won (%)']
        players = ['player1', 'player2']
        leaderboard = [self.ids.set1_stats, self.ids.set2_stats, self.ids.set3_stats]

        for set in range(3):
            i = 0
            for row in leaderboard[set].ids.values():
                row.ids.col2.text = caption[i]  # Writes all the captions
                i += 1
            for player in players:
                name = data[str(player + '_name')]
                serving_stats = data[str(player + '_serving_stats')]
                double_faults = serving_stats['double_faults'][set]
                aces = serving_stats['ace'][set]
                service_pts_played = serving_stats['service_points_played'][set]
                nbr_first_service_in = service_pts_played - serving_stats['second_service'][set]
                ratio_first_service_in = safe_div(nbr_first_service_in * 100, service_pts_played)
                ratio_first_service_won = safe_div(serving_stats['first_service_won'][set] * 100, nbr_first_service_in)
                ratio_second_service_won = safe_div(serving_stats['second_service_won'][set] * 100,
                                                    serving_stats['second_service_in'][set])
                stats = [name, aces, double_faults, ratio_first_service_in, ratio_first_service_won,
                         ratio_second_service_won]
                stats = list(map(str, stats))
                j = 0
                for row in leaderboard[set].ids.values():
                    cols = []
                    for col in row.ids.values():
                        cols.append(col)
                    cols.pop(1)
                    cols[players.index(player)].text = stats[j]
                    j += 1


def safe_div(x, y):
    if y <= 0:
        return 0
    return int(x / y)
