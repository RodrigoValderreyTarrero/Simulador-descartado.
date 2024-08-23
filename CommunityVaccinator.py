import random
from Simulation import Contagion, Simulation


class CommunityMember:
    def __init__(self, pr, id, community):
        self.pr = pr
        self.id = id
        self.community = community

class Community:
    def __init__(self, com_id):
        self.com_id = com_id
        self.members = set() #set of CommunityMember
        self.community_pr = 0
        self.num_vaccinated_people = 0
        self.community_size = 0


class CommunityVaccinator(Simulation):
    def __init__(self, notification_delay, monthly_vaccination_capacity_percentage, contagion_filename, contacts_file, community_file, method_distance,show_curve):
        super().__init__(notification_delay, monthly_vaccination_capacity_percentage, contagion_filename, contacts_file,method_distance,show_curve)
        self.output_filename = "CommunityVaccinator_" + str(self.monthly_vaccination_capacity_percentage) + ".txt"
        self.read_communities(community_file)

    def read_communities(self, community_file):
        try:
            self.G.graph['communities'] = {}
            with open(community_file, 'r') as file:
                for linea in file:
                    node, community = linea.strip().split()
                    node = int(node)
                    community = int(community)
                    if not self.G.has_node(node):
                        self.G.add_node(node, state="no-contact", notified=False, written=False)
                        # We add the nodes but they will not be connected to anyone
                    # every node has a community
                    self.G.nodes[node]['community'] = community

                    # if the community does not exist, it is created.
                    if community not in self.G.graph['communities']:
                        com = Community(com_id=community)
                        self.G.graph['communities'][community] = com
                    else:
                        com = self.G.graph['communities'][community]
                    com.members.add(node)
        except FileNotFoundError:
            print(f"The file does not exist {community_file} ")
        except Exception as e:
            print(f"There was an error opening the file: {community_file}. Error: {e}")

    def vaccinate(self):
        if self.method_distance == 1:
            self.first_method()
        elif self.method_distance == 2:
            self.second_method()
        elif self.method_distance == 3:
            self.third_method()

    def third_method(self):
        # Initialize a list to count the number of infected nodes per community
        community_infected_count = [0] * len(self.G.graph["communities"])

        # infections from the last 5 days
        past_five_days_infections = []
        for i in range(5):
            for infection in self.infections[self.notification_day - i]:
                past_five_days_infections.append(infection)

        # count the number of infected nodes / community
        target_nodes = [infection.target for infection in past_five_days_infections]
        community_counter = {}
        for target in target_nodes:
            community_id = self.G.nodes[target]['community']
            community_counter[community_id] = community_counter.get(community_id, 0) + 1

        # update community_infected_count using community_counter
        for community_id, count in community_counter.items():
            community_infected_count[community_id] = count

        # srt communities by the number of infections in descending order
        sorted_communities = sorted(community_counter, key=community_counter.get, reverse=True)

        max_infected_count = max(community_counter.values())
        nodes_with_X = []

        # Calculate the X value for each node
        for node in range(len(self.normalized_pr_list)):
            community_id = self.G.nodes[node]['community']
            norm_pr = self.normalized_pr_list[node][1]
            num_infectados = community_infected_count[community_id]

            if max_infected_count > 0:
                norm_inf = num_infectados / max_infected_count
            else:
                norm_inf = 0.0

            if norm_pr + norm_inf != 0:
                value_X = 2 * (norm_pr * norm_inf) / (norm_pr + norm_inf)
            else:
                value_X = 0.0

            nodes_with_X.append((node, value_X))

        #sort the nodes by the X value
        nodes_with_X.sort(key=lambda x: x[1], reverse=True)

        #vaccinate nodes based on X
        for node, _ in nodes_with_X:
            if self.available_vaccines_today == 0:
                break
            self.vaccine_if_corresponds(node)

    def second_method(self):
        past_five_days_infections = list()

        for i in range(5):
            for infection in self.infections[self.notification_day-i]:
                past_five_days_infections.append(infection)

        target_nodes = [infection.target for infection in past_five_days_infections]

        community_counter = {}
        for target in target_nodes:
            community_id = self.G.nodes[target]['community']


            if community_id in community_counter:
                community_counter[community_id] += 1
            else:
                community_counter[community_id] = 1
        sorted_communities = sorted(community_counter, key=community_counter.get, reverse=True)

        for comms in sorted_communities:
            nodes = self.G.graph['communities'][comms].members
            for node in nodes:
                self.vaccine_if_corresponds(node)

                if self.available_vaccines_today == 0:
                    return
        while self.available_vaccines_today > 0 and not self.check_end():
            self.vaccine_if_corresponds(random.randint(0,128260))

    def first_method(self):
        infections = self.infections[self.notification_day]
        target_nodes = [infection.target for infection in infections]
        # we get all target nodes from the infections and its comm

        communities = set(self.G.nodes[node]['community'] for node in target_nodes)

        # filtering by state and comm
        members_to_vaccinate = [
            node for node, pr in self.pagerank_list
            if self.G.nodes[node].get('state') in ('saved', 'no-contact') and self.G.nodes[node][
                'community'] in communities
        ]

        i = 0
        while self.available_vaccines_today > 0 and len(members_to_vaccinate) > i:
            # vaccine the available nodes following its pr
            self.vaccine_if_corresponds(members_to_vaccinate[i])
            i += 1

        # vaccine by pr
        i = 0
        while self.available_vaccines_today > 0 and len(self.pagerank_list) > i:
            node, _ = self.pagerank_list[i]
            self.vaccine_if_corresponds(node)
            i += 1

