from kivymd.app import MDApp
import json
import itertools
import random


class DrillManager:

    def __init__(self):

        with open('drills.json', 'r', encoding='utf-8') as drills_file:
            self.drills = json.load(drills_file)

        with open('conditions.json', 'r', encoding='utf-8') as conditions_file:
            self.conditions = json.load(conditions_file)

        self.app = MDApp.get_running_app()
        self.player_info = self.app.root.ids.analysis_screen.player_info
        self.analysis_info = self.app.root.ids.analysis_screen.analysis_info
        self.avg_stats = self.get_average_stats()
        self.sorted_drills = []
        self.picked_drills = []
        self.drill_schedule = {}

    def sort_drills(self, level):
        for drill in self.drills:  # Sort depending on the level
            if level in drill["difficulty"]:
                self.sorted_drills.append(drill)

    def get_average_stats(self):
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
        parameters = {}
        for condition in self.conditions:
            if condition['style'] == self.analysis_info['style']:
                parameters = condition
        if self.analysis_info['level'] == 'advanced':
            index = 1
        else:
            index = 0

        if 100 * (self.avg_stats['first_service_won'] + self.avg_stats['second_service_won']) / self.avg_stats[
                    'service_points_played'] < parameters['service']['general'][index]:

            service_order = []
            first_serve_in = self.avg_stats['service_points_played'] - self.avg_stats['second_service']
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
                'backhand': self.avg_stats['backhand_winners'],
                'forehand': self.avg_stats['forehand_winners'],
                'net': self.avg_stats['net_winners']
            }
            winners = sorted(winners.items(), key=lambda kv: (kv[1], kv[0]))
            winner_order = []
            for x in winners:
                winner_order.append(x[0])
            self.drill_schedule['winner'] = winner_order

        if self.avg_stats['unforced_errors'] > parameters['unforced_error']['general'][index]:
            unforced_errors = {
                'backhand': self.avg_stats['backhand_unforced_errors'],
                'forehand': self.avg_stats['forehand_unforced_errors'],
                'net': self.avg_stats['net_unforced_errors']
            }
            unforced_errors = sorted(unforced_errors.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
            unforced_errors_order = []
            for x in unforced_errors:
                unforced_errors_order.append(x[0])
            self.drill_schedule['unforced_error'] = unforced_errors_order

    def pick_drill(self):
        if self.analysis_info['level'] == 'beginner':
            self.picked_drills = self.sorted_drills.copy()
        else:
            compteur = 0
            while len(self.picked_drills) < 3 and compteur < 3:
                for key, value in self.drill_schedule.items():
                    #  print(key, value)
                    for shot, drill in itertools.product(value, self.sorted_drills):
                        for shot_drill, category in drill['details'].items():
                            #  print(shot_drill, category)
                            if shot_drill == shot and key in category and drill not in self.picked_drills:
                                self.picked_drills.append(drill)
                                new_ordered_list = value.copy()
                                new_ordered_list.remove(shot)
                                new_ordered_list.append(shot)  # To move it at the end of the list
                                self.drill_schedule[key] = new_ordered_list
                                break
                        else:
                            continue
                        break

                compteur += 1

            while len(self.picked_drills) < 3:  # Backup if not enough drill chosen
                drill = self.sorted_drills[random.randint(0, len(self.sorted_drills))]
                if drill not in self.picked_drills:
                    self.picked_drills.append(drill)

            if len(self.picked_drills) > 3:  # Backup if too many drills chosen
                random.shuffle(self.picked_drills)
