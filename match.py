import json
import logging as log


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
        Name of the match.

    server : object
        Instance of the class Player. It is the player who serves.

    receiver : object
        Instance of the class Player. It is the player who receives.

    Methods
    -------
    counter(winner, opponent):
        Counts the total point number of a player for each set.

    get_match_name():
        returns the name of the match.

    points_win(winner, opponent):
        Is called each time a player wins a point.
        Returns the appropriate method depending on the scoreboard.

    games_win(winner, opponent):
        Is called each time a player wins a game.
        Returns the appropriate method depending on the scoreboard.

    sets_win(winner, opponent):
        Is called each time a player wins a set.
        Returns the appropriate method depending on the scoreboard.

    tie_break(winner, opponent):
        Is called at the start of a Tie-Break.
        Resets all the points_amount.

    end_match(winner, opponent):
        Is called at the end of a match.
        Creates a dict with the data of the match. Returns write_json method.

    change_server():
        The server becomes the receiver, and the receiver becomes the server.
    """

    points = [0, 15, 30, 40]
    games = [0, 1, 2, 3, 4, 5, 6, 7]
    sets = [0, 1, 2]

    def __init__(self, player1, player2, match_name):
        """
        Parameters
        ----------
        player1 : object
            Instance of the class Player. It is the player 1 of the match.
        player2: object
            Instance of the class Player. It is the player 2 of the match.
        match_name : str
            Name of the match.
        """

        self.player1 = player1
        self.player2 = player2
        self.match_name = match_name
        self.server = player1
        self.receiver = player2

    def counter(self, winner, opponent):
        """Counts the total point number of a player for each set."""
        if winner.sets_amount == 0 and opponent.sets_amount == 0:
            winner.total_points[0] += 1
            winner.total_games[0] = winner.get_games_amount()
        elif winner.sets_amount == 1 and opponent.sets_amount == 0 or winner.sets_amount == 0 \
                and opponent.sets_amount == 1:
            winner.total_points[1] += 1
            winner.total_games[1] = winner.get_games_amount()
        else:
            winner.total_points[2] += 1
            winner.total_games[2] = winner.get_games_amount()

    def get_match_name(self):
        return self.match_name

    def points_win(self, winner, opponent):
        """
        Is called each time a player wins a point.
        Returns the appropriate method depending on the scoreboard.
        """
        if winner.games_amount == 6 and opponent.games_amount == 6:
            self.tie_break(winner, opponent)
        elif winner.points_amount == 40 and opponent.points_amount != 40 \
                and opponent.points_amount != 'AD' \
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
                log.info('{} a {}pts'.format(winner.get_name(), winner.get_points_amount()))
        self.counter(winner, opponent)
        log.info(winner.get_total_points_amount())
        log.info(winner.get_total_games_amount())

    def games_win(self, winner, opponent):
        if winner.games_amount == 5 and opponent.games_amount < 5:
            index = Match.games.index(winner.games_amount)
            winner.games_amount = Match.games[index + 1]
            return self.sets_win(winner, opponent)

        elif winner.games_amount == 5 and opponent.games_amount == 6:
            winner.games_amount = 6
            winner.points_amount = 0
            opponent.points_amount = 0
            self.change_server()
        elif winner.games_amount == 6 and opponent.games_amount == 5:
            index = Match.games.index(winner.games_amount)
            winner.games_amount = Match.games[index + 1]
            return self.sets_win(winner, opponent)
        else:
            index = Match.games.index(winner.games_amount)
            winner.games_amount = Match.games[index + 1]
            self.change_server()
        self.counter(winner, opponent)
        log.info(winner.get_total_points_amount())
        log.info(winner.get_total_games_amount())

    def sets_win(self, winner, opponent):
        self.counter(winner, opponent)
        self.change_server()
        log.info(winner.get_total_points_amount())
        log.info(winner.get_total_games_amount())
        index = Match.sets.index(winner.sets_amount)
        winner.sets_amount = Match.sets[index + 1]
        winner.points_amount = 0
        opponent.points_amount = 0
        winner.games_amount = 0
        opponent.games_amount = 0
        if winner.sets_amount == 2:
            return self.end_match(winner, opponent)

    def tie_break(self, winner, opponent):
        winner.points_amount += 1

        if winner.points_amount < 7 or abs(winner.points_amount - opponent.points_amount) < 2:
            if (winner.points_amount + opponent.points_amount) % 2 == 1:
                self.change_server()
        else:
            index = Match.games.index(winner.games_amount)
            winner.games_amount = Match.games[index + 1]
            self.sets_win(winner, opponent)

        self.counter(winner, opponent)
        log.info(winner.get_total_points_amount())
        log.info(winner.get_total_games_amount())

    def end_match(self, winner, opponent):
        winner_name = winner.get_name()
        looser_name = opponent.get_name()
        dict = {"match_name": self.get_match_name(),
                "winner_name": winner_name,
                "winner_points": winner.total_points,
                "winner_games": winner.get_total_games_amount(),
                "looser_name": looser_name,
                "looser_points": opponent.total_points,
                "looser_games": opponent.get_total_games_amount(),
                }
        with open('data.json', 'r') as file:
            existant_data = json.load(file)
            existant_data.append(dict)
        with open('data.json', 'w') as js:
            json.dump(existant_data, js)

    def change_server(self):
        if self.server == self.player1:
            self.server = self.player2
            self.receiver = self.player1
        else:
            self.server = self.player1
            self.receiver = self.player2
        log.info(self.server.get_name())
