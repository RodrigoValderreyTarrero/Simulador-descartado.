import sys
from Simulation import Contagion, Simulation
from collections import deque

class TopologyVaccinator(Simulation):
    def __init__(self, notification_delay, monthly_vaccination_capacity_percentage, contagion_filename, contacts_file, method_distance,show_curve):
        super().__init__(notification_delay, monthly_vaccination_capacity_percentage, contagion_filename, contacts_file, method_distance,show_curve)
        self.output_filename = "TopologyVaccinator_" + str(self.monthly_vaccination_capacity_percentage) + ".txt"

    def vaccinate(self):
        N = self.method_distance
        infections = self.infections[self.notification_day]
        #list to store all neighbors at distance 1
        neighbors_list = set()

        # get neighbors at distance 1 for each infected node
        for infection in infections:
            neighbors_1 = self.get_neighbors_at_exact_distance(infection.target, 1)
            neighbors_list.update(neighbors_1)

        # gf N == 2, also get neighbors at distance 2
        if N == 2:
            for infection in infections:
                neighbors_2 = self.get_neighbors_at_exact_distance(infection.target, 2)
                neighbors_list.update(neighbors_2)

        #vacinate nodes in the list according to pr order
        for node, _ in self.pagerank_list:
            if node in neighbors_list and self.available_vaccines_today > 0:
                self.vaccine_if_corresponds(node)
                if self.available_vaccines_today == 0:
                    return

        #if there are remaining vaccines, none are wasted
        for node, _ in self.pagerank_list:
            if self.available_vaccines_today > 0:
                self.vaccine_if_corresponds(node)
            else:
                return

