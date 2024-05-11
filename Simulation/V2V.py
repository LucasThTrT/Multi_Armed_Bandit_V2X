# This communication V2V is based on VANETs (Vehicular Ad Hoc Networks)
# The Quality of Service (QoS) will depend on the distance between the transmitter and the receiver and the traffic density in the area

import random
from Scenario import Scenario


class V2V(Scenario):
    def __init__(self, distance, traffic_density):
        super().__init__(distance, traffic_density, None)
        # Parameters

        # Scenario
        self.distance = distance                                                                           # Distance between the transmitter and the receiver in meters
        self.traffic_density = traffic_density                                                               # Traffic density in the area in percentage

        # To Define
        self.max_range = 300                                                                               # Max propagation Range in meters                      (TO DEFINE !!!!)
        self.communication_success_rate_distance_factor = 0.5                                              # Communication Success Rate Distance Factor           (TO DEFINE !!!!)
        self.transmission_time = 0.1                                                                       # Transmission time in seconds                         (TO DEFINE !!!!)
        self.retransmission_delay = 0.1                                                                    # Retransmission delay in seconds                      (TO DEFINE !!!!)
        self.computing_time = 0.1                                                                           # Computing time in seconds for the "router" vehicule  (TO DEFINE !!!!)

        # Admitted
        self.propagation_speed = 3 * 10 ** 8                                                                # Propagation speed in meters per second (Propagation speed in the air of an electromagnetic wave (WIFI))
        self.vehicule_length = 4.23                                                                         # Mean vehicle length in meters (in France)

        # 1 + Number of vehicles between V2V (distance / (space between vehicles + mean vehicle length)) * traffic density
        self.number_of_vehicles = 1 + self.distance // (self.space_between_vehicles + self.vehicule_length) * self.traffic_density  
        
        # Estimation of the space between vehicles
        self.space_between_vehicles = (self.distance / self.number_of_vehicles) - self.number_of_vehicles * (self.vehicle_length + self.space_between_vehicles)

        self.run()

    # Simulation of V2Vehicle communication
    def simple_V2Vehicle_simulation(self, time_delay, packet_lost):
        transmission_validated = False
        if self.space_between_vehicles > self.max_range:             # If the distance is bigger than the max range
            return transmission_validated              # The communication is not possible
        else:
            # We calculate the time delay & the number of packets lost
            time_delay = (self.space_between_vehicles / self.propagation_speed) + self.computing_time  # Time delay if no packet is lost
            while (random.random() > self.communication_success_rate_distance_factor):
                packet_lost += 1
                time_delay += (self.space_between_vehicles / self.propagation_speed) + self.retransmission_delay
            transmission_validated = True
            return transmission_validated, time_delay, packet_lost
            

    # Simulation of V2V communication with only one jump
    def simple_V2V_simulation(self,distance_to_V):
        transmission_validated = False
        packet_lost = 0
        if distance_to_V > self.max_range:             # If the distance is bigger than the max range
            return transmission_validated         # The communication is not possible
        else:
            # We calculate the time delay & the number of packets lost
            time_delay = self.transmission_time + (distance_to_V / self.propagation_speed)  # Time delay if no packet is lost
            while (random.random() > self.communication_success_rate_distance_factor):
                packet_lost += 1
                time_delay += self.transmission_time + (distance_to_V / self.propagation_speed) + self.retranmission_delay # Time delay if a packet is lost
            transmission_validated = True
            return [transmission_validated, time_delay, packet_lost]
        

    # Simulation of V2V communication with multiple jumps
    def complexe_V2V_simulation(self, vehicles_to_try):
        packet_lost = 0
        if self.space_between_vehicles > self.max_range:             # If the distance is bigger than the max range
                return False
        
        # first jump
        time_delay = self.transmission_time + (self.space_between_vehicles / self.propagation_speed)  # Time delay if no packet is lost
        while (random.random() > self.communication_success_rate_distance_factor):
            packet_lost += 1
            time_delay += self.transmission_time + (self.space_between_vehicles / self.propagation_speed) + self.retransmission_delay  # Time delay if a packet is lost

        while (vehicles_to_try > 1):    # next jumps
            transmission_validated, time_delay, packet_lost = self.simple_V2V_simulation(time_delay, packet_lost) # We simulate the next jump
            if not transmission_validated:
                return False
            vehicles_to_try -= 1
        
        return [True, time_delay, packet_lost]

    
    # Best V2V communication Test
    def best_V2V_simulation(self, memo_V2V, best_V2V_simulation):
        if memo_V2V[0] and memo_V2V[1] < best_V2V_simulation[1]:
            best_V2V_simulation = memo_V2V
        return best_V2V_simulation



    def V2V_simulation(self):
        transmission_validated = False
        best_V2V_simulation = [False, 60000, 0] # [transmission_validated, time_delay = 10min, packet_lost]
        # Simululate V2V communication for each possibility
        # We will try to communicate with each vehicle between the transmitter and the receiver
        number_of_vehicles = self.number_of_vehicles
        while (number_of_vehicles > 0):
            # Simulation of V2V communication with only one jump (direct V2V communication)
            distance_to_V = (self.space_between_vehicles + self.vehicule_length) * number_of_vehicles  # Distance to the Vulnerable road user and the vehicle        
            memo_simpleV2V = (self.simple_V2V_simulation(distance_to_V))

            # compare with the best V2V communication
            best_V2V_simulation = self.best_V2V_simulation(memo_simpleV2V, best_V2V_simulation)

            # Simulation of V2V communication with multiple jumps
            memo_complexe_V2V = self.complexe_V2V_simulation(number_of_vehicles)

            # compare with the best V2V communication
            best_V2V_simulation = self.best_V2V_simulation(memo_complexe_V2V, best_V2V_simulation)

            number_of_vehicles -= 1

        return best_V2V_simulation
    
    def run(self):
        result = self.V2V_simulation()
        print("Transmission validated: ", result[0])
        print("Time delay: ", result[1])
        print("Packet lost: ", result[2])