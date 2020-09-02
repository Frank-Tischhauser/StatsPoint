class Player:
    """
    A class to represent a Tennis Player.
    ...
    Attributes
    ----------
    name : str
        name of the player
    points_amount : int
        current points amount of the player (0, 15, 30, 40, AD) in a game
    games_amount : int
        current games amount of the player in a set
    sets_amount : int
        current sets amount of the player in a match
    total_points : list
        current total points amount of the player for every set.

    Methods
    -------
    get_name():
        returns the name of the player.
    get_points_amount():
        returns the current points amount of the player.
    get_games_amount():
        returns the current games amount of the player.
    get_sets_amount():
        returns the current sets amount of the player.
    get_total_points_amount():
        returns the total points amount of the player in the entire match.

    """

    def __init__(self, name='', stats=None):
        if stats is None:
            stats = {
                'points': 0,
                'games': 0,
                'sets': 0,
                'total_points': [0, 0, 0],
                'return_points_won': [0, 0, 0],
                'return_points_played': [0, 0, 0],
                'total_games': [0, 0, 0],
                'break_points': [0, 0, 0],
                'return_game_won': [0, 0, 0],
                'winners': [0, 0, 0],
                'backhand_winners': [0, 0, 0],
                'forehand_winners': [0, 0, 0],
                'net_winners': [0, 0, 0],
                'net_points': [0, 0, 0],
                'unforced_errors': [0, 0, 0],
                'backhand_unforced_errors': [0, 0, 0],
                'forehand_unforced_errors': [0, 0, 0],
                'net_unforced_errors': [0, 0, 0],
                'service_stats': {
                     'ace': [0, 0, 0],
                     'double_faults': [0, 0, 0],
                     'second_service': [0, 0, 0],
                     'second_service_in': [0, 0, 0],
                     'service_points_played': [0, 0, 0],
                     'first_service_won': [0, 0, 0],
                     'second_service_won': [0, 0, 0]}
                }
        self.name = name
        self.stats = stats
        self.points_amount = stats['points']
        self.games_amount = stats['games']
        self.sets_amount = stats['sets']
        self.total_points = stats['total_points']
        self.total_games = stats['total_games']
        self.service_stats = stats['service_stats']

    def get_name(self):
        return self.name

    def get_points_amount(self):
        return str(self.points_amount)

    def get_games_amount(self):
        return str(self.games_amount)

    def get_sets_amount(self):
        return str(self.sets_amount)

    def get_total_points_amount(self):
        return self.total_points

    def get_total_games_amount(self):
        return self.total_games
