import random
from Simulation import Contagion, Simulation


class RandomVaccinator(Simulation):
    def __init__(self, notification_delay, monthly_vaccination_capacity_percentage, contagion_filename, contacts_file, method_distance,show_curve):
        super().__init__(notification_delay, monthly_vaccination_capacity_percentage, contagion_filename, contacts_file, method_distance,show_curve)
        self.output_filename = "RandomVaccinator_" + str(self.monthly_vaccination_capacity_percentage) + ".txt"

    def vaccinate(self):
        # Obtener todos los nodos del grafo
        all_nodes = list(self.G.nodes())

        # Filtrar nodos que no estén "infected" ni "vaccinated"
        eligible_nodes = [node for node in all_nodes if self.G.nodes[node]['state'] not in ['infected', 'vaccinated']]
        while self.available_vaccines_today > 0 and eligible_nodes:
            if eligible_nodes:
                # Pick random
                node_to_vaccinate = random.choice(eligible_nodes)
                self.vaccine_if_corresponds(node_to_vaccinate)
                eligible_nodes.remove(node_to_vaccinate)


