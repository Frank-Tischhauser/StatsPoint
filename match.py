"""
Match

Module that manages the scoring and saving of a tennis match.
"""

import json
import logging as log

from kivymd.app import MDApp


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

    app : object
        Instance of the class StatsPointApp.

    set_index : int
        Number of played sets.

    sets_winners : list
        Winner of each set.

    Methods
    -------
    points_games_counter(winner):
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

    save_match(match_ended):
        Is called when the game stops.
        Saves the game in a JSON file.

    ace_played():
        Called when a player serves an ace.

    check_break_point(winner, opponent):
        Checks if it's a break point, if yes +1 in the statistics.

    change_server():
        The server becomes the receiver, and the receiver becomes the server.
    """

    points = [0, 15, 30, 40]
    games = [0, 1, 2, 3, 4, 5, 6, 7]
    sets = [0, 1, 2]

    def __init__(self, player1, player2, match_name, server=None, receiver=None, sets_winners=None):
        """
        Parameters
        ----------
        player1 : object
            Instance of the class Player. It is the player 1 of the match.
        player2: object
            Instance of the class Player. It is the player 2 of the match.
        match_name : str
            Name of the match.
        server : object
            Instance of the class Player. The player who is serving.
        receiver : object
            Instance of the class Player. The player who is returning.
        sets_winners : list
            Winner of each set.
        """
        if server is None:
            server = player1
        if receiver is None:
            receiver = player2
        if sets_winners is None:
            sets_winners = [None, None, None]

        self.player1 = player1
        self.player2 = player2
        self.match_name = match_name
        self.server = server
        self.receiver = receiver
        self.set_index = self.player1.sets_amount + self.player2.sets_amount
        self.app = MDApp.get_running_app()
        self.sets_winners = sets_winners

    def points_games_counter(self, winner):
        """Counts the total point number of a player for each set."""
        winner.total_points[self.set_index] += 1
        winner.total_games[self.set_index] = winner.games_amount
        log.info('{} a {}pts'.format(winner.get_name(), winner.get_points_amount()))
        log.info('Résumé des points gagnés dans le match {}'.format(
            winner.get_total_points_amount()))
        log.info('Résumé des jeux gagnés dans le match {}'.format(winner.get_total_games_amount()))

    def get_match_name(self):
        """Gets the name of the match"""
        return self.match_name

    def points_win(self, winner, opponent):
        """
        Is called each time a player wins a point.
        Returns the appropriate method depending on the scoreboard.
        """
        self.server.service_stats['service_points_played'][self.set_index] += 1
        self.receiver.stats['return_points_played'][self.set_index] += 1
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
            self.check_break_point(winner, opponent)
        self.points_games_counter(winner)

    def games_win(self, winner, opponent):
        """Is called each time a player wins a game.
        Returns the appropriate method depending on the scoreboard."""
        if self.server == opponent:  # Counts the number of return games won
            winner.stats['return_game_won'][self.set_index] += 1
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
        self.points_games_counter(winner)

    def sets_win(self, winner, opponent):
        """
        Is called each time a player wins a set.
        Returns the appropriate method depending on the scoreboard.
        """
        self.points_games_counter(winner)
        self.change_server()
        index = Match.sets.index(winner.sets_amount)
        winner.sets_amount = Match.sets[index + 1]
        winner.points_amount = 0
        opponent.points_amount = 0
        winner.games_amount = 0
        opponent.games_amount = 0
        self.sets_winners[self.set_index] = winner.name
        self.set_index = self.player1.sets_amount + self.player2.sets_amount
        if winner.sets_amount == 2:
            self.app.root.ids.game_screen.leave_match(True)  # Forces the end of the match

    def tie_break(self, winner, opponent):
        """Is called at the start of a Tie-Break.
        Resets all the points_amount."""
        winner.points_amount += 1

        if winner.points_amount < 7 or abs(winner.points_amount - opponent.points_amount) < 2:
            if (winner.points_amount + opponent.points_amount) % 2 == 1:
                self.change_server()
        else:
            index = Match.games.index(winner.games_amount)
            winner.games_amount = Match.games[index + 1]
            self.sets_win(winner, opponent)

        self.points_games_counter(winner)

    def save_match(self, match_ended):
        """Is called when the game stops.
        Saves the game in a JSON file."""
        player1_name = self.player1.get_name()
        player2_name = self.player2.get_name()
        players = [self.player1, self.player2]
        for player in players:
            player.stats['points'] = player.points_amount
            player.stats['games'] = player.games_amount
            player.stats['sets'] = player.sets_amount
        dictionnary = {"match_name": self.get_match_name(),
                       "player1_name": player1_name,
                       "player1_stats": self.player1.stats,
                       "player2_name": player2_name,
                       "player2_stats": self.player2.stats,
                       "server": self.server.name,
                       "receiver": self.receiver.name,
                       "sets_winners": self.sets_winners,
                       "match_ended": match_ended,
                       }
        with open('../statspoint_data.json', 'r') as file:
            existant_data = json.load(file)
            existant_data.append(dictionnary)
        with open('../statspoint_data.json', 'w') as js_file:
            json.dump(existant_data, js_file, indent=4, sort_keys=True)

    def change_server(self):
        """The server becomes the receiver, and the receiver becomes the server"""
        if self.server == self.player1:
            self.server = self.player2
            self.receiver = self.player1
        else:
            self.server = self.player1
            self.receiver = self.player2
        log.info('Le serveur est ' + self.server.get_name())

    def ace_played(self):
        """Called when a player serves an ace"""
        log.info(self.server.name)
        self.server.service_stats['ace'][self.set_index] += 1

    def check_break_point(self, winner, opponent):
        """Checks if it's a break point, if yes +1 in the statistics"""
        if winner == self.receiver:
            if winner.points_amount == 'AD' or \
                    winner.get_points_amount() == '40' and opponent.get_points_amount() != '40':
                winner.stats['break_points'][self.set_index] += 1
