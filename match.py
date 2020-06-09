import json


class Match:

    """
    A class to represent a Tennis model and its rules.
    ...
    Attributes
    ----------
    player1 : object
        Instance of the class Player. It is the player 1 of the match.
    player2 : object
        Instance of the class Player. It is the player 2 of the match.
    match_name : str
        Name of the match

    Methods
    -------
    points_counter(winner, opponent):
        Counts the total point number of a player for each set.
    get_match_name():
        returns the name of the match.
    points_win(winner, opponent):
        Is called each time a player wins a point. Returns the appropriate method depending on the scoreboard.
    games_win(winner, opponent):
        Is called each time a player wins a game. Returns the appropriate method depending on the scoreboard.
    sets_win(winner, opponent):
        Is called each time a player wins a set. Returns the appropriate method depending on the scoreboard.
    tie_break(winner, opponent):
        Is called at the start of a Tie-Break. Resets all the points_amount.
    end_match(winner, opponent):
        Is called at the end of a match. Creates a dict with the data of the match. Returns write_json method.
    write_json(data):
        Appends the data to a json file.
    """

    points = [0, 15, 30, 40]
    games = [0, 1, 2, 3, 4, 5, 6, 7]
    sets = [0, 1, 2]

    def __init__(self, player1, player2, match_name, end=0):

        self.player1 = player1
        self.player2 = player2
        self.match_name = match_name
        self.end = end

    def points_counter(self, winner, opponent):
        if winner.sets_amount == 0 and opponent.sets_amount == 0:
            winner.total_points[0] += 1
        elif winner.sets_amount == 1 and opponent.sets_amount == 0 or winner.sets_amount == 0 and opponent.sets_amount == 1:
            winner.total_points[1] += 1
        else:
            winner.total_points[2] += 1

    def get_match_name(self):
        return self.match_name

    def points_win(self, winner, opponent):
        if winner.games_amount == 6 and opponent.games_amount == 6:
            winner.points_amount += 1
            if winner.points_amount < 7 or abs(winner.points_amount - opponent.points_amount) < 2:
                pass
            else:
                winner.points_amount = 0
                opponent.points_amount = 0
                winner.games_amount = 0
                opponent.games_amount = 0
                self.sets_win(winner, opponent)
        elif winner.points_amount == 40 and opponent.points_amount != 40 and opponent.points_amount != 'AD' \
                or winner.points_amount == 'AD':
            winner.points_amount = 0
            opponent.points_amount = 0
            return self.games_win(winner, opponent)

        else:

            if opponent.points_amount == 40 and winner.points_amount == 40:
                winner.points_amount = 'AD'
            elif opponent.points_amount == 'AD' and winner.points_amount == 40:
                opponent.points_amount = 40
            else:
                index = Match.points.index(winner.points_amount)
                winner.points_amount = Match.points[index + 1]
                print('{} a {}pts'.format(winner.get_name(), winner.get_points_amount()))
        self.points_counter(winner, opponent)
        print(winner.get_total_points_amount())

    def games_win(self, winner, opponent):

        if winner.games_amount == 5 and opponent.games_amount < 5:
            winner.games_amount = 0
            opponent.games_amount = 0
            return self.sets_win(winner, opponent)

        elif winner.games_amount == 5 and opponent.games_amount == 6:
            winner.games_amount = 6
            return self.tie_break(winner, opponent)
        elif winner.games_amount == 6 and opponent.games_amount == 5:
            winner.games_amount = 0
            opponent.games_amount = 0
            return self.sets_win(winner, opponent)
        else:
            index = Match.games.index(winner.games_amount)
            winner.games_amount = Match.games[index + 1]
        self.points_counter(winner, opponent)

    def sets_win(self, winner, opponent):
        self.points_counter(winner, opponent)
        index = Match.sets.index(winner.sets_amount)
        winner.sets_amount = Match.sets[index + 1]
        if winner.sets_amount == 2:
            return self.end_match(winner, opponent)

    def tie_break(self, winner, opponent):
        winner.points_amount = 0
        opponent.points_amount = 0

    def end_match(self, winner, opponent):
        winner_name = winner.get_name()
        looser_name = opponent.get_name()
        dict = {"match_name": self.get_match_name(),
                "winner_name": winner_name,
                "winner_points": winner.total_points,
                "looser_name": looser_name,
                "looser_points": opponent.total_points
                }
        return self.write_json(dict)

    def write_json(self, data):

        with open('data.json', 'r') as file:
            existant_data = json.load(file)
            existant_data.append(data)
        with open('data.json', 'w') as js:
            json.dump(existant_data, js)
