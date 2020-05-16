class Player:

    def __init__(self, name=''):
        self.name = name
        self.points_amount = 0
        self.games_amount = 0
        self.sets_amount = 0
        self.total_points = [0, 0]

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
