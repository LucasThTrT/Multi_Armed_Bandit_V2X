# This communication V2V is based on VANETs (Vehicular Ad Hoc Networks)
# The Quality of Service (QoS) will depend on the distance between the transmitter and the receiver and the traffic density in the area

import random
from Scenario import Scenario


class V2V(Scenario):
    def __init__(self, distance, traffic_density):
        super().__init__(distance, traffic_density, None)
        # Parameters

        # Scenario
        self.distance = distance                                                                            # Distance between the transmitter and the receiver in meters
        self.traffic_density = traffic_density                                                              # Traffic density in the area in percentage

        # To Define
        self.max_range = 300                                                                                # Max propagation Range in meters                      (TO DEFINE !!!!)
        self.communication_success_rate_distance_factor = 0.5                                               # Communication Success Rate Distance Factor           (TO DEFINE !!!!) rate / distance
        self.transmission_time = 0.1                                                                        # Transmission time in seconds                         (TO DEFINE !!!!)
        self.retransmission_delay = 0.1                                                                     # Retransmission delay in seconds                      (TO DEFINE !!!!)
        self.computing_time = 0.3                                                                           # Computing time in seconds for the "router" vehicule  (TO DEFINE !!!!)

        # Admitted
        self.propagation_speed = 3 * 10 ** 8                                                                # Propagation speed in meters per second (Propagation speed in the air of an electromagnetic wave (WIFI))
        self.vehicle_length = 4.2                                                                           # Mean vehicle length in meters (in France)
        self.minimal_space_between_vehicles = 1                                                             # Minimal space between vehicles in meters (in France)


        # 1 + Number of vehicles between V2V (distance / (space between vehicles + mean vehicle length)) * traffic density
        self.number_of_vehicles = int((self.distance // (self.vehicle_length + self.minimal_space_between_vehicles)) * self.traffic_density)
        print("Number of vehicles: ", self.number_of_vehicles)

        # Estimation of the space between vehicles
        self.space_between_vehicles = round((self.distance - (self.number_of_vehicles * (self.vehicle_length))) / self.number_of_vehicles,1)
        print("Space between vehicles: ", self.space_between_vehicles)

        print("Place prise par les véhicules: ", self.number_of_vehicles * (self.vehicle_length + self.space_between_vehicles))
        self.run()


    # Simulation of V2Vehicle communication
    def simple_V2Vehicle_simulation(self, time_delay, packet_lost):
        transmission_validated = False
        if self.space_between_vehicles > self.max_range:             # If the distance is bigger than the max range
            return transmission_validated                            # The communication is not possible
        else:
            # We calculate the time delay & the number of packets lost
            time_delay = (self.space_between_vehicles / self.propagation_speed) + self.computing_time  # Time delay if no packet is lost
            while (random.random() > (self.communication_success_rate_distance_factor * (self.space_between_vehicles / self.max_range))):
                packet_lost += 1
                time_delay += (self.space_between_vehicles / self.propagation_speed) + self.retransmission_delay
            transmission_validated = True
            return transmission_validated, time_delay, packet_lost
            

    # Simulation of V2V communication with only one jump
    def simple_V2V_simulation(self,distance_to_V):
        transmission_validated = False
        packet_lost = 0
        if distance_to_V > self.max_range:             # If the distance is bigger than the max range
            return [transmission_validated]              # The communication is not possible
        else:
            # We calculate the time delay & the number of packets lost
            time_delay = self.transmission_time + (distance_to_V / self.propagation_speed)  # Time delay if no packet is lost
            while (random.random() > (self.communication_success_rate_distance_factor * (distance_to_V / self.max_range))):
                packet_lost += 1
                time_delay += self.transmission_time + (distance_to_V / self.propagation_speed) + self.retransmission_delay # Time delay if a packet is lost
            transmission_validated = True
            return [transmission_validated, time_delay, packet_lost]
        

    # Simulation of V2V communication with multiple jumps
    def complexe_V2V_simulation(self, vehicles_to_try):
        packet_lost = 0
        if self.space_between_vehicles > self.max_range:             # If the distance is bigger than the max range
                return [False]
        
        # first jump
        time_delay = self.transmission_time + (self.space_between_vehicles / self.propagation_speed)  # Time delay if no packet is lost
        while (random.random() > self.communication_success_rate_distance_factor):
            packet_lost += 1
            time_delay += self.transmission_time + (self.space_between_vehicles / self.propagation_speed) + self.retransmission_delay  # Time delay if a packet is lost

        while (vehicles_to_try > 1):    # next jumps
            transmission_validated, time_delay, packet_lost = self.simple_V2Vehicle_simulation(time_delay, packet_lost) # We simulate the next jump
            if not transmission_validated:
                return [False]
            vehicles_to_try -= 1
        
        # Last jump to the Vulnerable road user
        transmission_validated, time_delay_last, packet_lost_last = self.simple_V2Vehicle_simulation(time_delay, packet_lost) # We simulate the last jump

        return [transmission_validated, time_delay + time_delay_last, packet_lost + packet_lost_last]

    
    # Best V2V communication Test
    def best_V2V_simulation(self, memo_V2V, best_V2V_simulation):
        if memo_V2V[0] and memo_V2V[1] < best_V2V_simulation[1]:
            best_V2V_simulation = memo_V2V
        return best_V2V_simulation


    # Simulation of V2V communication
    # def V2V_simulation(self):
        transmission_validated = False
        best_V2V_simulation = [transmission_validated, 600000, 0,"methode"] # [transmission_validated, time_delay = 10min, packet_lost]
        # Simululate V2V communication for each possibility
        # We will try to communicate with each vehicle between the transmitter and the receiver
        number_of_vehicles = self.number_of_vehicles

        # while (number_of_vehicles > 0):

        # Simulation of V2V communication with only one jump (direct V2V communication)
        distance_to_V = (self.space_between_vehicles + self.vehicle_length) * number_of_vehicles  # Distance to the Vulnerable road user and the vehicle        
        memo_simpleV2V = (self.simple_V2V_simulation(distance_to_V))

        # compare with the best V2V communication
        best_V2V_simulation[0:2] = self.best_V2V_simulation(memo_simpleV2V, best_V2V_simulation)
        best_V2V_simulation[3] = 0


        # Simulation of V2V communication with multiple jumps
        memo_complexe_V2V = self.complexe_V2V_simulation(number_of_vehicles)

        # compare with the best V2V communication
        best_V2V_simulation[0:2] = self.best_V2V_simulation(memo_complexe_V2V, best_V2V_simulation)
        best_V2V_simulation[3] = 1

        number_of_vehicles -= 1

        return best_V2V_simulation
    

    # Run the simulation
    def run(self):
        result = self.V2V_simulation()
        print("Transmission validated: ", result[0])
        print("Time delay: ", result[1])
        print("Packet lost: ", result[2])
        if result[3] == 0:
            print("Method: Simple V2V simulation")
        else:
            print("Method: Complexe V2V simulation")

            

# Test
# Test avec Simulation simple V2V possible
print("------------------------------------------------------")
for i in range(1, 10):
    print("Test ", i)
    #V2V(250, 0.1 * i)
    print("------------------------------------------------------")

# Test avec Simulation simple V2V impossible
print("------------------------------------------------------")
for i in range(1, 10):
    print("Test ", i)
    #V2V(350, 0.1 * i)
    print("------------------------------------------------------")

for i in range(0, 2):
    print("Test ", i)
    for j in range(1,i):
        print(j)