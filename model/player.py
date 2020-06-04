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
        current total points amount of the player for every set

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
        returns the total points amount of the player in the entire match

    """
    def __init__(self, name=''):
        self.name = name
        self.points_amount = 0
        self.games_amount = 0
        self.sets_amount = 0
        self.total_points = [0, 0, 0]

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
