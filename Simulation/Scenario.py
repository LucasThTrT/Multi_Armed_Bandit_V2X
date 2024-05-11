# This class is used to define the context of the simulation


class Scenario:
    def __init__(self, distance, traffic_density, network_coverage):
        self.distance = distance                    # Distance between the transmitter and the receiver in meters
        self.traffic_density = traffic_density      # Traffic density in the area in percentage
        self.network_coverage = network_coverage    # Network coverage in the area in percentage
        self.run()                                 # Run the simulation

    def run(self):
        # Simulation of V2V communication
        from V2V import V2V
        V2V_simulation = V2V(self.distance, self.traffic_density)


# This class is used to define the scenario of the simulation