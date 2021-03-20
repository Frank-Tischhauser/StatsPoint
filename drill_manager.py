"""
DrillManager

Finds 3 drills depending on a player's stats.
Using a sorting algorithm that is based on a player's :
Level, Style and result.
"""

import json
import logging as log
import random

from kivymd.app import MDApp


class DrillManager:
    """
    Class which manages all the drill sorting algorithm.
    ...
    Attributes
    ----------
    app : object
        Instance of the class StatsPointApp.

    analysis_info : dict
        Contains all the information about the chosen player in order to provide a good analysis.

    drills : list
        Contains the list of all available drills with all their information.

    conditions : list
        Contains all the limit conditions / rates
        that tell if a game part is a weakness of the player or not.

    player_info: dict
        All the stats of the player.

    avg_stats: dict
        The average of a player's stats for all completed sets.

    sorted_drills: list
        The list of all drills that corresponds to a player's level.

    drill_schedule: dict
        Contains all the weaknesses of a player found by the module.

    Methods
    -------
    sort_drills(level):
        Sort drills depending on the player's level.

    get_average_stats():
        Get the value of the avg_stats attribute.

    make_drill_schedule():
        Get the value of the drill_schedule attribute using the conditions attribute.

    pick_drill():
        Picks 3 drills depending on the statistics of a player.
    """

    def __init__(self):

        with open('json_files/drills.json', 'r', encoding='utf-8') as drills_file:
            self.drills = json.load(drills_file)
        with open('json_files/conditions.json', 'r', encoding='utf-8') as conditions_file:
            self.conditions = json.load(conditions_file)

        random.shuffle(self.drills)
        self.app = MDApp.get_running_app()
        self.player_info = self.app.root.ids.form_screen.player_info
        self.analysis_info = self.app.root.ids.form_screen.analysis_info
        self.avg_stats = self.get_average_stats()
        self.sorted_drills = []
        self.drill_schedule = {}

    def sort_drills(self, level):
        """Sort drills depending on the player's level"""
        for drill in self.drills:
            if level in drill["difficulty"]:
                self.sorted_drills.append(drill)

    def get_average_stats(self):
        """Get the value of the avg_stats attribute"""
        sorting_stats = {}
        for key, value in self.player_info.items():
            result = 0
            if type(value).__name__ == 'list' and key not in ['total_games', 'total_points']:
                for i in range(self.player_info['ended_sets']):
                    result += value[i]
                result /= self.player_info['ended_sets']
                result = round(result)
                sorting_stats[key] = result
            elif type(value).__name__ == 'dict':
                for service_key, service_value in value.items():
                    for i in range(self.player_info['ended_sets']):
                        result += service_value[i]
                    result /= self.player_info['ended_sets']
                    result = round(result)
                    sorting_stats[service_key] = result

        return sorting_stats

    def make_drill_schedule(self):
        """Get the value of the drill_schedule attribute using the conditions attribute"""
        parameters = {}
        for condition in self.conditions:
            if condition['style'] == self.analysis_info['style']:
                parameters = condition
        if self.analysis_info['level'] == 'advanced':
            index = 1
        else:
            index = 0

        if 100 * (self.avg_stats['first_service_won']
                  + self.avg_stats['second_service_won']) \
                / self.avg_stats['service_points_played'] < \
                parameters['service']['general'][index]:

            service_order = []
            first_serve_in = (self.avg_stats['service_points_played']
                              - self.avg_stats['second_service'])
            first_serve_in_ratio = first_serve_in * 100 / self.avg_stats['service_points_played']
            first_serve_won_ratio = self.avg_stats['first_service_won'] * 100 / first_serve_in
            second_serve_won_ratio = self.avg_stats['second_service_won'] * 100 / self.avg_stats[
                'second_service_in']

            if first_serve_in_ratio < parameters['service']['first_serve_in'][index]:
                service_order.append('first_serve_in')
            if first_serve_won_ratio < parameters['service']['first_serve_won'][index]:
                service_order.append('first_serve_won')
            if second_serve_won_ratio > parameters['service']['second_serve_won'][index]:
                service_order.append('second_serve_won')
            self.drill_schedule['service'] = service_order

        if 100 * self.avg_stats['return_points_won'] / self.avg_stats['return_points_played'] \
                < parameters['return']['general'][index]:
            self.drill_schedule['return'] = ['return']

        if self.avg_stats['winners'] < parameters['winner']['general'][index]:
            winners = {
                'backhand': self.avg_stats['backhand_winners'] + 1,  # Overall players tend to do less backhand winners
                'forehand': self.avg_stats['forehand_winners'],
                'net': self.avg_stats['net_winners'] + 1  # There is usually less volleys in a match
            }
            winners = sorted(winners.items(), key=lambda kv: (kv[1], kv[0]))
            winner_order = []
            for winner in winners:
                winner_order.append(winner[0])
            self.drill_schedule['winner'] = winner_order

        if self.avg_stats['unforced_errors'] > parameters['unforced_error']['general'][index]:
            unforced_errors = {
                'backhand': self.avg_stats['backhand_unforced_errors'],
                'forehand': self.avg_stats['forehand_unforced_errors'],
                'net': self.avg_stats['net_unforced_errors']
            }
            unforced_errors = sorted(
                unforced_errors.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
            unforced_errors_order = []
            for unforced_error in unforced_errors:
                unforced_errors_order.append(unforced_error[0])
            self.drill_schedule['unforced_error'] = unforced_errors_order

    def pick_drill(self):
        """Picks 3 drills depending on the statistics of a player"""
        picked_drills = []
        first_selection = []
        if self.analysis_info['level'] == 'beginner':
            picked_drills = self.sorted_drills.copy()
            return picked_drills
        else:
            # Selects only drills that belong to a category that is a weakness
            for drill in self.sorted_drills:
                corresponds = False
                for category in self.drill_schedule.keys():
                    if category in drill["details"].keys():
                        corresponds = True
                if corresponds:
                    first_selection.append(drill)
            log.info(self.drill_schedule)
            compteur = 0
            if len(first_selection) > 3:
                while len(picked_drills) < 3 and compteur <= 3 * len(self.drill_schedule):
                    item_to_move = []
                    for weak_type, weak_shots in self.drill_schedule.items():
                        corresponds = False  # True if a drill has been chosen
                        for weak_shot in weak_shots:
                            for drill in first_selection:
                                drill_shots = []  # Shots that the drill trains
                                drill_types = list(drill['details'].keys())  # Types of the drill
                                for drill_details in drill['details'].values():
                                    drill_shots.append(drill_details[0])

                                if weak_shot in drill_shots and weak_type in drill_types:
                                    # A weak shot corresponds to a drill_shot
                                    picked_drills.append(drill)
                                    item_to_move.append([weak_type, weak_shot])
                                    corresponds = True
                                    break
                            if corresponds:
                                break
                        if corresponds:
                            first_selection.remove(picked_drills[-1])  # Avoids doubles
                    for item in item_to_move:  # prioritises shots that have not been chosen yet
                        self.drill_schedule[item[0]].remove(item[1])
                        self.drill_schedule[item[0]].append(item[1])
                    compteur += 1
            else:
                picked_drills = first_selection.copy()
            while len(picked_drills) < 3:  # Backup if not enough drill chosen
                drill = self.sorted_drills[random.randint(0, len(self.sorted_drills) - 1)]
                if drill not in picked_drills:
                    picked_drills.append(drill)

            if len(picked_drills) > 3:  # Backup if too many drills chosen
                priority_drills = picked_drills[:len(self.drill_schedule)]

                if len(priority_drills) > 3:
                    random.shuffle(priority_drills)

                while len(priority_drills) < 3:
                    priority_drills.append(random.choice(picked_drills[len(self.drill_schedule):]))

                return priority_drills

            return picked_drills
