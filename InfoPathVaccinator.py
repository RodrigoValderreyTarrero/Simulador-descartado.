from Simulation import Contagion, Simulation


class InfoPathVaccinator(Simulation):
    def __init__(self, notification_delay, monthly_vaccination_capacity_percentage, contagion_filename, contacts_file, method_distance, show_curve, filename):
        super().__init__(notification_delay, monthly_vaccination_capacity_percentage, contagion_filename, contacts_file, method_distance, show_curve)
        self.output_filename = "InfoPathVaccinator_" + str(self.monthly_vaccination_capacity_percentage) + ".txt"
        self.infopath_list = self.read_infopath(filename)

    def read_infopath(self,nombre_archivo):
        with open(nombre_archivo, 'r') as archivo:
            linea = archivo.readline().strip()
            nums = linea.split(',')
            nums = [int(num) for num in nums if num.isdigit()]
        return nums

    def vaccinate(self):
        #iterate over the infopath_list and vaccinate nodes until no vaccines are available
        for node in self.infopath_list:
            if self.available_vaccines_today == 0:
                break
            self.vaccine_if_corresponds(node)



