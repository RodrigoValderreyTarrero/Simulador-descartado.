import sys
import argparse
from TopologyVaccinator import TopologyVaccinator
from CommunityVaccinator import CommunityVaccinator
from TotalVaccinator import TotalVaccinator
from RandomVaccinator import RandomVaccinator
from PageRankVaccinator import PageRankVaccinator
from PageRankInfectionVaccinator import PageRankInfectionVaccinator
from InfoPathVaccinator import InfoPathVaccinator
def display_help():
    help_text = """
    Usage: script.py [OPTIONS]

    Run vaccination simulation to evaluate different vaccination strategies.

    Options:
      -nd, --notification_delay INT                (default: 2)
          Delay (in days) before notifying a susceptible individual of their exposure.

      -mvcp, --monthly_vaccination_capacity_percentage FLOAT (default: 0.1)
          Percentage of the population that can be vaccinated each month.

      -cf, --contagion_filename FILENAME           (default: 'infected_traze')
          Filename containing the infection trace data. 

      -ctd, --contacts_directory DIRECTORY        (default: 'contacts_directory')
          Directory containing the social contact network data.
           
      -vs, --vaccination_strategy STRATEGY      (default: '1')
          Vaccination strategy to use:
            1: TopologyVaccinator
            2: CommunityVaccinator
            3: RandomVaccinator
            4: PageRankVaccinator
            5: InfoPathVaccinator

      -cmf, --community_file FILENAME             (default: None)
          **Only for CommunityRank strategy:** Filename containing community information.

      --opt, --options                            Show this help message and exit.

      -md, --method_distance INT                  (default: 1)
          **CommunityRank and Topology strategies:**
            - For CommunityVaccinator: method 
            - For Topology: distance (e.g., 1 for direct contacts, 2 for contacts of contacts)
    """
    print(help_text)
    sys.exit(0)


def main():
    parser = argparse.ArgumentParser(description='Run vaccination simulation.')
    parser.add_argument('-nd', '--notification_delay', type=int, default=5)
    parser.add_argument('-mvcp', '--monthly_vaccination_capacity_percentage', type=float, default=0.03)
    parser.add_argument('-cf', '--contagion_filename', type=str, default='infected_traze')
    parser.add_argument('-ctd', '--contacts_directory', type=str, default='contacts_directory')
    parser.add_argument('-vs', '--vaccination_strategy', type=str, default='1', )
    parser.add_argument('-cmf', '--community_file', type=str, default=None,)
    parser.add_argument('--opt', '--options', action='store_true', )
    parser.add_argument('-md', '--method_distance', type=int, default=1)
    parser.add_argument('-sc', '--show_curve', type=bool, default=False)
    parser.add_argument('-if', '--infopath_filename', type=str, default="infopath_file.txt")

    args = parser.parse_args()
    if args.opt:
        display_help()

    if args.vaccination_strategy == "1":
        Simulation = TopologyVaccinator(args.notification_delay, args.monthly_vaccination_capacity_percentage, args.contagion_filename, args.contacts_directory, args.method_distance,args.show_curve)
    elif args.vaccination_strategy == "2":
        if args.community_file is None:
            print("Community file must be provided for CommunityVaccinator.")
            sys.exit(1)
        Simulation = CommunityVaccinator(args.notification_delay, args.monthly_vaccination_capacity_percentage, args.contagion_filename, args.contacts_directory, args.community_file, args.method_distance,args.show_curve)
    elif args.vaccination_strategy == "3":
        Simulation = RandomVaccinator(args.notification_delay, args.monthly_vaccination_capacity_percentage, args.contagion_filename, args.contacts_directory, args.method_distance,args.show_curve)
    elif args.vaccination_strategy == "4":
        Simulation = PageRankVaccinator(args.notification_delay, args.monthly_vaccination_capacity_percentage, args.contagion_filename, args.contacts_directory, args.method_distance,args.show_curve)
    elif args.vaccination_strategy == "5":
        if args.infopath_filename is None:
            print("Infopath file must be provided for InfoPathVaccinator.")
            sys.exit(1)
        Simulation = InfoPathVaccinator(args.notification_delay, args.monthly_vaccination_capacity_percentage, args.contagion_filename, args.contacts_directory, args.method_distance,args.show_curve, args.infopath_filename)
    else:
        print("Invalid vaccination strategy.")
        sys.exit(1)
    Simulation.run_simulation()

if __name__ == "__main__":
    main()
