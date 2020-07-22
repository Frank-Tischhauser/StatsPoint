from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.behaviors import RectangularElevationBehavior


class Rows(MDBoxLayout):
    pass


class DataLine(MDBoxLayout, RectangularElevationBehavior):
    pass


class LeaderBoard(MDGridLayout):
    pass


class DataScreen(MDScreen):
    """Shows the data of a match"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()

    def show_data(self, data):
        players = [self.ids.player1, self.ids.player2]
        stats = [data['player1_stats'], data['player2_stats']]
        for player, name, stat in zip(players, [data['player1_name'], data['player2_name']], stats):
            player.ids.player_name.text = name
            player.ids.set1.ids.label.text = str(stat['total_games'][0])
            player.ids.set2.ids.label.text = str(stat['total_games'][1])
            player.ids.set3.ids.label.text = str(stat['total_games'][2])
            self.square_design(name, player, data)

    def square_design(self, player_name, line_score, data):
        """Changes the square design when a player wins a set"""
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
                full_stats = data[str(player + '_stats')]
                serving_stats = full_stats['service_stats']
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
