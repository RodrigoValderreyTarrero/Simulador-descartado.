import random
import sys
from Simulation import Contagion, Simulation
from collections import deque
import time

class PageRankVaccinator(Simulation):
    def __init__(self, notification_delay, monthly_vaccination_capacity_percentage, contagion_filename, contacts_file, method_distance, show_curve):
        super().__init__(notification_delay, monthly_vaccination_capacity_percentage, contagion_filename, contacts_file, method_distance, show_curve)
        self.output_filename = "PageRankVaccinator_" + str(self.monthly_vaccination_capacity_percentage) + ".txt"


    def vaccinate(self):
        # Iterate over the pagerank_list and vaccinate nodes until no vaccines are available
        for node, _ in self.pagerank_list:
            if self.available_vaccines_today == 0:
                break
            self.vaccine_if_corresponds(node)



