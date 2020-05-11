class Player:

    points = [0, 15, 30, 40]
    games = [0, 1, 2, 3, 4, 5, 6, 7]
    sets = [0, 1, 2]

    def __init__(self, name='Frank'):
        self.name = name
        self.points_amount = 0
        self.games_amount = 0
        self.sets_amount = 0

    def get_name(self):
        return self.name

    def get_points_amount(self):
        return str(self.points_amount)

    def get_games_amount(self):
        return str(self.games_amount)

    def get_sets_amount(self):
        return str(self.sets_amount)

    def points_win(self, opponent):
        if self.games_amount == 6 and opponent.games_amount == 6:
            self.points_amount += 1
            if self.points_amount < 7 or abs(self.points_amount - opponent.points_amount) < 2:
                pass
            else:
                self.points_amount = 0
                opponent.points_amount = 0
                self.games_amount = 0
                opponent.games_amount = 0
                self.sets_win(opponent)
        elif self.points_amount == 40 and opponent.points_amount != 40 and opponent.points_amount != 'AD' \
                or self.points_amount == 'AD':
            print('{} wins the game'.format(self.name))
            self.points_amount = 0
            opponent.points_amount = 0
            return self.games_win(opponent)

        else:

            if opponent.points_amount == 40 and self.points_amount == 40:
                self.points_amount = 'AD'
            elif opponent.points_amount == 'AD' and self.points_amount == 40:
                opponent.points_amount = 40
            else:
                index = Player.points.index(self.points_amount)
                self.points_amount = Player.points[index + 1]
        print('{} a {} points'.format(self.get_name(), self.get_points_amount()))

    def games_win(self, opponent):

        if self.games_amount == 5 and opponent.games_amount < 5:
            self.games_amount = 0
            opponent.games_amount = 0
            return self.sets_win(opponent)

        elif self.games_amount == 5 and opponent.games_amount == 6:
            self.games_amount = 6
            return self.tie_break(opponent)
        elif self.games_amount == 6 and opponent.games_amount == 5:
            self.games_amount = 0
            opponent.games_amount = 0
            return self.sets_win(opponent)
        else:
            index = Player.games.index(self.games_amount)
            self.games_amount = Player.games[index + 1]

    def sets_win(self, opponent):
        index = Player.sets.index(self.sets_amount)
        self.sets_amount = Player.sets[index + 1]
        if self.sets_amount == 2:
            print('Fin du match')

    def tie_break(self, opponent):
        self.points_amount = 0
        opponent.points_amount = 0




