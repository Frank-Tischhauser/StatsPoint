"""
StatsDisplay

Displays the statistics of a match for both players set by set (and total).
"""
from kivymd.app import MDApp


def safe_div(num1, num2):
    """Returns an integer division.
    Avoids error if division by zero."""
    if num2 <= 0:
        return 0
    return num1 / num2


class StatsDisplay:
    """
    Displays statistics of a match on a screen.
    ...
    Attributes
    ----------
    app : object
        Instance of the class StatsPointApp.

    data : dict
        Data of the match.

    players : list
        Index of players.

    settings: dict
        Configuration of the data display.

    caption: list
        Captions of all statistics.

    highlights: list
        Highlighting systems for each stat.

    Methods
    -------
    get_stats_sets(manche, player):
        Get the stats of the match for each set.

    get_match_stats(player):
        Get the stats of the entire match.

    display_stats(stats, leaderboard, player)
        Displays the statistics on the screen.

    write_captions(leaderboard):
        Write all the captions on the screen.
    """
    def __init__(self, data):
        self.app = MDApp.get_running_app()
        self.data = data
        self.players = ['player1', 'player2']
        self.settings = {
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
            'Net winners': 'max',
            'Net unforced errors': 'min',
            'Return points won': 'ratio',
            'Unforced errors': 'min',
            'Forehand unforced errors': 'min',
            'Backhand unforced errors': 'min'
        }
        self.caption = list(self.settings.keys())[::-1]
        self.highlights = list(self.settings.values())[::-1]

    def get_stats_sets(self, manche, player):
        """Get the stats of the match for each set"""
        name = self.data[str(player + '_name')]
        full_stats = self.data[str(player + '_stats')]
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

        stats = [
            name, full_stats['total_points'][manche], aces, double_faults, ratio_first_service_in,
            ratio_first_service_won,
            ratio_second_service_won, break_points_ratio, full_stats['winners'][manche],
            full_stats['forehand_winners'][manche], full_stats['backhand_winners'][manche],
            full_stats['net_points'][manche], full_stats['net_winners'][manche],
            full_stats['net_unforced_errors'][manche], return_ratio,
            full_stats['unforced_errors'][manche], full_stats['forehand_unforced_errors'][manche],
            full_stats['backhand_unforced_errors'][manche]][::-1]
        return stats

    def get_match_stats(self, player):
        """Get the stats of the entire match"""
        name = self.data[str(player + '_name')]
        full_stats = self.data[str(player + '_stats')]
        serving_stats = full_stats['service_stats']
        double_faults = sum(serving_stats['double_faults'])
        aces = sum(serving_stats['ace'])
        service_pts_played = sum(serving_stats['service_points_played'])
        nbr_first_service_in = service_pts_played - sum(serving_stats['second_service'])
        ratio_first_service_in = int(safe_div(nbr_first_service_in * 100,
                                              service_pts_played))
        ratio_first_service_won = int(safe_div(
            sum(serving_stats['first_service_won']) * 100, nbr_first_service_in))
        ratio_second_service_won = int(safe_div(
            sum(serving_stats['second_service_won']) * 100,
            sum(serving_stats['second_service_in'])))
        break_points = sum(full_stats['break_points'])
        #  break_points_conv = int(safe_div(
        #  full_stats['return_game_won'][manche] * 100, break_points))
        break_points_ratio = '{}/{}'.format(
            sum(full_stats['return_game_won']), break_points)

        return_ratio = '{}/{}'.format(sum(full_stats['return_points_won']),
                                      sum(full_stats['return_points_played']))

        stats = [name, sum(full_stats['total_points']), aces, double_faults, ratio_first_service_in,
                 ratio_first_service_won,
                 ratio_second_service_won, break_points_ratio, sum(full_stats['winners']),
                 sum(full_stats['forehand_winners']), sum(full_stats['backhand_winners']),
                 sum(full_stats['net_points']), sum(full_stats['net_winners']),
                 sum(full_stats['net_unforced_errors']), return_ratio,
                 sum(full_stats['unforced_errors']), sum(full_stats['forehand_unforced_errors']),
                 sum(full_stats['backhand_unforced_errors'])][::-1]
        return stats

    def display_stats(self, stats, leaderboard, player):
        """Displays the statistics on the screen"""
        stats = list(map(str, stats))

        for row, j in zip(leaderboard.children, range(len(self.caption))):
            cols = []
            for col in row.ids.values():
                cols.append(col)
            cols.pop(1)
            cols[self.players.index(player)].ids.label.text = stats[j]
            if stats[j] == self.data[str(player + '_name')]:
                cols[self.players.index(player)].size_hint = 1, 1
                cols[self.players.index(player)].md_bg_color = (1, 1, 1, 1)

    def write_captions(self, leaderboard):
        """Write all the captions on the screen"""
        for row, i in zip(leaderboard.children, range(len(self.caption))):
            row.ids.col2.text = self.caption[i]  # Writes all the captions
            row.highlight = self.highlights[i]
